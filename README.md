# Km-Curve-Plot-Generator
This software generates two Km curves to compare survival outcomes between two sets of data.  It requires two files: 1. a csv with two columns with patient-IDs for each of the two groups that are being compared, and 2. the clinical output tsv file that can be downloaded from cbioportal.

## Instructions

1. Create a csv file with two columns, as shown below:
   
![image](https://github.com/u-kapoor/Km-Curve-Plot-Generator/assets/160059835/9b1ee9c3-1cad-4342-b30f-9dc5c6e86b44)
   
2. Download the tsv file from your desired dataset on https://www.cbioportal.org/ (example shown below):

![image](https://github.com/u-kapoor/Km-Curve-Plot-Generator/assets/160059835/81bece86-3e80-4a27-800f-8f69106f8d7e)

3. Edit the section labeled "variables to change" in the Km Plot Generator.py file with the desired filenames and filepaths.  Optionally, can change "all-charts" to True to view OS, DFS, PFS, and DSS all in one chart, or can individually set the desired outcome measure by changing the 'desired_survival_type' variable.
