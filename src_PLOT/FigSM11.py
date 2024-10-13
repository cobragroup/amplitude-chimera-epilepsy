
import numpy as np
import scipy.io

import os
import glob

## Mention the Data Path here for the RAW iEEG data 
data_path="/home/sapta/Documents/"
sampling_rate=512


import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import hilbert

# scaling between 0 and 1
scales= lambda signal: np.true_divide(( signal - np.amin(signal) ), (np.amax(signal)-np.amin(signal))) 

# Mention patient ID and seizure ID here
patid=2;sez_ID=3;

filename = os.path.join(data_path, "ID"+str(patid)+"/Sz"+str(sez_ID)+".mat")
mat=scipy.io.loadmat(filename)
data=np.array(mat.get('EEG'))

no_of_electrodes=np.shape(data)[1]
tme=np.arange(1,np.shape(data)[0]) / (sampling_rate*60) # time_window in Mins


fig=make_subplots(rows=4,cols=1,shared_xaxes=True,vertical_spacing=0.02,subplot_titles=("Channel 1","Channel 13","Channel 27", "Channel 39"))


ms=10;dc=1.5;

clr="rgb(0,100,0,0.5)";
wid=2;

fig.add_trace(go.Scatter(
    x=tme, y=scales(np.abs(hilbert(data[1:, 0]))),
    mode='lines',
    line=dict(width=wid,color=clr),
    ),row=1,col=1)

fig.add_trace(go.Scatter(
    x=tme, y=scales(np.abs(hilbert(data[1:, 12]))),
    mode='lines',
    line=dict(width=wid,color=clr),
    ),row=2,col=1)


fig.add_trace(go.Scatter(
    x=tme, y=scales(np.abs(hilbert(data[1:, 26]))),
    mode='lines',
    line=dict(width=wid,color=clr),
    ),row=3,col=1)

fig.add_trace(go.Scatter(
    x=tme, y=scales(np.abs(hilbert(data[1:, 38]))),
    mode='lines',
    line=dict(width=wid,color=clr),
    ),row=4,col=1)


fig.for_each_xaxis(lambda x: x.update(gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))
fig.for_each_yaxis(lambda x: x.update(title_text="AA (normalized)",zeroline=True,zerolinecolor="rgba(0,0,0,0.4)",gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))

fig.update_xaxes(title_text="Time (in Mins)",tickfont=dict(size=30),row=4,col=1)

fon_sz=30;
fig.update_layout(
    title_text="Local peak at onset in different Channels (Patient 2,Seizure 3)",showlegend=False,
    template="plotly_white",
    font_family="Times new Roman",font_color="black",font_size=fon_sz,height=2200,width=1500)
fig.update_annotations(font=dict(family="Times new Roman", size=30))
 
fig.show()       
#fig.write_image("../images/figSM11.png")


## Plot This for RAW amplitude Before Hilbert Transformation

# fig=make_subplots(rows=4,cols=1,shared_xaxes=True,vertical_spacing=0.02,subplot_titles=("Channel 1","Channel 13","Channel 27", "Channel 39"))


# ms=10;dc=1.5;

# clr="rgb(0,100,0,0.5)";
# wid=2;

# fig.add_trace(go.Scatter(
#     x=tme, y=data[1:, 0],
#     mode='lines',
#     line=dict(width=wid,color=clr),
#     ),row=1,col=1)

# fig.add_trace(go.Scatter(
#     x=tme, y=data[1:, 12],
#     mode='lines',
#     line=dict(width=wid,color=clr),
#     ),row=2,col=1)


# fig.add_trace(go.Scatter(
#     x=tme, y=data[1:, 26],
#     mode='lines',
#     line=dict(width=wid,color=clr),
#     ),row=3,col=1)

# fig.add_trace(go.Scatter(
#     x=tme, y=data[1:, 38],
#     mode='lines',
#     line=dict(width=wid,color=clr),
#     ),row=4,col=1)





# fig.for_each_xaxis(lambda x: x.update(gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))
# fig.for_each_yaxis(lambda x: x.update(title_text="Amplitude (im mV)",zeroline=True,zerolinecolor="rgba(0,0,0,0.4)",gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))

# fig.update_xaxes(title_text="Time (in Mins)",tickfont=dict(size=30),row=4,col=1)

# fon_sz=30;
# fig.update_layout(
#     title_text="Sezonset in different Channels (Patient 2,Seizure 3)",showlegend=False,
#     template="plotly_white",
#     font_family="Times new Roman",font_color="black",font_size=fon_sz,height=2200,width=1500)
# fig.update_annotations(font=dict(family="Times new Roman", size=30))
 
# fig.show()       
# # #fig.write_image("../images/figSM11.png")
