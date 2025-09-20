# -*- coding: utf-8 -*-
"""
File: SiC_analysis_main.py
Created: 2025-SEP-16
@author: Rebecca Frederick
Deku Lab Silicon Carbide Review Data Analysis
Last Updated: 2025-SEP-19 by Rebecca A. Frederick
"""

# Include packages required for data analysis functions:
import os   # used to get current working directory
import pandas as pd   # used to read raw data csv files
import plotly.express as px   # used to create interactive data visualizations
import plotly.graph_objects as go   # used to create interactive data visualizations
import plotly.io as pio  # used for creating plot templates
import matplotlib.pyplot as plt  # used to make static plots
import matplotlib.ticker as ticker # used to setup minor ticks in plots
from statsmodels.graphics.mosaicplot import mosaic  # used for mosaic plots only
from PIL import Image


#-----------------------------------------------------------------------------
#                            DATA ANALYSIS
#-----------------------------------------------------------------------------
# Create, Store, Plot ArticleList Statistics
#-----------------------------------------------------------------------------
def ArticleList_Analysis00a(ArticleList_DF):
    ArticleListDF_skinny = ArticleList_DF.drop(['SiC_label_count','SiC_Type',
                                                  'amorphousSiC','otherSiC',
                                                  'crystalline_other_unspecified',
                                                  'crystalline_3C-SiC',
                                                  'crystalline_4H-SiC',
                                                  'crystalline_6H-SiC',
                                                  'Category_label_count',
                                                  'Category','NeuralEng','Biosensor',
                                                  'Cardiovascular','Orthopedic_Dental',
                                                  'DrugRelease','GeneralImplants_OtherTech',
                                                  'Data_label_count','Data_Reported',
                                                  'InVivo_animal','InVivo_human',
                                                  'MaterialProperties',
                                                  'FabricationMethods',
                                                  'Benchtop','ExVivo',
                                                  'CellCulture_InVitro'],axis=1)
    return ArticleListDF_skinny

#-----------------------------------------------------------------------------
def ArticleList_Analysis00b(ArticleListDF_skinny):
    ArticleListDF_skinny = ArticleListDF_skinny.set_index('refID')
    ArticleListDF_exploded = ArticleListDF_skinny.explode('Reported_Category')
    ArticleListDF_exploded = ArticleListDF_exploded.explode('Reported_SiC')
    ArticleListDF_exploded = ArticleListDF_exploded.explode('Reported_Data')
    ArticleListDF_exploded['Reported_Category'] = ArticleListDF_exploded['Reported_Category'].astype('category')
    ArticleListDF_exploded['Reported_SiC'] = ArticleListDF_exploded['Reported_SiC'].astype('category')
    ArticleListDF_exploded['Reported_Data'] = ArticleListDF_exploded['Reported_Data'].astype('category')
    return ArticleListDF_exploded

#-----------------------------------------------------------------------------
def ArticleList_Analysis01(ArticleList_DF,decade_unique_count):
    #
    NE_by_Year = ArticleList_DF.groupby(['pub_decade'])['NeuralEng'].agg(
        NeuralEngineering = 'sum')
    #    NE_false = lambda x: (~x).sum())
    #    ).reset_index()
    NE_by_Year['decade_end'] = decade_unique_count.decade_end
    NE_by_Year = NE_by_Year.set_index('decade_end',append=True)
    #
    BioSens_by_Year = ArticleList_DF.groupby(['pub_decade'])['Biosensor'].agg(
        Biosensors = 'sum')
    #    BioSens_false = lambda x: (~x).sum())
    #    ).reset_index()
    BioSens_by_Year['decade_end'] = decade_unique_count.decade_end
    BioSens_by_Year = BioSens_by_Year.set_index('decade_end',append=True)
    #
    Cardio_by_Year = ArticleList_DF.groupby(['pub_decade'])['Cardiovascular'].agg(
        Cadiovascular = 'sum')
    #    Cardio_false = lambda x: (~x).sum())
    #    ).reset_index()
    Cardio_by_Year['decade_end'] = decade_unique_count.decade_end
    Cardio_by_Year = Cardio_by_Year.set_index('decade_end',append=True)
    #
    Ortho_by_Year = ArticleList_DF.groupby(['pub_decade'])['Orthopedic_Dental'].agg(
        Orthopedic_or_Dental = 'sum')
    #    Ortho_false = lambda x: (~x).sum())
    #    ).reset_index()
    Ortho_by_Year['decade_end'] = decade_unique_count.decade_end
    Ortho_by_Year = Ortho_by_Year.set_index('decade_end',append=True)
    #
    DrugRel_by_Year = ArticleList_DF.groupby(['pub_decade'])['DrugRelease'].agg(
        DrugRelease = 'sum')
    #    DrugRel_false = lambda x: (~x).sum())
    #    ).reset_index()
    DrugRel_by_Year['decade_end'] = decade_unique_count.decade_end
    DrugRel_by_Year = DrugRel_by_Year.set_index('decade_end',append=True)
    #
    GenImp_by_Year = ArticleList_DF.groupby(['pub_decade'])['GeneralImplants_OtherTech'].agg(
        OtherImplants = 'sum')
    #    GenImp_false = lambda x: (~x).sum())
    #    ).reset_index()
    GenImp_by_Year['decade_end'] = decade_unique_count.decade_end
    GenImp_by_Year = GenImp_by_Year.set_index('decade_end',append=True)
    #
    Categories_by_Year_full = NE_by_Year.join([BioSens_by_Year, Cardio_by_Year, Ortho_by_Year, DrugRel_by_Year, GenImp_by_Year])
    Categories_by_Year = Categories_by_Year_full.reset_index()#.drop(['NE_false','BioSens_false','Cardio_false','Ortho_false','DrugRel_false','GenImp_false'],axis=1)
    Cat_by_Yr_melted = Categories_by_Year.melt(id_vars=['pub_decade','decade_end'],
                                               value_vars=['NeuralEngineering','Biosensors','Cadiovascular','Orthopedic_or_Dental','DrugRelease','OtherImplants'],
                                               var_name='Category',
                                               value_name='Number of Articles')
    #    
    return Cat_by_Yr_melted

#-----------------------------------------------------------------------------
def ArticleList_Analysis02(Cat_by_Yr_melted):
    cat_by_decade_totals = Cat_by_Yr_melted.groupby(['pub_decade','decade_end'])['Number of Articles'].sum().reset_index()
    cat_by_decade_totals['Category'] = ['AllPublications']*6
    cat_by_decade_totals = cat_by_decade_totals[['pub_decade','decade_end','Category','Number of Articles']]
    return cat_by_decade_totals

#-----------------------------------------------------------------------------
def ArticleList_Analysis03(ArticleList_DF):
    Neural_DF = ArticleList_DF.loc[ArticleList_DF["NeuralEng"] == True]
    Biosensor_DF = ArticleList_DF.loc[ArticleList_DF["Biosensor"] == True]
    Cardio_DF = ArticleList_DF.loc[ArticleList_DF["Cardiovascular"] == True]
    Ortho_DF = ArticleList_DF.loc[ArticleList_DF["Orthopedic_Dental"] == True]
    DrugR_DF = ArticleList_DF.loc[ArticleList_DF["DrugRelease"] == True]
    Other_DF = ArticleList_DF.loc[ArticleList_DF["GeneralImplants_OtherTech"] == True]
    #
    ArticleList_Dictionary = {"NeuralEngineering": Neural_DF, "Biosensors": Biosensor_DF, "Cadiovascular": Cardio_DF, "Orthopedic_or_Dental": Ortho_DF, "DrugRelease": DrugR_DF, "OtherImplants": Other_DF}
    #
    return ArticleList_Dictionary

#-----------------------------------------------------------------------------
def ArticleList_Analysis04(ArticleList_DF):
    
    # setup datafram index values / column names:
    index_SiCType = ['a-SiC','3C-SiC','4H-SiC','6H-SiC','Crystalline-Unspecified','Other SiC']
    
    # Pull numbers for DF1 - col 1:
    count_fab_aSiC = ArticleList_DF[(ArticleList_DF['FabricationMethods'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_fab_3C = ArticleList_DF[(ArticleList_DF['FabricationMethods'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_fab_4H = ArticleList_DF[(ArticleList_DF['FabricationMethods'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_fab_6H = ArticleList_DF[(ArticleList_DF['FabricationMethods'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_fab_cryst = ArticleList_DF[(ArticleList_DF['FabricationMethods'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_fab_other = ArticleList_DF[(ArticleList_DF['FabricationMethods'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 2:
    count_mat_aSiC = ArticleList_DF[(ArticleList_DF['MaterialProperties'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_mat_3C = ArticleList_DF[(ArticleList_DF['MaterialProperties'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_mat_4H = ArticleList_DF[(ArticleList_DF['MaterialProperties'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_mat_6H = ArticleList_DF[(ArticleList_DF['MaterialProperties'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_mat_cryst = ArticleList_DF[(ArticleList_DF['MaterialProperties'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_mat_other = ArticleList_DF[(ArticleList_DF['MaterialProperties'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
        
    # Pull numbers for DF1 - col 3:
    count_bench_aSiC = ArticleList_DF[(ArticleList_DF['Benchtop'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_bench_3C = ArticleList_DF[(ArticleList_DF['Benchtop'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_bench_4H = ArticleList_DF[(ArticleList_DF['Benchtop'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_bench_6H = ArticleList_DF[(ArticleList_DF['Benchtop'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_bench_cryst = ArticleList_DF[(ArticleList_DF['Benchtop'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_bench_other = ArticleList_DF[(ArticleList_DF['Benchtop'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 4:
    count_cell_aSiC = ArticleList_DF[(ArticleList_DF['CellCulture_InVitro'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_cell_3C = ArticleList_DF[(ArticleList_DF['CellCulture_InVitro'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_cell_4H = ArticleList_DF[(ArticleList_DF['CellCulture_InVitro'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_cell_6H = ArticleList_DF[(ArticleList_DF['CellCulture_InVitro'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_cell_cryst = ArticleList_DF[(ArticleList_DF['CellCulture_InVitro'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_cell_other = ArticleList_DF[(ArticleList_DF['CellCulture_InVitro'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 5:
    count_exvivo_aSiC = ArticleList_DF[(ArticleList_DF['ExVivo'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_exvivo_3C = ArticleList_DF[(ArticleList_DF['ExVivo'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_exvivo_4H = ArticleList_DF[(ArticleList_DF['ExVivo'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_exvivo_6H = ArticleList_DF[(ArticleList_DF['ExVivo'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_exvivo_cryst = ArticleList_DF[(ArticleList_DF['ExVivo'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_exvivo_other = ArticleList_DF[(ArticleList_DF['ExVivo'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 6:
    count_animal_aSiC = ArticleList_DF[(ArticleList_DF['InVivo_animal'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_animal_3C = ArticleList_DF[(ArticleList_DF['InVivo_animal'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_animal_4H = ArticleList_DF[(ArticleList_DF['InVivo_animal'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_animal_6H = ArticleList_DF[(ArticleList_DF['InVivo_animal'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_animal_cryst = ArticleList_DF[(ArticleList_DF['InVivo_animal'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_animal_other = ArticleList_DF[(ArticleList_DF['InVivo_animal'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 7:
    count_human_aSiC = ArticleList_DF[(ArticleList_DF['InVivo_human'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_human_3C = ArticleList_DF[(ArticleList_DF['InVivo_human'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_human_4H = ArticleList_DF[(ArticleList_DF['InVivo_human'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_human_6H = ArticleList_DF[(ArticleList_DF['InVivo_human'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_human_cryst = ArticleList_DF[(ArticleList_DF['InVivo_human'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_human_other = ArticleList_DF[(ArticleList_DF['InVivo_human'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    
    # create 3 new dataframes (split DF2 & DF3 to functions Analysis05 & Analysis06):
    fab_SiC_col = [count_fab_aSiC,count_fab_3C,count_fab_4H,count_fab_6H,count_fab_cryst,count_fab_other]
    mat_SiC_col = [count_mat_aSiC,count_mat_3C,count_mat_4H,count_mat_6H,count_mat_cryst,count_mat_other]
    bench_SiC_col = [count_bench_aSiC,count_bench_3C,count_bench_4H,count_bench_6H,count_bench_cryst,count_bench_other]
    cell_SiC_col = [count_cell_aSiC,count_cell_3C,count_cell_4H,count_cell_6H,count_cell_cryst,count_cell_other]
    exvivo_SiC_col = [count_exvivo_aSiC,count_exvivo_3C,count_exvivo_4H,count_exvivo_6H,count_exvivo_cryst,count_exvivo_other]
    animal_SiC_col = [count_animal_aSiC,count_animal_3C,count_animal_4H,count_animal_6H,count_animal_cryst,count_animal_other]
    human_SiC_col = [count_human_aSiC,count_human_3C,count_human_4H,count_human_6H,count_human_cryst,count_human_other]
    
    #
    DF1_data = {
        'Fabrication Methods': fab_SiC_col,
        'Material Properties': mat_SiC_col,
        'Benchtop': bench_SiC_col,
        'Cell Culture': cell_SiC_col,
        'Ex Vivo': exvivo_SiC_col,
        'In Vivo Animal': animal_SiC_col,
        'In Vivo Human': human_SiC_col
        }
    #
    DF1 = pd.DataFrame(DF1_data, index=index_SiCType)
    #
    return DF1

#-----------------------------------------------------------------------------
def ArticleList_Analysis05(ArticleList_DF):
    
    # setup datafram index values / column names:
    index_SiCType = ['a-SiC','3C-SiC','4H-SiC','6H-SiC','Crystalline-Unspecified','Other SiC']
    
    # Pull numbers for DF1 - col 1:
    count_neng_aSiC = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_neng_3C = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_neng_4H = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_neng_6H = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_neng_cryst = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_neng_other = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 2:
    count_biosens_aSiC = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_biosens_3C = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_biosens_4H = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_biosens_6H = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_biosens_cryst = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_biosens_other = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
        
    # Pull numbers for DF1 - col 3:
    count_cardio_aSiC = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_cardio_3C = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_cardio_4H = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_cardio_6H = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_cardio_cryst = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_cardio_other = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 4:
    count_ortho_aSiC = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_ortho_3C = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_ortho_4H = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_ortho_6H = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_ortho_cryst = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_ortho_other = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 5:
    count_drug_aSiC = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_drug_3C = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_drug_4H = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_drug_6H = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_drug_cryst = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_drug_other = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 6:
    count_genimplant_aSiC = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['amorphousSiC'] == True)].shape[0]
    count_genimplant_3C = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['crystalline_3C-SiC'] == True)].shape[0]
    count_genimplant_4H = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['crystalline_4H-SiC'] == True)].shape[0]
    count_genimplant_6H = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['crystalline_6H-SiC'] == True)].shape[0]
    count_genimplant_cryst = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['crystalline_other_unspecified'] == True)].shape[0]
    count_genimplant_other = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['otherSiC'] == True)].shape[0]
    
    
    # create 3 new dataframes (split DF2 & DF3 to functions Analysis05 & Analysis06):
    neng_SiC_col = [count_neng_aSiC,count_neng_3C,count_neng_4H,count_neng_6H,count_neng_cryst,count_neng_other]
    biosens_SiC_col = [count_biosens_aSiC,count_biosens_3C,count_biosens_4H,count_biosens_6H,count_biosens_cryst,count_biosens_other]
    cardio_SiC_col = [count_cardio_aSiC,count_cardio_3C,count_cardio_4H,count_cardio_6H,count_cardio_cryst,count_cardio_other]
    ortho_SiC_col = [count_ortho_aSiC,count_ortho_3C,count_ortho_4H,count_ortho_6H,count_ortho_cryst,count_ortho_other]
    drug_SiC_col = [count_drug_aSiC,count_drug_3C,count_drug_4H,count_drug_6H,count_drug_cryst,count_drug_other]
    genimplant_SiC_col = [count_genimplant_aSiC,count_genimplant_3C,count_genimplant_4H,count_genimplant_6H,count_genimplant_cryst,count_genimplant_other]
    
    #
    DF2_data = {
        'Neural Engineering': neng_SiC_col,
        'Biosensors': biosens_SiC_col,
        'Cardiovascular': cardio_SiC_col,
        'Orthopedic or Dental': ortho_SiC_col,
        'Drug Release': drug_SiC_col,
        'Other Implants': genimplant_SiC_col
        }
    #
    DF2 = pd.DataFrame(DF2_data, index=index_SiCType)
    #
    return DF2

#-----------------------------------------------------------------------------
def ArticleList_Analysis06(ArticleList_DF):
    
    # setup datafram index values / column names:
    index_DataType = ['Fabrication Methods', 'Material Properties','Benchtop','Cell Culture','Ex Vivo','In Vivo Animal','In Vivo Human']
    #index_StudyCat = ['Neural Engineering','Biosensors','Cadiovascular','Orthopedic & Dental','Drug Release','Other Implants']
    
    # Pull numbers for DF1 - col 1:
    count_neng_fab = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['FabricationMethods'] == True)].shape[0]
    count_neng_mat = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['MaterialProperties'] == True)].shape[0]
    count_neng_bench = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['Benchtop'] == True)].shape[0]
    count_neng_cell = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['CellCulture_InVitro'] == True)].shape[0]
    count_neng_exvivo = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['ExVivo'] == True)].shape[0]
    count_neng_animal = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['InVivo_animal'] == True)].shape[0]
    count_neng_human = ArticleList_DF[(ArticleList_DF['NeuralEng'] == True) & (ArticleList_DF['InVivo_human'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 2:
    count_biosens_fab = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['FabricationMethods'] == True)].shape[0]
    count_biosens_mat = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['MaterialProperties'] == True)].shape[0]
    count_biosens_bench = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['Benchtop'] == True)].shape[0]
    count_biosens_cell = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['CellCulture_InVitro'] == True)].shape[0]
    count_biosens_exvivo = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['ExVivo'] == True)].shape[0]
    count_biosens_animal = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['InVivo_animal'] == True)].shape[0]
    count_biosens_human = ArticleList_DF[(ArticleList_DF['Biosensor'] == True) & (ArticleList_DF['InVivo_human'] == True)].shape[0]
        
    # Pull numbers for DF1 - col 3:
    count_cardio_fab = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['FabricationMethods'] == True)].shape[0]
    count_cardio_mat = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['MaterialProperties'] == True)].shape[0]
    count_cardio_bench = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['Benchtop'] == True)].shape[0]
    count_cardio_cell = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['CellCulture_InVitro'] == True)].shape[0]
    count_cardio_exvivo = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['ExVivo'] == True)].shape[0]
    count_cardio_animal = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['InVivo_animal'] == True)].shape[0]
    count_cardio_human = ArticleList_DF[(ArticleList_DF['Cardiovascular'] == True) & (ArticleList_DF['InVivo_human'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 4:
    count_ortho_fab = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['FabricationMethods'] == True)].shape[0]
    count_ortho_mat = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['MaterialProperties'] == True)].shape[0]
    count_ortho_bench = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['Benchtop'] == True)].shape[0]
    count_ortho_cell = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['CellCulture_InVitro'] == True)].shape[0]
    count_ortho_exvivo = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['ExVivo'] == True)].shape[0]
    count_ortho_animal = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['InVivo_animal'] == True)].shape[0]
    count_ortho_human = ArticleList_DF[(ArticleList_DF['Orthopedic_Dental'] == True) & (ArticleList_DF['InVivo_human'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 5:
    count_drug_fab = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['FabricationMethods'] == True)].shape[0]
    count_drug_mat = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['MaterialProperties'] == True)].shape[0]
    count_drug_bench = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['Benchtop'] == True)].shape[0]
    count_drug_cell = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['CellCulture_InVitro'] == True)].shape[0]
    count_drug_exvivo = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['ExVivo'] == True)].shape[0]
    count_drug_animal = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['InVivo_animal'] == True)].shape[0]
    count_drug_human = ArticleList_DF[(ArticleList_DF['DrugRelease'] == True) & (ArticleList_DF['InVivo_human'] == True)].shape[0]
    
    # Pull numbers for DF1 - col 6:
    count_genimplant_fab = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['FabricationMethods'] == True)].shape[0]
    count_genimplant_mat = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['MaterialProperties'] == True)].shape[0]
    count_genimplant_bench = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['Benchtop'] == True)].shape[0]
    count_genimplant_cell = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['CellCulture_InVitro'] == True)].shape[0]
    count_genimplant_exvivo = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['ExVivo'] == True)].shape[0]
    count_genimplant_animal = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['InVivo_animal'] == True)].shape[0]
    count_genimplant_human = ArticleList_DF[(ArticleList_DF['GeneralImplants_OtherTech'] == True) & (ArticleList_DF['InVivo_human'] == True)].shape[0]
    
    
    # create 3 new dataframes (split DF2 & DF3 to functions Analysis05 & Analysis06):
    neng_data_col = [count_neng_fab,count_neng_mat,count_neng_bench,count_neng_cell,count_neng_exvivo,count_neng_animal,count_neng_human]
    biosens_data_col = [count_biosens_fab,count_biosens_mat,count_biosens_bench,count_biosens_cell,count_biosens_exvivo,count_biosens_animal,count_biosens_human]
    cardio_data_col = [count_cardio_fab,count_cardio_mat,count_cardio_bench,count_cardio_cell,count_cardio_exvivo,count_cardio_animal,count_cardio_human]
    ortho_data_col = [count_ortho_fab,count_ortho_mat,count_ortho_bench,count_ortho_cell,count_ortho_exvivo,count_ortho_animal,count_ortho_human]
    drug_data_col = [count_drug_fab,count_drug_mat,count_drug_bench,count_drug_cell,count_drug_exvivo,count_drug_animal,count_drug_human]
    genimplant_data_col = [count_genimplant_fab,count_genimplant_mat,count_genimplant_bench,count_genimplant_cell,count_genimplant_exvivo,count_genimplant_animal,count_genimplant_human]
    
    #
    DF3_data = {
        'Neural Engineering': neng_data_col,
        'Biosensors': biosens_data_col,
        'Cardiovascular': cardio_data_col,
        'Orthopedic or Dental': ortho_data_col,
        'Drug Release': drug_data_col,
        'Other Implants': genimplant_data_col
        }
    #
    DF3 = pd.DataFrame(DF3_data, index=index_DataType)
    #
    return DF3

#-----------------------------------------------------------------------------
def Neural_InVivo_Analysis00(Neural_InVivo_DF):
    #
    
    #
    return 


#-----------------------------------------------------------------------------
# END OF FILE
#-----------------------------------------------------------------------------