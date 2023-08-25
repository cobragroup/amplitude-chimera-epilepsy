# %%
import numpy as np
import scipy.io
import matplotlib.pyplot as plt

# %%
import sys

# Get frequency and amplitude from command line arguments
if len(sys.argv) < 3:
    print("Usage: python Sez_plot.py <pat_id> <sz_id>")
    sys.exit(1)

try:
    pat_id = int(sys.argv[1])
    sz_id = int(sys.argv[2])
except ValueError:
    print("Invalid input. Patient ID and Seizure ID must be numeric values.")
    sys.exit(1)


#pat_id=2;sz_id=3;

dname="ID"+str(pat_id)+"/Sz"+str(sz_id)+".mat"
mat=scipy.io.loadmat(dname)
data=np.array(mat.get('EEG'))

# %%
no_of_electrodes=np.shape(data)[1]
sampling_rate=512

tme=np.arange(1,np.shape(data)[0]) / (sampling_rate*60) # time_window in Mins


# %%

#########  Plotting the data  using Matplotlib #########

fig, ax = plt.subplots(figsize=(15, 15))
ax.set_title("Actual Signal ID" + str(pat_id) + "Sz" + str(sz_id))

colors = plt.get_cmap('tab10').colors  # Get the colors from the tab10 colormap
num_colors = len(colors)
for c in range(no_of_electrodes):
    color = colors[c % num_colors]  # Cycle through the available colors
    ax.plot(tme, data[1:, c] + (c * 1000), color=color, lw=0.5)
ax.set_yticks(range(0, no_of_electrodes * 1000, 1000))
ax.set_yticklabels(range(1, no_of_electrodes + 1))
ax.set_xlabel('Time (Mins)')
ax.set_ylabel('Channel Number')
ax.axvline(3, color='red', linestyle='--')

ax.grid(True)  # Add a grid

plt.show()


#########  Plotting the data  using Plotly Express #########
'''
import plotly.graph_objects as go

fig = go.Figure()

for c in range(no_of_electrodes):
    fig.add_trace(go.Scattergl(x=tme, y=data[:, c] + (c * 1000), mode='lines', line=dict(width=0.5)))
    #fig.add_annotation(x=tme[0], y=c * 1000, text=f"Channel {c+1}", showarrow=False, xshift=-10, yshift=10)
    #Just remove extra annotations; But you can assign other useful text here
fig.add_vline(x=3.0)
fig.update_layout(
    title="Actual Signal ID" + str(pat_id) + "Sz" + str(sz_id),
    xaxis_title="Time (Mins)",
    yaxis_title="Channel Number",
    hovermode='x',
    showlegend=False,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ),
    yaxis=dict(
        tickmode='array',
        tickvals=list(range(0, no_of_electrodes * 1000, 1000)),
        ticktext=list(range(1, no_of_electrodes + 1))
    )
)
fig.update_shapes(dict(xref='x', yref='y'))

fig.show()
'''
