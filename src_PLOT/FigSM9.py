
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  

#Creating folder for the SM9 figures
import os
if not os.path.exists('../images/figSM9'):
   os.makedirs('../images/figSM9')
   
   
#Global variables
sampling_rate=512;
bin_size=10;
#Time-points to show in SM6
st=2.5;ut=4; #This should match the values generated in "unfiltered_data_gen.py"
        
##SUP Figure - 6
outp=pd.read_json("../data/all_unfiltered_electrode_data_Swiss-Short_"+str(st)+"_"+str(ut)+".json",orient="records")
#Columns: pat_ID - elec_no - X_t1 - X_t2 - ampen_t1 - ampen_t2 - elecs_t1 - elecs_t2    

# The 9 plot

for pid in range(1,17):
    s=outp.query('pat_id=="ID'+str(pid)+'"')[['ampen_t1','elecs_t1','X_t1','X_t2','ampen_t2','elecs_t2']]
    #replacing 0s with np.nan
    s['elecs_t1'] = s['elecs_t1'].apply(lambda x: [np.nan if val==0.0 else val for val in x])
    #replacing 0s with np.nan
    s['elecs_t2'] = s['elecs_t2'].apply(lambda x: [np.nan if val==0.0 else val for val in x])
    #Not bothering with X_t1,X_t2 and ampen_t1,ampen_t2 as they are same and don't have 0s

    y1m = np.nanmean(np.array(s['elecs_t1'].tolist()),axis=0)
    x1m = np.nanmean(np.array(s['X_t1'].tolist()),axis=0)
    y2m = np.nanmean(np.array(s['elecs_t2'].tolist()),axis=0)
    x2m = np.nanmean(np.array(s['X_t2'].tolist()),axis=0)
    
    f,ax=plt.subplots(figsize=(20,10))
    ax.bar(x1m[~np.isnan(y1m)],y1m[~np.isnan(y1m)],width=3,color='red',label="T1="+str(st)+"min")
    ax.bar(x2m[~np.isnan(y2m)]+4,y2m[~np.isnan(y2m)],width=3,color='blue',label="T2="+str(ut)+"min")
    ax.set_title("ID"+str(pid),fontsize=20)
    
    ax.set_ylabel("Channels per bin (in fraction)",fontsize=40)
    ax.set_xlabel("Bin Index",fontsize=40)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.legend(fontsize="60")
    ax.grid()
    textstr = '\n'.join((
        r'$\mathrm{AE_{T1}}=%.2f$' % (s['ampen_t1'].mean()),
        r'$\mathrm{AE_{T2}}=%.2f$' % (s['ampen_t2'].mean())))
    # place a text box in upper left in axes coords
    ax.text(0.7, 0.45, textstr, transform=ax.transAxes, fontsize=50,verticalalignment='top')
    
    f.tight_layout()
    f.savefig("../images/figSM9/FigSM9_ID"+str(pid)+".png")
    plt.close(f)