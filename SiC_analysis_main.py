# -*- coding: utf-8 -*-
"""
File: SiC_analysis_main.py
Created: 2024-DEC-10
@author: RebeccaFrederick
Deku Lab Silicon Carbide Review Data Analysis
Last Updated: 2025-JUNE-18 by Rebecca A. Frederick
"""
#-----------------------------------------------------------------------------
# !!!  TO DO LIST  !!!
#-----------------------------------------------------------------------------
# make single folder with data analysis files and raw data...
    # downloadable from Open Science Framework = data anlysis folder
# Ask user for data analysis folder location:
    # (to avoid breaking later data analysis steps)
# pop-up user query to get location of data analysis folder
# Create variable "RawData_ArticleList_Location" to store article data location
# pop-up user query to get article csv file within data analysis folder
# fix grouping of SiC_types_info list
#-----------------------------------------------------------------------------
# Notes for running code via Spyder...
#-----------------------------------------------------------------------------
# Figures are displayed in the Plots pane by default.
# To make figuers also appear inline in the console, 
# you need to uncheck "Mute inline plotting" under the options menu of Plots.
# 
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#                               SECTION 1
#-----------------------------------------------------------------------------
# Required Packages
#-----------------------------------------------------------------------------
# Include packages required for data analysis:
import pandas as pd   # used to read raw data csv files
import numpy as np
import matplotlib.pyplot as plt  # used to make plots
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker # used to setup minor ticks in plots
#
#
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#                               SECTION 2
#-----------------------------------------------------------------------------
# Set Folder and File Locations
FolderName = 'S:\\Code Repository\\SiC Review Paper Data and Figures\\'
ArticleList_FileName = '0_SiC-Review_Included-Articles-List.csv'
#NeuralEngList_FileName = '0_SiC-Review_Included-Articles-NeuralEng.csv'
#-----------------------------------------------------------------------------
#ArticleList_Location = r'S:/Code Repository/SiC Review Paper Data and Figures/0_SiC-Review_Included-Articles-List.csv'
ArticleList_Location = FolderName + ArticleList_FileName
#NeuralEngList_Location = r'S:/Code Repository/SiC Review Paper Data and Figures/0_SiC-Review_Included-Articles-NeuralEng.csv'
#NeuralEngList_Location = FolderName + NeuralEngList_FileName
#
#
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#                               SECTION 3
#-----------------------------------------------------------------------------
# Import Data Into Data Frame
#-----------------------------------------------------------------------------
#
# Read Raw Data CSV File Into New DataFrames:
ArticleList_DataFrame = pd.read_csv(ArticleList_Location)
#NeuralEngList_DataFrame = pd.read_csv(NeuralEngList_Location)
print("Article List...")
# Convert Year Column to DateTime Data Type:
ArticleList_DataFrame['year'] = pd.to_datetime(ArticleList_DataFrame['year'], format='%Y').dt.year
#print(ArticleList_DataFrame.year)
# Check Imported Data for Article List:
ArticleList_Columns = ArticleList_DataFrame.columns    # pull list of column names
print(ArticleList_Columns)    # display list of column names
ArticleList_DataTypes = ArticleList_DataFrame.dtypes    # pull list of data types
print(ArticleList_DataTypes)    # display list of data types
#-----------------------------------------------------------------------------
# Separate list into review vs. non-review publications:
ArticleList_Reviews = ArticleList_DataFrame[ArticleList_DataFrame['review_article'] == True]
ArticleList_NoReviews = ArticleList_DataFrame[ArticleList_DataFrame['review_article'] == False]
#
#
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#                               SECTION 4
#-----------------------------------------------------------------------------
# Create and Store Article List Statistics
#-----------------------------------------------------------------------------
# Report statistics on publication years
year_max = ArticleList_NoReviews.year.max()
year_min = ArticleList_NoReviews.year.min()
year_range = year_max-year_min
year_unique_count = ArticleList_NoReviews.year.value_counts().sort_index()
ArticleList_NoReviews['pub_decade'] = ArticleList_NoReviews['year'] // 10 * 10    # creates new year values by decades
#print("Number of Publications by Year...")
#print(year_unique_count)
# 
# Report statistics on types of silicon carbide reported:
SiC_types_info = ArticleList_NoReviews.SiC_Type.value_counts().sort_index()
#print("Number of Publications by SiC Type...")
#print(SiC_types_info)
##crSiC_types = ArticleList_DataFrame.SiC_type_crystalline.unique()
##crSiC_types = crSiC_types[~pd.isna(crSiC_types)]
##print(crSiC_types)
# 
# Group articles by category and year:
Categories_by_Year = ArticleList_NoReviews.groupby(['year', 'Application']).size().unstack()
#print("Applications vs. Year...")
#print(Categories_by_Year)
#
Categories_by_Decade = ArticleList_NoReviews.groupby(['pub_decade', 'Application']).size().unstack()
#print("Applications vs. Decade...")
#print(Categories_by_Decade)
#
# Group articles by silicon carbide type and category:
SiC_by_Cat = ArticleList_NoReviews.groupby(['Application', 'SiC_Type']).size().unstack()
#print("SiC Types vs. Applications...")
#print(SiC_by_Cat)
#
# Group articles by silicon carbide type and data reported:
Data_by_SiC_animal = ArticleList_NoReviews.groupby(['SiC_Type', 'InVivo_animal']).size().unstack()
#print("Data Reported vs. SiC Type...")
#print(Data_by_SiC_animal)
#
#
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#                               SECTION 5
#-----------------------------------------------------------------------------
# Pull list of only Neural Engineering articles:
NeuralEngList_DataFrame = ArticleList_DataFrame[ArticleList_DataFrame['NeuralEng'] == True]
NeuralEngList_DataFrame = NeuralEngList_DataFrame.drop(['Biosensor','GlucoseSensor',
                                                        'Cardiovascular','Bone',
                                                        'DrugRelease','Electroporation',
                                                        'GeneralImplants','RadiationDetection',
                                                        'TissueEng'],axis='columns')
NeuralEngList_Columns = NeuralEngList_DataFrame.columns
NeuralEngList_DataTypes = NeuralEngList_DataFrame.dtypes
#-----------------------------------------------------------------------------
# Separate list into review vs. non-review publications:
NeuralEngList_Reviews = NeuralEngList_DataFrame[NeuralEngList_DataFrame['review_article'] == True]
NeuralEngList_NoReviews = NeuralEngList_DataFrame[NeuralEngList_DataFrame['review_article'] == False]
#
# Create lists of differnt reported data types within Neural Eng papers:
#   In Vivo Data - Animals:
in_vivo_a_list = NeuralEngList_NoReviews[NeuralEngList_NoReviews['InVivo_animal'] == True]    
in_vivo_a_list = in_vivo_a_list.drop(['InVivo_human','ExVivoData','BiocompatibilityData'],axis=1)
#   In Vivo Data - Humans:
in_vivo_h_list = NeuralEngList_NoReviews[NeuralEngList_NoReviews['InVivo_human'] == True]
in_vivo_h_list = in_vivo_h_list.drop(['InVivo_animal','ExVivoData','BiocompatibilityData'],axis=1)
#   Material Properties:
mat_properties_list = NeuralEngList_NoReviews[NeuralEngList_NoReviews['MaterialProperties'] == True]
mat_properties_list = mat_properties_list.drop(['InVivo_human','InVivo_animal','ExVivoData','BiocompatibilityData'],axis=1)
#   Fabrication Methods:
benchtop_list = NeuralEngList_NoReviews[NeuralEngList_NoReviews['FabricationMethods'] == True]
benchtop_list = benchtop_list.drop(['InVivo_human','InVivo_animal','ExVivoData','BiocompatibilityData'],axis=1)
#   Benchtop:
benchtop_list = NeuralEngList_NoReviews[NeuralEngList_NoReviews['BenchtopData'] == True]
benchtop_list = benchtop_list.drop(['InVivo_human','InVivo_animal','ExVivoData','BiocompatibilityData'],axis=1)
#   Ex Vivo Data:
ex_vivo_list = NeuralEngList_NoReviews[NeuralEngList_NoReviews['ExVivoData'] == True]
ex_vivo_list = ex_vivo_list.drop(['InVivo_human','InVivo_animal','BiocompatibilityData'],axis=1)
#   In Vitro Data:
in_vitro_list = NeuralEngList_NoReviews[NeuralEngList_NoReviews['BiocompatibilityData'] == True]
in_vitro_list = in_vitro_list.drop(['InVivo_human','InVivo_animal','ExVivoData'],axis=1)
#
#-----------------------------------------------------------------------------
# Export Neural Engineering Article Lists
#-----------------------------------------------------------------------------
NeuralEngList_DataFrame.to_csv(FolderName+'Outputs/NeuralEng_Articles.csv')
in_vivo_h_list.to_csv(FolderName+'Outputs/neuraleng_list_human.csv')
in_vivo_a_list.to_csv(FolderName+'Outputs/neuraleng_list_animal.csv')
ex_vivo_list.to_csv(FolderName+'Outputs/neuraleng_list_ex_vivo.csv')
in_vitro_list.to_csv(FolderName+'Outputs/neuraleng_list_in_vitro.csv')
benchtop_list.to_csv(FolderName+'Outputs/neuraleng_list_benchtop.csv')
mat_properties_list.to_csv(FolderName+'Outputs/neuraleng_list_mat_properties.csv')
#
#
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#                               SECTION 6
#-----------------------------------------------------------------------------
# Plot General Article Statistics and Metadata Information
#-----------------------------------------------------------------------------
#
# [Fig01] PlotCatbyYear, title='Category Counts by Year'
ax01 = Categories_by_Year.plot(kind='bar', stacked=True, zorder=2,
                            title='Silicon Carbide Publication Topics Over Time', 
                            xlabel='Year', ylabel='Number of Publications', 
                            yticks=[0,2,4,6,8,10,12,14,16,18])
ax01.yaxis.minorticks_on()
ax01.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
ax01.yaxis.grid(True,which='major',linestyle='-',linewidth=1,color='lightgray',zorder=1)
ax01.yaxis.grid(True,which='minor',linestyle='--',linewidth=0.5,color='lightgray',zorder=1)
plt.show()
fig01 = ax01.get_figure()
fig01.savefig(FolderName+'Outputs/PubCounts_vs_Year.png')
#
# [Fig02] 

#plt.show()
#
#-----------------------------------------------------------------------------
# Extra/Unused (Brainstorming Plots)
#-----------------------------------------------------------------------------
# PubYears - Histogram
#ArticleList_DataFrame['year'].plot.hist(bins=20, title='Article Counts by Year', xlabel='Year')
#plt.show()
# PlotYears - Bar Chart
#year_unique_count.plot.bar(title='Article Counts by Year', xlabel='Year', ylabel='Number of Articles')
#plt.show()
# PlotYears - Scatter Plot
#year_unique_count.scatter(title='Article Counts by Year', xlabel='Year', ylabel='Number of Publications')
#plt.show()
# function to add value labels
##def addlabels(x,y):
##    for i in range(len(x)):
##        plt.text(i, y[i]//2, y[i], ha = 'center')

# PlotCatbyDecade, title='Category Counts by Decade'
#Categories_by_Decade.plot.bar(stacked=True, title='Category Counts by Decade', xlabel='Decade', ylabel='Number of Articles')
#plt.show()
# PlotSiCbyCat, title='SiC Reports by Category'
#SiC_by_Cat.plot.bar(stacked=True, title='SiC Reports by Category', xlabel='Category', ylabel='Number of Articles')
#plt.show()

#-----------------------------------------------------------------------------
# Save all variables:

#-----------------------------------------------------------------------------
# End of File
#-----------------------------------------------------------------------------
