
import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

data=pd.read_json("../data/all_mean_Swiss-Short.json",orient="records")
# Columns: file_ID	pat_id	sez_id	band	sez_length	no_of_elec	pre_mean	pre_sd	sez_mean	sez_sd	post_mean	post_sd

#Just adding ID in front of pat_id for labeling 
data['pat_id']=data['pat_id'].apply(lambda x: "ID"+str(x))



# Supplementary Figure 8

fig=make_subplots(rows=6,cols=1,shared_xaxes=True,vertical_spacing=0.02,subplot_titles=("Delta (δ)","Theta (θ)","Alpha (α)","Beta (β)","Lgamma (Lγ)","Hgamma (Hγ)"))


ms=10;dc=1.5;

s=data.query('band == "delta"')
fig.add_trace(go.Box(
    x=s['pat_id'],
    y=s['sez_mean'] - s['pre_mean'],
    marker_color="rgb(139, 0, 0)",
    boxpoints="all",
    marker=dict(size=ms,color="black",opacity=0.5),
    pointpos=dc,
    boxmean=True),row=1,col=1)

s=data.query('band == "theta"')
fig.add_trace(go.Box(
    x=s['pat_id'],
    y=s['sez_mean'] - s['pre_mean'],
    marker_color="rgb(255, 69, 0)",
    boxpoints="all",
    marker=dict(size=ms,color="black",opacity=0.5),
    pointpos=dc,
    boxmean=True),row=2,col=1)

s=data.query('band == "alpha"')
fig.add_trace(go.Box(
    x=s['pat_id'],
    y=s['sez_mean'] - s['pre_mean'],
    marker_color="rgb(0, 205, 0)",
    boxpoints="all",
    marker=dict(size=ms,color="black",opacity=0.5),
    pointpos=dc,
    boxmean=True),row=3,col=1)

s=data.query('band == "beta"')
fig.add_trace(go.Box(
    x=s['pat_id'],
    y=s['sez_mean'] - s['pre_mean'],
    marker_color="rgb(0, 206, 209)",
    boxpoints="all",
    marker=dict(size=ms,color="black",opacity=0.5),
    pointpos=dc,
    boxmean=True),row=4,col=1)

s=data.query('band == "lgamma"')
fig.add_trace(go.Box(
    x=s['pat_id'],
    y=s['sez_mean'] - s['pre_mean'],
    marker_color="rgb(105, 89, 205)",
    boxpoints="all",
    marker=dict(size=ms,color="black",opacity=0.5),
    pointpos=dc,
    boxmean=True),row=5,col=1)

s=data.query('band == "hgamma"')
fig.add_trace(go.Box(
    x=s['pat_id'],
    y=s['sez_mean'] - s['pre_mean'],
    marker_color="rgb(238, 122, 233)",
    boxpoints="all",
    marker=dict(size=ms,color="black",opacity=0.5),
    pointpos=dc,
    boxmean=True),row=6,col=1)


fig.for_each_xaxis(lambda x: x.update(gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))
fig.for_each_yaxis(lambda x: x.update(title_text="Sez. eff.",zeroline=True,zerolinecolor="rgba(0,0,0,0.4)",gridwidth=2,showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True))

fig.update_xaxes(title_text="Patient ID",tickfont=dict(size=30),row=6,col=1)

fon_sz=30;
fig.update_layout(
    title_text="Seizure effect in different frequency bands",showlegend=False,
    template="plotly_white",
    font_family="Times new Roman",font_color="black",font_size=fon_sz,height=2200,width=1500)
fig.update_annotations(font=dict(family="Times new Roman", size=30))
        
fig.show()
#fig.write_image("../images/FigSM13.png")  


