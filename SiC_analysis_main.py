# -*- coding: utf-8 -*-
"""
File: SiC_analysis_main.py
Created: 2024-DEC-10
@author: Rebecca Frederick
Deku Lab Silicon Carbide Review Data Analysis
Last Updated: 2025-SEP-19 by Rebecca A. Frederick


"""
#-----------------------------------------------------------------------------
#                               READ ME
#-----------------------------------------------------------------------------
# Files Required in Project Folder:
    # SiC_analysis_main.py
    # SiC_analysis_functions.py
# Subfolders Required in Project Folder:
    # Data Files
    # Outputs
#-----------------------------------------------------------------------------
# Run installations as needed for your environment (using conda):
    # conda install os
    # conda install pandas
    # conda install plotly
    # conda install -c conda-forge python-kaleido
    # conda install matplotlib
    # conda install statsmodels
# Run installations as needed for your environment (using pip):
    # pip install os
    # pip install pandas
    # pip install plotly
    # pip install kaleido
    # pip install matplotlib
    # pip install statsmodels


#-----------------------------------------------------------------------------
#                               SECTION 1
#-----------------------------------------------------------------------------
# Import Required Packages
#
# Include packages required for data analysis:
import os   # used to get current working directory
import pandas as pd   # used to read raw data csv files
import plotly.express as px   # used to create interactive data visualizations
import plotly.graph_objects as go   # used to create interactive data visualizations
import plotly.io as pio  # used for creating plot templates
import matplotlib.pyplot as plt  # used to make static plots
import matplotlib.ticker as ticker # used to setup minor ticks in plots
from statsmodels.graphics.mosaicplot import mosaic  # used for mosaic plots only
from PIL import Image
#import numpy as np
#import matplotlib.mlab as mlab
#
# Include all custom functions for data analysis and plotting:
    # files SiC_analysis_functions.py and SiC_plot_functions.py
    # must be in the same folder as SiC_analysis_main.py
from SiC_functions_analysis import ArticleList_Analysis00a
from SiC_functions_analysis import ArticleList_Analysis00b
from SiC_functions_analysis import ArticleList_Analysis01
from SiC_functions_analysis import ArticleList_Analysis02
from SiC_functions_analysis import ArticleList_Analysis03
from SiC_functions_analysis import ArticleList_Analysis04
from SiC_functions_analysis import ArticleList_Analysis05
from SiC_functions_analysis import ArticleList_Analysis06
from SiC_functions_plots import ArticleList_Plot01
from SiC_functions_plots import ArticleList_Plot02
from SiC_functions_plots import ArticleList_Plot02b
from SiC_functions_plots import ArticleList_Plot03mosaic
from SiC_functions_plots import ArticleList_Plot03heat
from SiC_functions_plots import ArticleList_Plot03ice



#-----------------------------------------------------------------------------
#                               SECTION 2
#-----------------------------------------------------------------------------
# Define all datafile names/locations
#-----------------------------------------------------------------------------
TopFolderName = os.getcwd()
FolderName = TopFolderName + '\\Data Files\\'
SaveLocation = TopFolderName + '\\Outputs\\'
SaveFolderHTML = TopFolderName + '\\App Files\\Graphs\\'
#
ArticleList_FileName = '0_SiC-Review_Included-Articles_Master-List_Stage3_reduced.csv'
#ArticleList_FileName = '0_SiC-Review_Included-Articles_Master-List.csv'
ReviewsList_FileName = '0_SiC-Review_Included-Articles_Review-List_Stage3_reduced.csv'
#ReviewsList_FileName = '0_SiC-Review_Included-Articles_Reviews-List.csv'
Neural_InVivo_FileName = 'NeuralEng_Details_All_InVivo.csv'
#-----------------------------------------------------------------------------
#
ArticleList_Location = FolderName + ArticleList_FileName
ReviewsList_Location = FolderName + ReviewsList_FileName
NE_data_InVivo_Location = FolderName + Neural_InVivo_FileName
#


#-----------------------------------------------------------------------------
#                               SECTION 3
#-----------------------------------------------------------------------------
# Import Data Into Data Frames
#-----------------------------------------------------------------------------
#
# Read Raw Data CSV Files Into New DataFrames:
ArticleList_DF = pd.read_csv(ArticleList_Location)
ReviewsList_DF = pd.read_csv(ReviewsList_Location)
Neural_InVivo_DF = pd.read_csv(NE_data_InVivo_Location)
#
# Force pubmed_id to text from number
ArticleList_DF['pubmed_id'] = ArticleList_DF['pubmed_id'].astype(pd.Int64Dtype()).astype(str)
ReviewsList_DF['pubmed_id'] = ReviewsList_DF['pubmed_id'].astype(pd.Int64Dtype()).astype(str)
Neural_InVivo_DF['pubmed_id'] = Neural_InVivo_DF['pubmed_id'].astype(pd.Int64Dtype()).astype(str)


#-----------------------------------------------------------------------------
#                               SECTION 4
#-----------------------------------------------------------------------------
# Format and Add Information to ArticleList_DF dataframe:
#-----------------------------------------------------------------------------
# Convert Year Column to DateTime Data Type:
ArticleList_DF['year'] = pd.to_datetime(ArticleList_DF['year'], format='%Y').dt.year
# Check Imported Data for Article List:
ArticleList_DTypes_atLoad = ArticleList_DF.dtypes    # pull initial list of data types
# Add publication decade data column to ArticleList_DF
ArticleList_DF['pub_decade'] = ArticleList_DF['year'] // 10 * 10    # creates new year values by decades
#-----------------------------------------------------------------------------
# Define the range of SiC Type columns to check
start_col_SiC = 'amorphousSiC'
end_col_SiC = 'crystalline_6H-SiC'
# Get the list of column names within the specified range
cols_in_SiC_range = ArticleList_DF.loc[:, start_col_SiC:end_col_SiC].columns.tolist()
# Apply a function to each row to get the true column names in the specified range
ArticleList_DF['Reported_SiC'] = ArticleList_DF.apply(
    lambda row: [col for col in cols_in_SiC_range if row[col]], axis=1)
# Replace column names with shorter labels
ArticleList_DF['Reported_SiC'] = ArticleList_DF['Reported_SiC'].apply(lambda x: [item.replace('amorphousSiC', 'a-SiC') for item in x])
ArticleList_DF['Reported_SiC'] = ArticleList_DF['Reported_SiC'].apply(lambda x: [item.replace('otherSiC', 'Other') for item in x])
ArticleList_DF['Reported_SiC'] = ArticleList_DF['Reported_SiC'].apply(lambda x: [item.replace('crystalline_other_unspecified', 'Crystalline') for item in x])
ArticleList_DF['Reported_SiC'] = ArticleList_DF['Reported_SiC'].apply(lambda x: [item.replace('crystalline_3C-SiC', '3C-SiC') for item in x])
ArticleList_DF['Reported_SiC'] = ArticleList_DF['Reported_SiC'].apply(lambda x: [item.replace('crystalline_4H-SiC', '4H-SiC') for item in x])
ArticleList_DF['Reported_SiC'] = ArticleList_DF['Reported_SiC'].apply(lambda x: [item.replace('crystalline_6H-SiC', '6H-SiC') for item in x])
#-----------------------------------------------------------------------------
# Define the range of Study Category columns to check
start_col_cat = 'NeuralEng'
end_col_cat = 'GeneralImplants_OtherTech'
# Get the list of column names within the specified range
cols_in_cat_range = ArticleList_DF.loc[:, start_col_cat:end_col_cat].columns.tolist()
# Apply a function to each row to get the true column names in the specified range
ArticleList_DF['Reported_Category'] = ArticleList_DF.apply(
    lambda row: [col for col in cols_in_cat_range if row[col]], axis=1)
# Replace column names with shorter labels
ArticleList_DF['Reported_Category'] = ArticleList_DF['Reported_Category'].apply(lambda x: [item.replace('NeuralEng', 'Neural') for item in x])
ArticleList_DF['Reported_Category'] = ArticleList_DF['Reported_Category'].apply(lambda x: [item.replace('Biosensor', 'Biosensors') for item in x])
ArticleList_DF['Reported_Category'] = ArticleList_DF['Reported_Category'].apply(lambda x: [item.replace('Orthopedic_Dental', 'Ortho/Dental') for item in x])
ArticleList_DF['Reported_Category'] = ArticleList_DF['Reported_Category'].apply(lambda x: [item.replace('Cardiovascular', 'Cardio') for item in x])
ArticleList_DF['Reported_Category'] = ArticleList_DF['Reported_Category'].apply(lambda x: [item.replace('DrugRelease', 'Drug Release') for item in x])
ArticleList_DF['Reported_Category'] = ArticleList_DF['Reported_Category'].apply(lambda x: [item.replace('GeneralImplants_OtherTech', 'OtherTech') for item in x])
#-----------------------------------------------------------------------------
# Define the range of Data Type columns to check
start_col_dtype = 'InVivo_animal'
end_col_dtype = 'ExVivo'
# Get the list of column names within the specified range
cols_in_dtype_range = ArticleList_DF.loc[:, start_col_dtype:end_col_dtype].columns.tolist()
# Apply a function to each row to get the true column names in the specified range
ArticleList_DF['Reported_Data'] = ArticleList_DF.apply(
    lambda row: [col for col in cols_in_dtype_range if row[col]], axis=1)
# Replace column names with shorter labels
ArticleList_DF['Reported_Data'] = ArticleList_DF['Reported_Data'].apply(lambda x: [item.replace('FabricationMethods', 'Fabrication') for item in x])
ArticleList_DF['Reported_Data'] = ArticleList_DF['Reported_Data'].apply(lambda x: [item.replace('MaterialProperties', 'Material Properties') for item in x])
ArticleList_DF['Reported_Data'] = ArticleList_DF['Reported_Data'].apply(lambda x: [item.replace('Benchtop', 'Benchtop') for item in x])
ArticleList_DF['Reported_Data'] = ArticleList_DF['Reported_Data'].apply(lambda x: [item.replace('CellCulture_InVitro', 'In Vitro') for item in x])
ArticleList_DF['Reported_Data'] = ArticleList_DF['Reported_Data'].apply(lambda x: [item.replace('ExVivo', 'Ex Vivo') for item in x])
ArticleList_DF['Reported_Data'] = ArticleList_DF['Reported_Data'].apply(lambda x: [item.replace('InVivo_animal', 'Aniaml') for item in x])
ArticleList_DF['Reported_Data'] = ArticleList_DF['Reported_Data'].apply(lambda x: [item.replace('InVivo_human', 'Human') for item in x])
#-----------------------------------------------------------------------------
# Export ArticleList dataframe information:
ArticleList_Columns = ArticleList_DF.columns    # pull list of column names
ArticleList_DataTypes = ArticleList_DF.dtypes    # pull new list of data types
#-----------------------------------------------------------------------------
# !!!!!!!  in progress 2025 Sept
#testgroup01 = ArticleList_DF.groupby('Study_Category')['SiC_Type'].sum()

#-----------------------------------------------------------------------------
# Format and Add Information to Neural dataframes:
#-----------------------------------------------------------------------------
# Change index to refID:
Neural_InVivo_DF = Neural_InVivo_DF.set_index(['refID'])
# !!!!!!!  Add other Neural dataframes

# Update column data types for Neural_InVivo_DF:
Neural_InVivo_DF['Species'] = Neural_InVivo_DF['Species'].astype('category')
Neural_InVivo_DF['Strain'] = Neural_InVivo_DF['Strain'].astype('category')
Neural_InVivo_DF['Sex'] = Neural_InVivo_DF['Sex'].astype('category')
Neural_InVivo_DF['Implant_Location'] = Neural_InVivo_DF['Implant_Location'].astype('category')
Neural_InVivo_DF['DeviceID'] = Neural_InVivo_DF['DeviceID'].astype('category')
Neural_InVivo_DF['Device_Substrate'] = Neural_InVivo_DF['Device_Substrate'].astype('category')
Neural_InVivo_DF['ElectrodeSite_Material'] = Neural_InVivo_DF['ElectrodeSite_Material'].astype('category')



#-----------------------------------------------------------------------------
#                               SECTION 5
#-----------------------------------------------------------------------------
# Setup Template for Plots
# 'rgba(0,0,0,0)' # = transparent
# 'rgba(255, 255, 255, 0.5)' = # white, 60% tranparency
#-----------------------------------------------------------------------------

# Setup plot template:
template1 = go.layout.Template()
# Set font and colors
template1.layout.font = dict(size=16,color='black')
template1.layout.plot_bgcolor = 'white'
# Set axis line properties
template1.layout.xaxis = dict(gridcolor='lightgray',gridwidth=1,
                              showline=True,mirror=True)
template1.layout.yaxis = dict(gridcolor='lightgray',gridwidth=1,
                              showline=True,mirror=True)
# Set figure margins
template1.layout.margin =  dict(l=60,r=40,t=60,b=60)
# Set legend properties
template1.layout.legend.font = dict(size=14)
#template1.layout.legend.bgcolor = 'rgba(0,0,0,0)' # = transparent

# Set template as default
pio.templates['SiC_app_plot_template'] = template1
pio.templates.default = 'SiC_app_plot_template'

#-----------------------------------------------------------------------------
# Color-blind tested color schemes:
#-----------------------------------------------------------------------------

# Custom color pallet 1 = Paul Tol's Muted
my_colors1 = [0] * 9
my_colors1[0] = 'rgb(221,221,221)'
my_colors1[1] = 'rgb(46,37,133)'
my_colors1[2] = 'rgb(51,117,56)'
my_colors1[3] = 'rgb(93,168,153)'
my_colors1[4] = 'rgb(148,203,236)'
my_colors1[5] = 'rgb(220,205,125)'
my_colors1[6] = 'rgb(194,106,119)'
my_colors1[7] = 'rgb(159,74,150)'
my_colors1[8] = 'rgb(126,41,84)'

# Custom color pallet 2 = Paul Tol's Bright
my_colors2 = [0] * 7
my_colors2[0] = 'rgb(187,187,187)'
my_colors2[1] = 'rgb(46,37,133)'
my_colors2[2] = 'rgb(51,117,56)'
my_colors2[3] = 'rgb(93,168,153)'
my_colors2[4] = 'rgb(148,203,236)'
my_colors2[5] = 'rgb(220,205,125)'
my_colors2[6] = 'rgb(194,106,119)'

# Custom color pallet 3 = Okabe and Ito
my_colors3 = [0] * 8
my_colors3[0] = 'rgb(0,0,0)'
my_colors3[1] = 'rgb(0,158,115)'
my_colors3[2] = 'rgb(0,114,178)'
my_colors3[3] = 'rgb(86,180,233)'
my_colors3[4] = 'rgb(240,228,66)'
my_colors3[5] = 'rgb(230,159,0)'
my_colors3[6] = 'rgb(213,94,0)'
my_colors3[7] = 'rgb(204,121,167)'

# Pull seleced default color values from Plotly
    # see https://plotly.com/python/builtin-colorscales/
c_greys = px.colors.sequential.Greys
c_gray = px.colors.sequential.gray
c_vidiris = px.colors.sequential.Viridis


#-----------------------------------------------------------------------------
#                               SECTION 6
#-----------------------------------------------------------------------------
# Create and Store ArticleList Statistics
#-----------------------------------------------------------------------------
# Pull/Crate statistics on publication years:
year_max = ArticleList_DF.year.max()
year_min = ArticleList_DF.year.min()
year_range = year_max-year_min
# Count total publications for each year:
year_unique_count = ArticleList_DF.year.value_counts().sort_index().reset_index()
year_unique_count = year_unique_count.rename(columns={'count':'publications'})
year_unique_count = year_unique_count.set_index('year')
# Create list of publication decades:
decade_unique_count = ArticleList_DF.pub_decade.value_counts().sort_index().reset_index()
decade_unique_count = decade_unique_count.rename(columns={'count':'publications'})
decade_unique_count['decade_end'] = decade_unique_count.pub_decade+9
decade_unique_count[5,'decade_end'] = 2025  # review data ends in year 2025
decade_unique_count.set_index('pub_decade', inplace=True)


#-----------------------------------------------------------------------------
#                               SECTION 7
#-----------------------------------------------------------------------------
# Run ArticleList_Analysis functions:
#-----------------------------------------------------------------------------
# Create ArticleListDF_skinny (remove boolean cols & extra info)
ArticleListDF_skinny = ArticleList_Analysis00a(ArticleList_DF) 
# Create ArticleListDF_exploded (expand category label lists to multiple rows)
ArticleListDF_exploded = ArticleList_Analysis00b(ArticleListDF_skinny)
# Create Cat_by_Yr_melted
Cat_by_Yr_melted = ArticleList_Analysis01(ArticleList_DF,decade_unique_count)
# Create cat_by_decade_totals
cat_by_decade_totals = ArticleList_Analysis02(Cat_by_Yr_melted)
# Output dataframes filtered by device type/category
    # ['NeuralEng','Biosensor','Cardiovascular','Orthopedic_Dental','DrugRelease','GeneralImplants_OtherTech']

# !!!!!!!  in progress 2025 Sept

ArticleList_Dictionary = ArticleList_Analysis03(ArticleList_DF)
DF1 = ArticleList_Analysis04(ArticleList_DF)  
DF2 = ArticleList_Analysis05(ArticleList_DF)  
DF3 = ArticleList_Analysis06(ArticleList_DF)  


#-----------------------------------------------------------------------------
#                               SECTION 8
#-----------------------------------------------------------------------------
# Run ArticleList_Plot functions:
#-----------------------------------------------------------------------------
# save html & png version of "fig_article-count-by-year" to Outputs folder
ArticleList_Plot01(SaveLocation,SaveFolderHTML,year_unique_count)
# save html & png version of "fig_article-category-by-decade" to Outputs folder
ArticleList_Plot02(SaveLocation,SaveFolderHTML,c_greys,Cat_by_Yr_melted,cat_by_decade_totals)
ArticleList_Plot02b(SaveLocation,SaveFolderHTML,c_greys,ArticleListDF_exploded) # -vB
#save html & png version of "fig_mosaic-SiC-publications" to Outputs folder
ArticleList_Plot03mosaic(SaveLocation,SaveFolderHTML,ArticleListDF_exploded)
ArticleList_Plot03heat(SaveLocation,SaveFolderHTML,ArticleListDF_exploded)
ArticleList_Plot03ice(SaveLocation,SaveFolderHTML,ArticleListDF_exploded)

# !!!!!!!  in progress 2025 Sept



#-----------------------------------------------------------------------------
#                               SECTION 9
#-----------------------------------------------------------------------------
# Run NeuralEng_Analysis functions:
#-----------------------------------------------------------------------------
# !!!!!!!  in progress 2025 Sept


#-----------------------------------------------------------------------------
#                         TEMP CODE - TESTING AREA
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# Sample data
#data = {
#    'Gender': ['Male', 'Male', 'Female', 'Female', 'Male', 'Female'],
#    'Smoker': ['Yes', 'No', 'Yes', 'No', 'Yes', 'No']
#}
#df = pd.DataFrame(data)

# Create the mosaic plot
#mosaic(df, ['Gender', 'Smoker'])

# Add a title (optional)
#plt.title('Mosaic Plot of Gender and Smoker Status')

# Display the plot
#plt.show()

#-----------------------------------------------------------------------------
#                             End of File
#-----------------------------------------------------------------------------
