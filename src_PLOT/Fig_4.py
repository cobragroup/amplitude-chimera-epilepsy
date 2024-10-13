
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore")
#to supress RuntimeWarning: Mean of empty slice
#This is because, we are taking mean across all patients, and some patients don't have data for some time points
#Thus, the mean of those time points across all patients will be NaN, which is not an error


import plotly.graph_objects as go
from plotly.subplots import make_subplots

data=pd.read_json("../data/all_mean_Swiss-Short.json",orient="records")
# Columns: file_ID	pat_id	sez_id	band	sez_length	no_of_elec	pre_mean	pre_sd	sez_mean	sez_sd	post_mean	post_sd

#Just adding ID in front of pat_id for labeling 
data['pat_id']=data['pat_id'].apply(lambda x: "ID"+str(x))

def mappi(fig,df,band_name,color_rgba):
    fig.add_trace(go.Box(
    y=df['pat_id'],
    x=df['sez_mean'] - df['pre_mean'],
    name=band_name,
    marker_color=color_rgba,
    boxpoints="all",
    marker=dict(size=7,color="black",opacity=0.5),
    pointpos=0,
    boxmean=True,
    orientation="v"
    jitter=0.1,  # add some jitter on points for better visibility
    ))
    return fig

fig=go.Figure()

mappi(fig,data.query('band == "delta"'),"δ", "rgb(139, 0, 0)")
mappi(fig,data.query('band == "theta"'),"θ", "rgb(255, 69, 0)")
mappi(fig,data.query('band == "alpha"'),"α", "rgb(0, 205, 0)")
mappi(fig,data.query('band == "beta"'),"β", "rgb(0, 206, 209)")
mappi(fig,data.query('band == "lgamma"'),"Lγ", "rgb(105, 89, 205)")
mappi(fig,data.query('band == "hgamma"'),"Hγ", "rgb(238, 122, 233)")

fig.update_layout(boxmode='group',width=2500,height=1400,
    xaxis=dict(
        showgrid=False,
        # autorange="reversed",
        showticklabels=True,
        gridcolor="rgb(235,235,235)",
        tickfont=dict(size=40)
    ),
    yaxis=dict(
        zeroline=True,
        zerolinecolor="black",
        title=dict(
            text="Seizure Effect (seizure - pre-seizure)",
            font=dict(size=40)
        ),
        tickfont=dict(size=40),
        gridcolor="rgb(235,235,235)"
    )
)

## Adding X and Y axis lines
fig.add_shape(dict(type="line", xref="paper", yref="paper",
                   x0=0.001, x1=0.001, y0=0, y1=1,line=dict(color='rgba(0,0,0,1)', width=1)))
fig.add_shape(dict(type="line", xref="paper", yref="paper",
                   x0=0, x1=16, y0=0, y1=0,line=dict(color='rgba(0,0,0,1)', width=1)))

#Update layout for better visualization
fig.update_layout(
        legend=dict(orientation="h",yanchor="top",y=0.99,xanchor="center",x=0.5,font=dict(color="blue",size=60)),
        template="plotly_white",
        font_family="Times new Roman",font_color="black",font_size=20)

fig.show()
#fig.write_image("../images/Fig4.png")
#fig.write_html("../images/Fig4.html")
