
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
bin_size=10;
#Time-slice (range of X axis, determinted by seizure lengths) to show in 2-C
t1=2;t2=5;
#Time-points to show in 2-A,B
st=2.5;ut=4; #This should match the values generated in "unfiltered_data_gen.py"
        
        
data_load_path="../../Code_4/data/"

##Main Figure - 2
##Needed Data Files: all_unfiltered_electrode_data_Swiss-Short_2.5_4.json,all_unfiltered_mean_AE_Swiss-Short.json
outp=pd.read_json(data_load_path+"all_unfiltered_electrode_data_Swiss-Short_"+str(st)+"_"+str(ut)+".json",orient="records")
#Columns: pat_ID - elec_no - X_t1 - X_t2 - ampen_t1 - ampen_t2 - elecs_t1 - elecs_t2    
df=pd.read_json(data_load_path+"all_unfiltered_mean_AE_Swiss-Short.json",orient="records")
#Columns: pat_ID - elec_no - mean_AE - std_AE

# The 2-C plot
no_of_timepoints=len(df['mean_AE'][0])
time=np.arange(0,no_of_timepoints)/(60*sampling_rate) #in minutes

#lambda function for replacing None with np.nan
df['mean_AE'] = df['mean_AE'].apply(lambda x: [np.nan if val is None else val for val in x])
df['std_AE'] = df['std_AE'].apply(lambda x: [np.nan if val is None else val for val in x])


#Calculating NaNmean(Over Patients) of NanMeans(Over Seizure) and NaNmean(Over Patients) of NaNstds(Over Seizure) across all patients
mean_AE= np.nanmean(np.array(df['mean_AE'].tolist()),axis=0)
#std_AE = np.nanstd(np.array(df['std_AE'].tolist()),axis=0,ddof=1)
std_AE = np.nanmean(np.array(df['std_AE'].tolist()),axis=0) # Taking mean of std across all patients
std_AE = np.where(np.isnan(std_AE),0.0, std_AE) # replacing np.nan with 0.0

#Taking a Splice of the data between t1 and t2  
time=time[(t1*60*sampling_rate):(t2*60*sampling_rate)] #in minutes
mean_AE=mean_AE[(t1*60*sampling_rate):(t2*60*sampling_rate)]
std_AE=std_AE[(t1*60*sampling_rate):(t2*60*sampling_rate)]


# The 2-A,B plot
output={'pat_ID':[],'elec_no':[],'X_t1':[],'X_t2':[],'elecs_t1':[],'elecs_t2':[],'ampen_t1':[],'ampen_t2':[]}
for pid in range(1,17): # 16 patients
    s=outp.query('pat_id=="ID'+str(pid)+'"')[['ampen_t1','elecs_t1','X_t1','X_t2','ampen_t2','elecs_t2']];
    
    #replacing 0s with np.nan
    s['elecs_t1'] = s['elecs_t1'].apply(lambda x: [np.nan if val==0.0 else val for val in x])
    #replacing 0s with np.nan
    s['elecs_t2'] = s['elecs_t2'].apply(lambda x: [np.nan if val==0.0 else val for val in x])
    #Not bothering with X_t1,X_t2 and ampen_t1,ampen_t2 as they are same and don't have 0s

    output['pat_ID'].append("ID"+str(pid))
    output['elec_no'].append(outp.query('pat_id=="ID'+str(pid)+'"')['elec_no'].unique()[0])
    
    output['X_t1'].append(np.nanmean(np.array(s['X_t1'].tolist()),axis=0))
    output['X_t2'].append(np.nanmean(np.array(s['X_t2'].tolist()),axis=0))
  
    output['elecs_t1'].append(np.nanmean(np.array(s['elecs_t1'].tolist()),axis=0))
    output['elecs_t2'].append(np.nanmean(np.array(s['elecs_t2'].tolist()),axis=0))
    
    output['ampen_t1'].append(s['ampen_t1'].mean())
    output['ampen_t2'].append(s['ampen_t2'].mean())

outS=pd.DataFrame.from_dict(output)

#Taking NaN mean acroos all patients
y1m = np.nanmean(np.array(outS['elecs_t1'].tolist()),axis=0)
x1m = np.nanmean(np.array(outS['X_t1'].tolist()),axis=0)
y2m = np.nanmean(np.array(outS['elecs_t2'].tolist()),axis=0)
x2m = np.nanmean(np.array(outS['X_t2'].tolist()),axis=0)


## Making Fig 2
fig = make_subplots(
    rows=2, cols=2,shared_yaxes='rows',shared_xaxes='rows',vertical_spacing=0.15,horizontal_spacing=0.05,
    specs=[[{}, {}],
           [{"colspan": 2}, None]],
    subplot_titles=("pre-seizure (T1)","seizure (T2)", ""))

# Traces for 2-A,B
# Just In case, if you want to match X axis of 2-A with 2-B
# fig.add_trace(go.Bar(name='t1', x=np.arange(len(x1m)), y=y1m*100,showlegend=False),row=1,col=1)
# fig.add_trace(go.Bar(name='t2', x=np.arange(len(x2m))[:len(x1m)], y=y2m[:len(x1m)]*100,showlegend=False),row=1,col=2)

#100 is multipled to show in percentage, original value in fraction 0-1 as it was a PMF
fig.add_trace(go.Bar(name='t1', x=np.arange(len(x1m)), y=y1m*100,showlegend=False),row=1,col=1) 
fig.add_trace(go.Bar(name='t2', x=np.arange(len(x2m)), y=y2m*100,showlegend=False),row=1,col=2)
fig.update_traces(width=2,row=1)

# Traces for 2-C
fig.add_trace(go.Scatter(x=time,y=mean_AE,mode='lines',
                        line=dict(color='blue'),
                        showlegend=False),row=2,col=1)

fig.add_trace(go.Scatter(x=time,y=mean_AE+std_AE,
        mode='lines',marker=dict(color="#444"),line=dict(width=0),showlegend=False),row=2,col=1)

fig.add_trace(go.Scatter(x=time,y=mean_AE-std_AE,
                         marker=dict(color="#444"),line=dict(width=0),mode='lines',
                         fillcolor='rgba(75,   0, 130, 0.3)',fill='tonexty',showlegend=False),row=2,col=1)
# Enhancing the plot
fig.update_yaxes(title_text="Channels per bin (in %)",range=(0,18),row=1,col=1)
fig.update_xaxes(title_text="Bin Index",range=(0,400),row=1,col=1) #Change here for X axis of 2-A,B
fig.update_xaxes(title_text="Bin Index",row=1,col=2)

fig.update_yaxes(title_text="average AE",range=(2.6,5),row=2,col=1) #Change here for Y axis of 2-C
fig.update_xaxes(title_text="Time (in Mins)",row=2,col=1)

# Adding vertical lines in 2-C for T1,T2 and seizure onset
fig.add_shape(dict(type="line",x0=3,y0=2.6,x1=3,y1=5,line=dict(color="red", width=3)),row=2,col=1)

fig.add_shape(dict(type="line",x0=2.5,y0=2.6,x1=2.5,y1=5,line=dict(color="black", dash='dashdot',width=1.5)),row=2,col=1)
fig.add_shape(dict(type="line",x0=4,y0=2.6,x1=4,y1=5,line=dict(color="black", dash='dashdot',width=1.5)),row=2,col=1)

# Adding annotations for Mean AE from 2-C to 2-A,B
fig.add_annotation(dict(text="mean AE "+str(np.round(mean_AE[time==st][0],decimals=2)),xref='x',yref='y',
                x=116,y=16,showarrow=False),
                font=dict(size=30, color="black",family="Times new Roman"),
                row=1, col=1)
fig.add_annotation(dict(text="mean AE "+str(np.round(mean_AE[time==ut][0],decimals=2)),xref='x',yref='y',
                x=116,y=16,showarrow=False),
                font=dict(size=30, color="black",family="Times new Roman"),
                row=1, col=2)

# Enhancing the plot
fig.add_annotation(dict(text="T1",xref='x',yref='y',
        x=2.46,y=4.85,showarrow=False),font=dict(size=30, color="black",family="Times new Roman"),
        row=2, col=1)

fig.add_annotation(dict(text="T2",xref='x',yref='y',
        x=4.06,y=2.9,showarrow=False),font=dict(size=30, color="black",family="Times new Roman"),
        row=2, col=1)

fig.add_annotation(dict(text="seizure onset",xref='x',yref='y',
        x=3.18,y=4.85,showarrow=False),font=dict(size=30, color="red",family="Times new Roman"),
        row=2, col=1)

fig.update_layout(
        template="plotly_white",
        #legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5,font=dict(size=40)),
        font_family="Times new Roman",font_color="black",font_size=25,height=1000,width=1800)

fig.update_traces(textposition='top right',row=2,col=1)
fig.update_annotations(font_size=30)

# Update grid settings for x-axes in the bottom row
fig.for_each_xaxis(lambda x: x.update(
    gridwidth=2, showgrid=True, showline=True, linewidth=2, linecolor='black', mirror=True))

# Update grid settings for y-axes in the bottom row
fig.for_each_yaxis(lambda y: y.update(
    gridwidth=2, gridcolor="rgba(0,0,0,0.35)",showgrid=True, showline=True, linewidth=2, linecolor='black', mirror=True))


fig.show()
fig.write_image("../images/Fig2_400.png")
# fig.write_html("../images/Fig2.html")

