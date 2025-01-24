
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
t1=2;t2=5;
#Time-points to show in SM6
st=2.5;ut=4; #This should match the values generated in "unfiltered_data_gen.py"
        
        
data_load_path="../../Code_4/data/"

##SUP Figure - 6
df=pd.read_json(data_load_path+"all_unfiltered_mean_AE_Swiss-Short.json",orient="records")
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

fig.add_shape(dict(type="line",x0=3,y0=2.8,x1=3,y1=5,line=dict(color="red", width=3)))

# fig.add_annotation(dict(text="seizure onset",xref='x',yref='y',
#         x=3.18,y=4.8,showarrow=False),font=dict(size=30, color="red",family="Times new Roman"))



fig.add_shape(dict(type="line",x0=st,y0=2.8,x1=st,y1=5,line=dict(color="black", dash='dashdot',width=2)))
fig.add_shape(dict(type="line",x0=ut,y0=2.8,x1=ut,y1=5,line=dict(color="black", dash='dashdot',width=2)))

fig.update_layout(
        title_text="Average AE (averaged over subjects)",
        template="simple_white",
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5,font=dict(size=40)),
        font_family="Times new Roman",font_color="black",font_size=25,height=600,width=1500)

fig.for_each_xaxis(lambda x: x.update(showgrid=True))
fig.for_each_yaxis(lambda x: x.update(showgrid=True))

#fig.show()
fig.write_image("../images/FigSM4a.png")
# fig.write_html("../images/FigSM4.html")


#Plotting the same figure ignoring the largest seizure of ID14 
#Taking only a seizure slice of 4 min or 240 seconds, which is the largest seizure length and averaging over them
largest_seizure_length=240
out=pd.read_json(data_load_path+"all_unfiltered_data_AE_Swiss-Short.json",orient="records")
# Mean patient AEs with time (which is averaged over seizures per patient)
def nans(pid,considered_window_after_seizure):
    ss=[]
    for s in out.query('pat_id=="ID'+str(pid)+'"')[['sez_len','AE']].iterrows():
        tmp=s[1]['AE']
        lng=s[1]['sez_len']
        no_datapoints = len(tmp)
        rg=tmp[(3*60*sampling_rate) : (no_datapoints - (3*60*sampling_rate))] #Seizure Segment
        if (len(rg)/sampling_rate)== lng:
            # vstacking to make all the segments of same length
            #first 3 mins of pre seizure  #seziure segment # np.nan of a length #last 3 mins of post seizure
            #largest seizure is 1002 secs so making all seziure segments as 1005 secs with np.nan padding
            new_rg=np.hstack((rg,np.full(shape=((1005*sampling_rate) - len(rg)), fill_value=np.nan)))
            #To remove the largest seizure of ID14
            #stacking whole pre-seizure segment, seizure segment (of length considered_window_after_seizure in s) and post-seizure segment 
            new_aa=np.hstack((tmp[:(3*60*sampling_rate)],new_rg[:(considered_window_after_seizure*sampling_rate)],tmp[(no_datapoints - (3*60*sampling_rate)):]))
            
            ss.append(new_aa)
    return np.nanmean(np.array(ss),axis=0),np.nanstd(np.array(ss),axis=0,ddof=1) 

output={'pat_ID':[],'elec_no':[],'mean_AE':[],'std_AE':[]}

for i in range(1,17):
    output['pat_ID'].append("ID"+str(i))
    output['elec_no'].append(out.query('pat_id=="ID'+str(i)+'"')['elec_no'].unique()[0])
    a,b=nans(i,largest_seizure_length)
    output['mean_AE'].append(a)
    output['std_AE'].append(b)

df=pd.DataFrame.from_dict(output)


# The plot
no_of_timepoints=len(df['mean_AE'][0])

time=np.hstack((
    np.arange(0,(3*60*sampling_rate))/(60*sampling_rate), #First 3 mins Pre-Seizure
    #Seizure Segment of largest_seizure_length
    ((180*sampling_rate)+np.arange(0,(largest_seizure_length*sampling_rate)))/(60*sampling_rate), 
    np.arange((no_of_timepoints -(3*60*sampling_rate)),no_of_timepoints)/(60*sampling_rate) #Last 3 mins Post-Seizure
           ))

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

fig.add_shape(dict(type="line",x0=3,y0=2.8,x1=3,y1=5,line=dict(color="red", width=3)))

# fig.add_annotation(dict(text="seizure onset",xref='x',yref='y',
#         x=3.18,y=4.8,showarrow=False),font=dict(size=30, color="red",family="Times new Roman"))


fig.add_shape(dict(type="line",x0=st,y0=2.8,x1=st,y1=5,line=dict(color="black", dash='dashdot',width=2)))
fig.add_shape(dict(type="line",x0=ut,y0=2.8,x1=ut,y1=5,line=dict(color="black", dash='dashdot',width=2)))

fig.update_layout(
        title_text="Average AE (averaged over subjects)",
        template="simple_white",
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5,font=dict(size=40)),
        font_family="Times new Roman",font_color="black",font_size=25,height=600,width=1500)

fig.for_each_xaxis(lambda x: x.update(showgrid=True))
fig.for_each_yaxis(lambda x: x.update(showgrid=True))

#fig.show()
fig.write_image("../images/FigSM4b.png")

print("Images generated successfully and saved in images folder as SM4a and SM4b.png")