
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
#Time-slice to show in SM6
t1=0;t2=22;
#Time-points to show in SM6
st=2.5;ut=4; #This should match the values generated in "unfiltered_data_gen.py"
        
data_load_path="../../Code_5_sci_rep_review_1_test/data/"

##SUP Figure - 6
df=pd.read_json(data_load_path+"all_unfiltered_mean_AE_Swiss-Short_normed_time_b10.json",orient="records")
#Columns: pat_ID - elec_no - mean_AE - std_AE

# The plot
no_of_timepoints=len(df['mean_AE'][0])
time=np.arange(0,no_of_timepoints)/(60*sampling_rate) #in minutes

#replacing None with np.nan
df['mean_AE'] = df['mean_AE'].apply(lambda x: [np.nan if val is None else val for val in x])
df['std_AE'] = df['std_AE'].apply(lambda x: [np.nan if val is None else val for val in x])

#Calculating NaNmean and NaNstd across all patients
mean_AE= np.nanmean(np.array(df['mean_AE'].tolist()),axis=0)
std_AE = np.nanstd(np.array(df['std_AE'].tolist()),axis=0,ddof=1)

#std_AE = np.where(np.isnan(std_AE),0.0000001, std_AE) # replacing np.nan with 0.0000001
#std_AE = np.where(std_AE==0.0,0.0000001, std_AE) # replacing 0.0 with 0.0000001

#Taking a Splice of the data between t1 and t2  
#time=time[(t1*60*sampling_rate):(t2*60*sampling_rate)]
#mean_AE=mean_AE[(t1*60*sampling_rate):(t2*60*sampling_rate)]
#std_AE=std_AE[(t1*60*sampling_rate):(t2*60*sampling_rate)]

fig=go.Figure()

fig.add_trace(go.Scatter(x=time,y=mean_AE,mode='lines',
                        line=dict(color='rgb(31, 119, 180)'),
                        showlegend=False))

# fig.add_trace(go.Scatter(x=time,y=mean_AE+std_AE,mode='lines',
#                          marker=dict(color="#444"),line=dict(width=0),showlegend=False))

# fig.add_trace(go.Scatter(x=time,y=mean_AE-std_AE,mode='lines',
#                          marker=dict(color="#444"),line=dict(width=0),
#                          fillcolor='rgba(68, 68, 68, 0.3)',fill='tonexty',showlegend=False))


fig.update_yaxes(title_text="average AE",range=(2.8,5))
fig.update_xaxes(title_text="Time (in Mins)")

#fig.add_shape(dict(type="line",x0=3,y0=2.8,x1=3,y1=5,line=dict(color="red", width=3)))
fig.add_shape(dict(type="line",x0=st,y0=2.8,x1=st,y1=5,line=dict(color="black", dash='dashdot',width=2)))
fig.add_shape(dict(type="line",x0=ut,y0=2.8,x1=ut,y1=5,line=dict(color="black", dash='dashdot',width=2)))

# Adding vertical lines to show the T1 and T2 and seizure onset 
## Onset of Seizure
fig.add_shape(dict(type="line",x0=3,y0=1.5,x1=3,y1=6,line=dict(color="red", width=3)))
fig.add_annotation(dict(text="seizure onset",xref='x',yref='y',
        x=3.18,y=5.7,showarrow=False),font=dict(size=10, color="red",family="Times new Roman"))


## offset of Seizure ## Seizure lasts for 1005 seconds () and starts at 3 mins
fig.add_shape(dict(type="line",x0=(3+(1005/60)),y0=1.5,x1=(3+(1005/60)),y1=6,line=dict(color="red", width=3)))
fig.add_annotation(dict(text="seizure offset",xref='x',yref='y',
        x=19.18,y=5.7,showarrow=False),font=dict(size=10, color="red",family="Times new Roman"))




fig.update_layout(
        title_text="Average AE (averaged over subjects)",
        template="simple_white",
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5,font=dict(size=40)),
        font_family="Times new Roman",font_color="black",font_size=25,height=600,width=1500)

fig.for_each_xaxis(lambda x: x.update(showgrid=True))
fig.for_each_yaxis(lambda x: x.update(showgrid=True))

#fig.show()
fig.write_image("../images/FigSM4a_time_normed.png")
# fig.write_html("../images/FigSM4.html")

