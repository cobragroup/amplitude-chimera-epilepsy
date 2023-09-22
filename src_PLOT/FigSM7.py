
import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Creating folder for the SM9 figures
import os
if not os.path.exists('../images/figSM7'):
   os.makedirs('../images/figSM7')
   
   
   
data=pd.read_json("../data/all_mean_Swiss-Short.json",orient="records")
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


bandds=pd.DataFrame({'name':['delta','theta','alpha','beta','lgamma','hgamma'], 
             'sym':["δ","θ","α","β","Lγ","Hγ"],
             'color':["rgba(139,0,0,0.5)","rgba(255,69,0,0.5)","rgba(0,205,0,0.5)","rgba(0,206,209,0.5)","rgba(105,89,205,0.5)","rgba(238,122,233,0.5)"]})


# Suplimentary Figure 7
# Plotting the average AE for each band for each patient

for pid in range(1,17):        
        x_coords = [0, 1, 2]
        s=pat_grouped_data.query('pat_id=='+str(pid))[['band','pre_mean','sez_mean','post_mean']]
        fig = make_subplots(rows=3, cols=2,vertical_spacing=0.1,horizontal_spacing=0.2,shared_xaxes=True,subplot_titles=(
                                "Delta (δ) Band",
                                "Theta (θ) Band",
                                "Alpha (α) Band",
                                "Beta (β) Band",
                                "Lgamma (Lγ) Band",
                                "Hgamma (Hγ) Band"))
        
        bad=["delta","theta","alpha","beta","lgamma","hgamma"]
        bd_idx=0

        for ridx in range(1,4):
                for cidx in range(1,3):
                        bd=bad[bd_idx]
                        means=s.query('band=="'+bd+'"')[['pre_mean','sez_mean','post_mean']].iloc[0].values
                        fig.add_trace(go.Scatter(x=x_coords,y=means,mode='lines+markers',
                                        #error_y=dict(type='data', array=sems,color='rgba(0,0,0,0.5)', thickness=1.5, width=10),
                                        name=bandds[bandds.name==bd].sym.values[0],
                                        marker=dict(color=bandds[bandds.name==bd].color.values[0],size=40),
                                        line=dict(color=bandds[bandds.name==bd].color.values[0],width=3)
                                        ),row=ridx, col=cidx)
                        fig.update_xaxes(tickvals=x_coords,ticktext=["pre", "seizure", "post"],row=ridx, col=cidx)
                        bd_idx+=1

        fig.update_yaxes(title_text="average AE",row=1, col=1)
        fig.update_yaxes(title_text="average AE",row=2, col=1)
        fig.update_yaxes(title_text="average AE",row=3, col=1)

        fig.for_each_xaxis(lambda x: x.update(gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))
        fig.for_each_yaxis(lambda x: x.update(gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))


        fon_sz=60;
        fig.update_layout(
            title_text="Patient ID: "+str(pid),
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5,font=dict(color="blue",size=50)),template="plotly_white",
            font_family="Times new Roman",font_color="black",font_size=fon_sz,height=1500,width=1500)
        
        fig.update_annotations(font=dict(family="Times new Roman", size=40))

        #fig.show()    
        fig.write_image("../images/figSM7/FigSM7_ID"+str(pid)+".png")   



