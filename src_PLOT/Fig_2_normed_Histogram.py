
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
pid=2; ## Patient ID = ID2
sz=3; ## Seizure ID = s3

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

## Normalization of AE, For One Patient and One Seizure
print(np.sum(outp.query('fileID=="p'+str(pid)+'s'+str(sz)+'"').elecs_t1.values[0]))
## Normalization of AE, For One Patient
print(np.nansum(np.array(
        outp.query('pat_id=="ID'+str(pid)+'"')['elecs_t1'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).to_list())
                ,axis=1))



# # The 2-A,B plot
# output={'pat_ID':[],'elec_no':[],'X_t1':[],'X_t2':[],'elecs_t1':[],'elecs_t2':[],'ampen_t1':[],'ampen_t2':[]}
# for pid in range(1,17): # 16 patients
#     s=outp.query('pat_id=="ID'+str(pid)+'"')[['ampen_t1','elecs_t1','X_t1','X_t2','ampen_t2','elecs_t2']];
    
#     #replacing 0s with np.nan
#     s['elecs_t1'] = s['elecs_t1'].apply(lambda x: [np.nan if val==0.0 else val for val in x])
#     #replacing 0s with np.nan
#     s['elecs_t2'] = s['elecs_t2'].apply(lambda x: [np.nan if val==0.0 else val for val in x])
#     #Not bothering with X_t1,X_t2 and ampen_t1,ampen_t2 as they are same and don't have 0s

#     output['pat_ID'].append("ID"+str(pid))
#     output['elec_no'].append(outp.query('pat_id=="ID'+str(pid)+'"')['elec_no'].unique()[0])
    
#     output['X_t1'].append(np.nanmean(np.array(s['X_t1'].tolist()),axis=0))
#     output['X_t2'].append(np.nanmean(np.array(s['X_t2'].tolist()),axis=0))
  
#     output['elecs_t1'].append(np.nanmean(np.array(s['elecs_t1'].tolist()),axis=0))
#     output['elecs_t2'].append(np.nanmean(np.array(s['elecs_t2'].tolist()),axis=0))
    
#     output['ampen_t1'].append(s['ampen_t1'].mean())
#     output['ampen_t2'].append(s['ampen_t2'].mean())

# outS=pd.DataFrame.from_dict(output)


y1ms=np.array(outp.query('pat_id=="ID'+str(pid)+'"')['elecs_t1'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).to_list())

x1ms=np.array(outp.query('pat_id=="ID'+str(pid)+'"')['X_t1'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).to_list())

y2ms=np.array(outp.query('pat_id=="ID'+str(pid)+'"')['elecs_t2'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).to_list())

x2ms=np.array(outp.query('pat_id=="ID'+str(pid)+'"')['X_t2'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).to_list())



#Taking NaN mean acroos all patients
y1m = np.nanmean(np.array(outp.query('pat_id=="ID'+str(pid)+'"')['elecs_t1'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).tolist()),axis=0)
x1m = np.nanmean(np.array(outp.query('pat_id=="ID'+str(pid)+'"')['X_t1'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).tolist()),axis=0)
y2m = np.nanmean(np.array(outp.query('pat_id=="ID'+str(pid)+'"')['elecs_t2'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).tolist()),axis=0)
x2m = np.nanmean(np.array(outp.query('pat_id=="ID'+str(pid)+'"')['X_t2'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).tolist()),axis=0)

# Not Normalised
print("T1:", np.nansum(np.array(outp.query('pat_id=="ID'+str(pid)+'"')['elecs_t1'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).tolist())))
print("T2:", np.nansum(np.array(outp.query('pat_id=="ID'+str(pid)+'"')['elecs_t2'].apply(lambda x: [np.nan if val==0.0 else val for val in x]).tolist())))

#print(np.max(x2ms[0,:]),np.max(x2ms[1,:]),np.max(x2ms[2,:]),np.max(x2ms[3,:]),np.max(x2m))

print(np.max(x1ms[0,:][y1ms[0,:]>0]),np.max(x1ms[1,:][y1ms[1,:]>0]),np.max(x1ms[2,:][y1ms[2,:]>0]),np.max(x1ms[3,:][y1ms[3,:]>0]),np.max(x1m[y1m>0]))


print(np.max(x2ms[0,:][y2ms[0,:]>0]),np.max(x2ms[1,:][y2ms[1,:]>0]),np.max(x2ms[2,:][y2ms[2,:]>0]),np.max(x2ms[3,:][y2ms[3,:]>0]),np.max(x2m[y2m>0]))

print(x2ms[3,:][y2ms[3,:]>0],y2ms[3,:][y2ms[3,:]>0]*100)

## Making Fig 2
fig = make_subplots(
    rows=5, cols=2,shared_yaxes='all',vertical_spacing=0.025,horizontal_spacing=0.005,
#     specs=[[{}, {}],
#            [{"colspan": 2}, None]],
    subplot_titles=("ID2S1 pre-seizure (T1)","ID2S1 seizure (T2)", 
                    "ID2S2 pre-seizure (T1)","ID2S2 seizure (T2)",
                    "ID2S3 pre-seizure (T1)","ID2S3 seizure (T2)",
                    "ID2S4 pre-seizure (T1)","ID2S4 seizure (T2)",
                    "ID2 (mean) pre-seizure (T1)","ID2 (mean) seizure (T2) Normalised"))

# Traces for 2-A,B
wd=5


rwx=1
#100 is multipled to show in percentage, original value in fraction 0-1 as it was a PMF
fig.add_trace(go.Bar(name='t1', x=np.arange(len(x1ms[rwx-1,:])), y=y1ms[rwx-1,:]*100,showlegend=False),row=rwx,col=1) 
fig.add_trace(go.Bar(name='t2', x=np.arange(len(x2ms[rwx-1,:])), y=y2ms[rwx-1,:]*100,showlegend=False),row=rwx,col=2)
fig.update_traces(width=wd,row=rwx)

rwx=2
#100 is multipled to show in percentage, original value in fraction 0-1 as it was a PMF
fig.add_trace(go.Bar(name='t1', x=np.arange(len(x1ms[rwx-1,:])), y=y1ms[rwx-1,:]*100,showlegend=False),row=rwx,col=1) 
fig.add_trace(go.Bar(name='t2', x=np.arange(len(x2ms[rwx-1,:])), y=y2ms[rwx-1,:]*100,showlegend=False),row=rwx,col=2)
fig.update_traces(width=wd,row=rwx)

rwx=3
#100 is multipled to show in percentage, original value in fraction 0-1 as it was a PMF
fig.add_trace(go.Bar(name='t1', x=np.arange(len(x1ms[rwx-1,:])), y=y1ms[rwx-1,:]*100,showlegend=False),row=rwx,col=1) 
fig.add_trace(go.Bar(name='t2', x=np.arange(len(x2ms[rwx-1,:])), y=y2ms[rwx-1,:]*100,showlegend=False),row=rwx,col=2)
fig.update_traces(width=wd,row=rwx)

rwx=4
#100 is multipled to show in percentage, original value in fraction 0-1 as it was a PMF
fig.add_trace(go.Bar(name='t1', x=np.arange(len(x1ms[rwx-1,:])), y=y1ms[rwx-1,:]*100,showlegend=False),row=rwx,col=1) 
fig.add_trace(go.Bar(name='t2', x=np.arange(len(x2ms[rwx-1,:])), y=y2ms[rwx-1,:]*100,showlegend=False),row=rwx,col=2)
fig.update_traces(width=wd,row=rwx)



rwx=5
#100 is multipled to show in percentage, original value in fraction 0-1 as it was a PMF
fig.add_trace(go.Bar(name='t1', x=np.arange(len(x1m)), y=y1m*100,showlegend=False),row=rwx,col=1) 
fig.add_trace(go.Bar(name='t2', x=np.arange(len(x2m)), y=y2m*100,showlegend=False),row=rwx,col=2)
fig.update_traces(width=wd,row=rwx)



# Update grid settings for x-axes in the bottom row
fig.for_each_xaxis(lambda x: x.update(
    gridwidth=2, showgrid=True, showline=True, linewidth=2, linecolor='black', mirror=True))

# Update grid settings for y-axes in the bottom row
fig.for_each_yaxis(lambda y: y.update(
    gridwidth=2, gridcolor="rgba(0,0,0,0.35)",showgrid=True, showline=True, linewidth=2, linecolor='black', mirror=True))


fig.update_layout(
        template="plotly_white",
        #legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5,font=dict(size=40)),
        font_family="Times new Roman",font_color="black",font_size=25,height=3000,width=1800)

#fig.update_traces(textposition='top right',row=2,col=1)
fig.update_annotations(font_size=30)

fig.show()
#fig.write_image("../images/Fig2.png")
# fig.write_html("../images/Fig2.html")

