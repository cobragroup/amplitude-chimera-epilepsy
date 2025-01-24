
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore")
#to supress RuntimeWarning: Mean of empty slice


import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Global variables
sampling_rate=512;
bin_size=10;
#Time-slice to show in SM5
t1=2;t2=5;
#Time-points to show in SM5
st=2.5;ut=4; #This should match the values generated in "unfiltered_data_gen.py"
        
data_load_path="../../Code_4/data/"

##SUP Figure - 5
df=pd.read_json(data_load_path+"all_unfiltered_mean_AE_Swiss-Short.json",orient="records")
#Columns: pat_ID - elec_no - mean_AE - std_AE

# The 5 plot
no_of_timepoints=len(df['mean_AE'][0])
time=np.arange(0,no_of_timepoints)/(60*sampling_rate) #in minutes

fig= make_subplots(rows=8, cols=2,vertical_spacing=0.024,horizontal_spacing=0.02,shared_xaxes='all',shared_yaxes='all',subplot_titles=("ID1","ID2","ID3","ID4","ID5","ID6","ID7","ID8","ID9","ID10","ID11","ID12","ID13","ID14","ID15","ID16"))

pid=1 #patient ID
for ridx in range(1,9): #iterate over rows
    for cidx in range(1,3): #iterate over columns
        tim=time[(t1*60*sampling_rate):(t2*60*sampling_rate)] #showing only time-slice between t1 and t2
        mean=np.array(df.loc[pid-1]['mean_AE'][(t1*60*sampling_rate):(t2*60*sampling_rate)])
        mean[np.equal(mean, None)]=np.nan #Replace None with 0.0
        #stdd=np.array(df.loc[pid-1]['std_aa'][(2*60*sampling_rate):(5*60*sampling_rate)]) #not showing the std

        fig.add_trace(go.Scatter(x=tim,y=mean,
                                mode='lines',
                                line=dict(width=0.5),
                                showlegend=False,
                                ),row=ridx,col=cidx)
        pid+=1

# Adding vertical lines to show the T1 and T2 and seizure onset 
fig.add_shape(dict(type="line",x0=3,y0=1.5,x1=3,y1=6,line=dict(color="red", width=3)),row="all",col="all")

fig.add_annotation(dict(text="seizure onset",xref='x',yref='y',
        x=2.6,y=5.7,showarrow=False),font=dict(size=10, color="red",family="Times new Roman"),row="all",col="all")


fig.add_shape(dict(type="line",x0=2.5,y0=1.5,x1=2.5,y1=6,line=dict(color="green", dash='dashdot',width=2)),row="all",col="all")
fig.add_shape(dict(type="line",x0=4,y0=1.5,x1=4,y1=6,line=dict(color="green",dash='dashdot',width=2)),row="all",col="all")

# Enhancing the plot
fig.update_xaxes(title_text="Time (in Mins)",range=(t1,t2),row=8,col=1)
fig.update_xaxes(title_text="Time (in Mins)",range=(t1,t2),row=8,col=2)
for i in range(1,9):
    fig.update_yaxes(title_text="average AE",range=(1.5,6),row=i,col=1)

fig.update_layout(
        title_text="Average AE for all subjects",
        template="simple_white",
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5,font=dict(size=40)),
        font_family="Times new Roman",font_color="black",font_size=25,height=1800,width=1500)
fig.update_annotations(font=dict(family="Times new Roman", size=30))

fig.for_each_xaxis(lambda x: x.update(gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))
fig.for_each_yaxis(lambda x: x.update(gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))

fig.show()
#fig.write_image("../images/FigSM2.png")
# fig.write_html("../images/FigSM2.html")
