
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore")
#to supress RuntimeWarning: Mean of empty slice
#This is because, we are taking mean across all patients, and some patients don't have data for some time points
#Thus, the mean of those time points across all patients will be NaN, which is not an error


import plotly.graph_objects as go
from plotly.subplots import make_subplots


#Global variables
sampling_rate=512;
bin_size=50;
data_load_path="../../Code_5_sci_rep_review_1_test/data/"


data=pd.read_json(data_load_path+"all_mean_Swiss-Short_bin"+str(bin_size)+".json",orient="records")
# Columns: file_ID	pat_id	sez_id	band	sez_length	no_of_elec	pre_mean	pre_sd	sez_mean	sez_sd	post_mean	post_sd

#Custom function to calculate std hading empty arrays
custom_nanstd = lambda data: np.nanstd(data, ddof=1) if np.count_nonzero(~np.isnan(data)) > 1 else(
    np.unique(data * (~np.isnan(data)))[0] if np.count_nonzero(~np.isnan(data)) == 1 else np.nan
)


pat_grouped_data = data.groupby(['band','pat_id']).agg(
    pre_mean=('pre_mean', 'mean'),
    pre_sd=('pre_sd', lambda x: custom_nanstd(x)),
    sez_mean=('sez_mean', 'mean'),
    sez_sd=('sez_sd', lambda x: custom_nanstd(x)),
    post_mean=('post_mean', 'mean'),
    post_sd=('post_sd', lambda x: custom_nanstd(x)),
    sezs=('file_ID', 'unique'),
    sez_length=('sez_length', 'mean'),
    no_of_elec=('no_of_elec','unique'),
    no_of_sez=('sez_id', 'count')
    )
pat_grouped_data = pat_grouped_data.reset_index()  

band_grouped_data = pat_grouped_data.groupby(['band']).agg(
    pre_mean=('pre_mean', 'mean'),
    pre_sd=('pre_sd', lambda x: custom_nanstd(x)),
    sez_mean=('sez_mean', 'mean'),
    sez_sd=('sez_sd', lambda x: custom_nanstd(x)),
    post_mean=('post_mean', 'mean'),
    post_sd=('post_sd', lambda x: custom_nanstd(x)),
    no_of_pats=('pat_id', 'count'),
    )
band_grouped_data = band_grouped_data.reset_index()  


bandds=pd.DataFrame({'name':['delta','theta','alpha','beta','lgamma','hgamma'], 
             'sym':["δ","θ","α","β","Lγ","Hγ"],
             'color':["rgba(139,0,0,0.5)","rgba(255,69,0,0.5)","rgba(0,205,0,0.5)","rgba(0,206,209,0.5)","rgba(105,89,205,0.5)","rgba(238,122,233,0.5)"]})


def mappi(fig,bd,ridx,cidx,p1,p2,p3):
    x_coords = [0, 1, 2]
    means=band_grouped_data.query('band=="'+bd+'"')[['pre_mean','sez_mean','post_mean']].iloc[0].values
    #sems=band_grouped_data.query('band=="'+bd+'"')[['pre_sd','sez_sd','post_sd']].iloc[0].values
    
    fig.add_trace(go.Scatter(x=x_coords,y=means,mode='lines+markers',
                             #error_y=dict(type='data', array=sems,color='rgba(0,0,0,0.5)', thickness=1.5, width=10),
                             name=bandds[bandds.name==bd].sym.values[0],
                             marker=dict(color=bandds[bandds.name==bd].color.values[0],size=10),
                             line=dict(color=bandds[bandds.name==bd].color.values[0],width=3)
                             ),row=ridx, col=cidx)
    fig.update_xaxes(tickvals=x_coords,ticktext=["pre", "seizure", "post"],row=ridx, col=cidx)
        
    # p_value_brackets = [
    #         {'x_coords': [0,0,0.99,0.99],
    #         'y_coords': [means[0]  +0.05, means[1] + +0.1 ,
    #                     means[1]  +0.1 , means[1] + 0.05 ],
    #         'label': p1},
    #         {'x_coords': [1.01,1.01,2,2],
    #         'y_coords': [means[1] +  0.05, means[1]  + 0.1,
    #                     means[1] +  0.1, means[2]  + 0.05],
    #         'label': p2},
    #         {'x_coords': [0,0,2,2],
    #         'y_coords': [means[1]  + 0.17, means[1]  +0.27,
    #                     means[1]  + 0.27, means[1]  + 0.17 ],
    #         'label': p3}
    #         ] 
    # if (ridx*cidx!=6):
    #     # Add p-value brackets and labels
    #     for bracket in p_value_brackets:
    #         for i in range(1, len(bracket['x_coords'])):
    #             fig.add_shape(dict(type="line", xref="x", yref="y",
    #                 x0=bracket['x_coords'][i - 1],x1=bracket['x_coords'][i],
    #                 y0=bracket['y_coords'][i - 1],y1=bracket['y_coords'][i]),
    #                 line=dict(color='rgba(0,0,0,1)', width=1.5),
    #                 row=ridx, col=cidx)
    #         fig.add_annotation(dict(
    #             text=bracket['label'],name="p-value",xref="x", 
    #             x=(bracket['x_coords'][0] + bracket['x_coords'][2]) / 2,
    #             y=bracket['y_coords'][1]+0.08,
    #             showarrow=False),
    #             font=dict(size=30, color="black",family="Times new Roman"),
    #             row=ridx, col=cidx)
    return fig

fig = make_subplots(rows=2, cols=3,vertical_spacing=0.07,horizontal_spacing=0.08,shared_xaxes=True,
                    subplot_titles=(
                            "Delta (δ) Band",
                            "Theta (θ) Band",
                            "Alpha (α) Band",
                            "Beta (β) Band",
                            "Lgamma (Lγ) Band",
                            "Hgamma (Hγ) Band"))

# This P values are calculated seperately using using a linear mixed-effect model implemented in Matlab 2020b
# See section 3.1 last paragraph of the paper for more details
mappi(fig,"delta",1,1,"<0.001","ns","<0.001")
mappi(fig,"theta",1,2,"<0.001","<0.001","ns")
mappi(fig,"alpha",1,3,"<0.001","<0.001","ns")
mappi(fig,"beta",2,1,"<0.001","<0.001","<0.001")
mappi(fig,"lgamma",2,2,"<0.001","<0.001","ns")
mappi(fig,"hgamma",2,3,"<0.001","<0.001","ns")

# Doing the H gamma seperate as it has very small scale and hard to fit in the generall fitting
means=band_grouped_data.query('band=="hgamma"')[['pre_mean','sez_mean','post_mean']].iloc[0].values
# p_value_brackets = [
#             {'x_coords': [0,0,0.99,0.99],
#             'y_coords': [means[0]  +0.03, means[1] + +0.04 ,
#                         means[1]  +0.04 , means[1] + 0.03 ],
#             'label': "<0.001"},
#             {'x_coords': [1.01,1.01,2,2],
#             'y_coords': [means[1] +  0.03, means[1]  + 0.04,
#                         means[1] +  0.04, means[2]  + 0.03],
#             'label': "<0.001"},
#             {'x_coords': [0,0,2,2],
#             'y_coords': [means[1]  + 0.09, means[1]  +0.11,
#                         means[1]  + 0.11, means[1]  + 0.09 ],
#             'label': "ns"}] 

# for bracket in p_value_brackets:
#         for i in range(1, len(bracket['x_coords'])):
#                 fig.add_shape(dict(type="line", xref="x", yref="y",
#                     x0=bracket['x_coords'][i - 1],x1=bracket['x_coords'][i],
#                     y0=bracket['y_coords'][i - 1],y1=bracket['y_coords'][i]),
#                     line=dict(color='rgba(0,0,0,1)', width=1.5),
#                     row=2, col=3)
#         fig.add_annotation(dict(
#                 text=bracket['label'],name="p-value",xref="x", 
#                 x=(bracket['x_coords'][0] + bracket['x_coords'][2]) / 2,
#                 y=bracket['y_coords'][1]+0.03,
#                 showarrow=False),
#                 font=dict(size=30, color="black",family="Times new Roman"),
#                 row=2, col=3)


# fig.update_yaxes(title_text="average AE",range=(2.65,3.95),row=1, col=1)
# fig.update_yaxes(range=(1.6,3.4),row=1, col=2)
# fig.update_yaxes(range=(1.1,2.9),row=1, col=3)
# fig.update_yaxes(title_text="average AE",range=(1.1,2.9),row=2, col=1)
# fig.update_yaxes(range=(0.2,1.5),row=2, col=2)
# fig.update_yaxes(range=(0.03,0.47),row=2, col=3)


fig.for_each_xaxis(lambda x: x.update(gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))
fig.for_each_yaxis(lambda x: x.update(gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))


fon_sz=30;
fig.update_layout(
        legend=dict(orientation="h",yanchor="bottom",y=1.05,xanchor="center",x=0.5,font=dict(color="blue",size=40)),
        template="plotly_white",
        font_family="Times new Roman",font_color="black",font_size=fon_sz,height=800,width=1500)
fig.update_annotations(font=dict(family="Times new Roman", size=30))



fig.show()
fig.write_image("../images/Fig3_bin50.png")
# fig.write_html("../images/Fig3.html")

