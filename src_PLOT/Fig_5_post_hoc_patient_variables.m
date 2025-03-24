clear all; close all; clc;

%% Change the path accordingly
data_path = 'data/';

data = struct2table(jsondecode(fileread(fullfile(data_path, 'all_mean_Swiss-Short.json'))));
pat_info = tdfread(fullfile(data_path, 'Swiss Short Seizure Meta-Data - Sez_Meta.tsv'), 'tab');

freqs=unique(data(:,4));
n_patients=16;
n_seizures=100;
seizures=unique(data(:,1));


%% select data 

% by frequency bands
for f=1:size(freqs,1)
    cond1=contains(data.band,freqs{f,:});
    freq_data.(freqs{f,:}{:})=table2struct(data(cond1,:));
end
clear f cond1

% by seizures
for s=1:n_seizures
    cond2=strcmp(data.file_ID,seizures{s,:});
    seiz_data.(seizures{s,:}{:})=table2struct(data(cond2,:));
end
clear s cond2

% by patients
for p=1:n_patients
    patID=['p',num2str(p)];
    
    cond3=ismember(data.pat_id,p);
    pat_data.(patID)=table2struct(data(cond3,:));
        
    %by patient AND frequency
    for f=1:size(freqs,1)
        cond1=contains(data.band,freqs{f,:});
        pat_freq_data.(patID).(freqs{f,:}{:})=table2struct(data(...
            and(cond1,cond3),:));
    end
    clear f
    
    %by patient AND seizure, averaged across frequency for each seizure
    cond4=~contains(seizures{:,:},[patID,'s']);
    pat_seiz_data.(patID)=rmfield(seiz_data,seizures{cond4,:});
    
end
clear patID p cond3 cond4


%% seizure effect: ( AE seiz - AE preseiz )

seiz_effect = data.sez_mean - data.pre_mean;

%by freq
for f=1:size(freqs,1)
    seiz_effect_freq(f,:) = [freq_data.(freqs{f,:}{:}).sez_mean]' - [freq_data.(freqs{f,:}{:}).pre_mean]';
end
clear f 

%by seiz
for s=1:n_seizures
    seiz_effect_seiz(s,:) = [seiz_data.(seizures{s,:}{:}).sez_mean]' - [seiz_data.(seizures{s,:}{:}).pre_mean]';
end
clear s

% by patient
for p=1:n_patients
    patID=['p',num2str(p)];

    seiz_effect_pat(p,:) = mean([pat_data.(patID).sez_mean]' - [pat_data.(patID).pre_mean]');
        
    %by patient AND seiz, with averaged freq
    sz=fieldnames(pat_seiz_data.(patID));
    for s=1:length(sz)
        seiz_effect_pat_seiz(p,s,:) = mean([pat_seiz_data.(patID).(sz{s}).sez_mean]'...
            - [pat_seiz_data.(patID).(sz{s}).pre_mean]');
        seiz_len_pat_seiz(p,s,:)=pat_seiz_data.(patID).(sz{s}).sez_length;
    end
    seiz_effect_pat_seiz(seiz_effect_pat_seiz==0)=NaN;
    
    %by patient AND frequency
    for f=1:size(freqs,1)
        seiz_effect_pat_freq(p,f,1:s)=[pat_freq_data.(patID).(freqs{f,:}{:}).sez_mean]' ...
            - [pat_freq_data.(patID).(freqs{f,:}{:}).pre_mean]';
    end   
    clear f sz s
    seiz_effect_pat_freq(seiz_effect_pat_freq==0)=NaN;

    
end
clear p 


%% correlate seizure effect per patient with clinical variables
pat_sel=1:n_patients; %info table with clinical vars has additional rows


%% age
disp('age')

figure
[r,p] = corr(pat_info.Age(pat_sel),seiz_effect_pat,'Type', 'Spearman');
scatter(pat_info.Age(pat_sel),seiz_effect_pat,80,'filled'); 
title(['Spearman r = ',num2str(r),', p = ',num2str(p)]);
xlabel('age (years)'); ylabel('AE seizure effect ( seiz - pre )');


%% number of electrodes 
disp('# electrodes')

figure;
[r,p] = corr(pat_info.No_of_Electrodes(pat_sel),seiz_effect_pat,'Type', 'Spearman');
scatter(pat_info.No_of_Electrodes(pat_sel),seiz_effect_pat,80,'filled'); 
title(['Spearman r = ',num2str(r),', p = ',num2str(p)]);
xlabel('# electrodes'); ylabel('AE seizure effect ( seiz - pre )');


%% epilepsy lobe & MRI_investigation
disp('MRI investigation')
temporal=contains(string(pat_info.epilepsy_lobe(pat_sel,:)),'TLE'); % split into TLE and other

figure
p= ranksum(seiz_effect_pat(temporal,:),seiz_effect_pat(~temporal,:));
boxplot(seiz_effect_pat,[pat_info.epilepsy_lobe(pat_sel,:),pat_info.MRI(pat_sel,:)]); 
%For MATLAB older than 2018b
%line([2.5 2.5], ylim, 'Color', 'r', 'LineStyle', '--')
xline(2.5)
title(['epilepsy lobe & MRI investigation, p = ',num2str(p)]);
ylabel('AE seizure effect ( seiz - pre )')


%% left vs right
disp('left vs. right')
left=contains(string(pat_info.hemisphere(pat_sel,:)),'L');

figure
p=ranksum(seiz_effect_pat(left),seiz_effect_pat(~left));
boxplot(seiz_effect_pat,pat_info.hemisphere(pat_sel,:)); 
title(['hemisphere, p = ',num2str(p)]);
ylabel('AE seizure effect ( seiz - pre )')


%% good vs bad surgery outcome 
disp('good vs. bad outcome')
badoutcome=pat_info.engel_outcome(pat_sel)==4; 

figure
p=ranksum(seiz_effect_pat(badoutcome),seiz_effect_pat(~badoutcome),'tail','left');
boxplot(seiz_effect_pat,pat_info.engel_outcome(pat_sel)); 
%For MATLAB older than 2018b
%line([2.5 2.5], ylim, 'Color', 'r', 'LineStyle', '--')
xline(2.5);
title(['surgery outcome (Engel), p = ',num2str(p)]);
ylabel('AE seizure effect ( seiz - pre )')


% patients with good outcome have significantly longer seizures
disp('seiz length and surgery outcome')
goodoutcome=pat_info.engel_outcome(pat_sel)==1;

figure
%without outlier patient number 14
p=ranksum(pat_info.mean_Sez_Len(goodoutcome([1:13,15:16])),pat_info.mean_Sez_Len(~goodoutcome([1:13,15:16])));
boxplot(pat_info.mean_Sez_Len(([1:13,15:16])),pat_info.engel_outcome(([1:13,15:16])))

%For MATLAB older than 2018b
%line([1.5 1.5], ylim, 'Color', 'r', 'LineStyle', '--')
xline(1.5);
ylabel('mean seiz length (s)');
xlabel('surgery outcome (Engel)');
title(['mean seiz length, p = ',num2str(p)])


%% # seizures
disp('# seizures')

figure
[r,p] = corr(pat_info.No_of_Seizures(pat_sel),seiz_effect_pat,'Type', 'Spearman');
scatter(pat_info.No_of_Seizures(pat_sel),seiz_effect_pat,80,pat_info.engel_outcome(pat_sel),'filled'); 
xfit=fit(pat_info.No_of_Seizures(pat_sel),seiz_effect_pat,'poly1');
hold on; plot(xfit)
title(['r = ', num2str(r),', p = ',num2str(p)]);
xlabel('# seizures')
ylabel('AE seizure effect ( seiz - pre )')


%% mean_Sez_Len
disp('mean seiz length')

figure;
%without outlier patient number 14
[r,p] = corr(pat_info.mean_Sez_Len([1:13,15:16]),mean(seiz_effect_pat_seiz([1:13,15:16],:),2,'omitnan'),'Type', 'Spearman');
scatter(pat_info.mean_Sez_Len([1:13,15:16]),mean(seiz_effect_pat_seiz([1:13,15:16],:),2,'omitnan'),80,pat_info.engel_outcome([1:13,15:16]),'filled'); 
title(['Spearman r = ',num2str(r),', p = ',num2str(p)]);
xlabel('mean seizure length (s)'); ylabel('AE seizure effect ( seiz - pre )');



%%  3D: seiz length, number of seizures, and surgery outcome
figure;scatter3(pat_info.mean_Sez_Len(pat_sel),...
    pat_info.No_of_Electrodes(pat_sel),seiz_effect_pat,80,pat_info.engel_outcome(pat_sel),'filled')
xlabel('mean seizure length (s)')
ylabel('# seizures')
zlabel('AE seizure effect ( seiz - pre )')
title('surgery outcome (Engel)');


