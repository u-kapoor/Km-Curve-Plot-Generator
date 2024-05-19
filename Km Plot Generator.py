# %% [markdown]
# **Generating Km Curves**

# %%
# Key functions and imported libraries
from docx import Document
import numpy as np
import pandas as pd
import re
import os
import json
from lifelines import KaplanMeierFitter
import lifelines.datasets
import matplotlib.pyplot as plt

# Variables to change 
filepath = r'C:\Users\ ... ' # Edit this and the filename as needed
IDs_filename = r'... .csv' # Set this to a file with two columns, with patient IDs (e.g., TCGA-XYZ) from each of the two desired comparison groups
clin_filename = r'... .tsv' # Set this to the clinical data tsv file, as taken from cbioportal
all_charts = False #toggle whether you need all charts at once or not
desired_survival_type = 0 # Set this to desired survival type:
                          #  0 = Disease Free, 1 = Progression Free, 2 = Disease Specific, 3 = Overall

# Additional variables
survival_names = ['Disease Free', 'Progression Free', 'Disease Specific', 'Overall']
survival_types = ['Disease Free', 'Progress', '-specific', 'Overall']

# %%
# Generating all curves in one chart
if (all_charts == True):
    desired_survival_type = 0
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    match_duration = []
    match_status = []
    non_match_duration = []
    non_match_status = []

    for desired_survival_type in range(len(survival_types)):
        extracted_cols = survival_types[desired_survival_type]
        
        # Read in clinical and patient group data 
        clin_data = pd.read_csv(filepath + chr(92) + clin_filename, sep='\t')
        IDs_data = pd.read_csv(filepath + chr(92) + IDs_filename)
        clin_filtered = clin_data.filter(regex=extracted_cols).dropna().join(clin_data.iloc[:,1])
        
        # Filter by match and non-match
        Match = IDs_data.iloc[:,0].dropna()
        Non_Match = IDs_data.iloc[:,1].dropna()
        clin_match = np.in1d(clin_filtered.iloc[:,2], Match)
        clin_non_match = np.in1d(clin_filtered.iloc[:,2], Non_Match)
        clin_filtered['Group'] = ''
        clin_filtered['Group'].mask(clin_match, other='Match', inplace=True)
        clin_filtered['Group'].mask(clin_non_match, other='Non-Match', inplace=True)
        match_surv_data = clin_filtered.where(clin_filtered['Group'] == 'Match').dropna()
        non_match_surv_data = clin_filtered.where(clin_filtered['Group'] == 'Non-Match').dropna()
        
        # Survival duration and status from the datasets
        match_duration.append(match_surv_data.iloc[:,0])
        match_status.append(match_surv_data.iloc[:,1].str.split(':', n=1, expand=True).iloc[:,0].astype(int))
        non_match_duration.append(non_match_surv_data.iloc[:,0])
        non_match_status.append(non_match_surv_data.iloc[:,1].str.split(':', n=1, expand=True).iloc[:,0].astype(int))

        # Km curves
        kmf = KaplanMeierFitter()
        plot_bin = str(bin(desired_survival_type).lstrip('-0b').zfill(2)) +'0'
        kmf.fit(match_duration[desired_survival_type], match_status[desired_survival_type], label=IDs_data.columns[0])
        ax = kmf.plot_survival_function(ax=axes[int(plot_bin[0])][int(plot_bin[1])], color='k', ci_show=False)
        kmf.fit(non_match_duration[desired_survival_type], non_match_status[desired_survival_type], label=IDs_data.columns[1])
        ax = kmf.plot_survival_function(ax=ax, color='0.7', ci_show=False)
        ax.set_xlabel('Months elapsed')
        ax.set_ylabel('Probability of Survival')
        ax.get_legend().remove()
        plt.show()

#One chart display
else:
    extracted_cols = survival_types[desired_survival_type]

    # Read in clinical and patient group data 
    clin_data = pd.read_csv(filepath + chr(92) + clin_filename, sep='\t')
    IDs_data = pd.read_csv(filepath + chr(92) + IDs_filename)
    clin_filtered = clin_data.filter(regex=extracted_cols).dropna().join(clin_data.iloc[:,1])

    # Filter by match and non-match
    Match = IDs_data.iloc[:,0].dropna()
    Non_Match = IDs_data.iloc[:,1].dropna()
    clin_match = np.in1d(clin_filtered.iloc[:,2], Match)
    clin_non_match = np.in1d(clin_filtered.iloc[:,2], Non_Match)
    clin_filtered['Group'] = ''
    clin_filtered['Group'].mask(clin_match, other='Match', inplace=True)
    clin_filtered['Group'].mask(clin_non_match, other='Non-Match', inplace=True)
    match_surv_data = clin_filtered.where(clin_filtered['Group'] == 'Match').dropna()
    non_match_surv_data = clin_filtered.where(clin_filtered['Group'] == 'Non-Match').dropna()

    # Survival duration and status from the datasets
    match_duration = match_surv_data.iloc[:,0]
    match_status = match_surv_data.iloc[:,1].str.split(':', n=1, expand=True).iloc[:,0].astype(int)
    non_match_duration = non_match_surv_data.iloc[:,0]
    non_match_status = non_match_surv_data.iloc[:,1].str.split(':', n=1, expand=True).iloc[:,0].astype(int)

    #Generate Graphs
    kmf = KaplanMeierFitter()
    kmf.fit(match_duration, match_status)
    ax = kmf.plot_survival_function(color='k', ci_show=False, fontsize=20)
    kmf.fit(non_match_duration, non_match_status)
    ax = kmf.plot_survival_function(ax=ax, color='0.7', ci_show=False)
    ax.set_xticks([0,25,50,75,100,125,150])
    ax.set_yticks([0,0.25,0.5,0.75,1])
    ax.get_legend().remove()
    plt.xlabel("")
    plt.show()


