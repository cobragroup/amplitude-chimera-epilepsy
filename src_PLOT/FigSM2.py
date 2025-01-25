
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  

import warnings
warnings.filterwarnings("ignore")
#to supress RuntimeWarning: Mean of empty slice


#Creating folder for the SM9 figures
import os
if not os.path.exists('../images/figSM3'):
   os.makedirs('../images/figSM3')
   
   
#Global variables
sampling_rate=512;
bin_size=10;
#Time-points to show in SM6
st=2.5;ut=4; #This should match the values generated in "unfiltered_data_gen.py"
        
#data_load_path="../../Code_4/data/"
data_load_path="../../Code_5_sci_rep_review_1_test/data/"

##SUP Figure - 6
outp=pd.read_json(data_load_path+"all_unfiltered_electrode_data_Swiss-Short_"+str(st)+"_"+str(ut)+"_bin"+str(bin_size)+".json",orient="records")
#Columns: pat_ID - elec_no - X_t1 - X_t2 - ampen_t1 - ampen_t2 - elecs_t1 - elecs_t2    

# The plot

for pid in range(1,17):
    s=outp.query('pat_id=="ID'+str(pid)+'"')[['ampen_t1','elecs_t1','X_t1','X_t2','ampen_t2','elecs_t2']]
    # #replacing 0s with np.nan
    # s['elecs_t1'] = s['elecs_t1'].apply(lambda x: [np.nan if val==0.0 else val for val in x])
    # #replacing 0s with np.nan
    # s['elecs_t2'] = s['elecs_t2'].apply(lambda x: [np.nan if val==0.0 else val for val in x])
    # #Not bothering with X_t1,X_t2 and ampen_t1,ampen_t2 as they are same and don't have 0s

    y1m = np.mean(np.array(s['elecs_t1'].tolist()),axis=0)
    x1m = np.mean(np.array(s['X_t1'].tolist()),axis=0)
    
    if (pid not in [7,10]): #ID7 and ID10 don't have T2 in Seizure
        y2m = np.mean(np.array(s['elecs_t2'].tolist()),axis=0)
        x2m = np.mean(np.array(s['X_t2'].tolist()),axis=0)

    widx=5
    ##### Plotting with zero counts an normal mean
    f,ax=plt.subplots(figsize=(20,10))
    ax.bar(range(len(x1m)),np.array(y1m)*100,width=widx,alpha=0.5,color='red',label="T1="+str(st)+"min")

    if (pid not in [7,10]):#ID7 and ID10 don't have T2 in Seizure
        ax.bar(np.array(range(len(x2m)))+widx+1,np.array(y2m)*100,width=widx,alpha=0.5,color='blue',label="T2="+str(ut)+"min")
        
    ax.set_title("ID"+str(pid),fontsize=20)
    ax.set_xlim(0,650)
    ax.set_ylabel("Channels per bin (in %)",fontsize=40)
    ax.set_xlabel("Bin Index",fontsize=40)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.legend(fontsize="60")
    ax.grid()

    if pid not in [7,10]:#ID7 and ID10 don't have T2 in Seizure
        textstr = '\n'.join((
            r'$\mathrm{AE_{T1}}=%.2f$' % (s['ampen_t1'].mean()),
            r'$\mathrm{AE_{T2}}=%.2f$' % (s['ampen_t2'].mean())))
        # place a text box in upper left in axes coords
        ax.text(0.7, 0.45, textstr, transform=ax.transAxes, fontsize=50,verticalalignment='top')
    else:
        textstr = '\n'.join((
            r'$\mathrm{AE_{T1}}=%.2f$' % (s['ampen_t1'].mean()),
            ))
        # place a text box in upper left in axes coords
        ax.text(0.7, 0.45, textstr, transform=ax.transAxes, fontsize=50,verticalalignment='top')
  
    f.tight_layout()
    f.savefig("../images/figSM3/FigSM3_ID"+str(pid)+".png")
    plt.close(f)