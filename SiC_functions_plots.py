# -*- coding: utf-8 -*-
"""
File: SiC_analysis_main.py
Created: 2025-SEP-16
@author: Rebecca Frederick
Deku Lab Silicon Carbide Review Data Analysis
Last Updated: 2026-JUl-13 by Rebecca A. Frederick
"""

# Include packages required for data analysis functions:
#import os   # used to get current working directory
import pandas as pd   # used to read raw data csv files
from pandas.api.types import CategoricalDtype
import plotly.express as px   # used to create interactive data visualizations
import plotly.graph_objects as go   # used to create interactive data visualizations
from plotly.subplots import make_subplots
import plotly.io as pio
#import plotly.io as pio  # used for creating plot templates
import matplotlib.pyplot as plt  # used to make static plots
import matplotlib.ticker as ticker # used to setup minor ticks in plots
import numpy as np
from statsmodels.graphics.mosaicplot import mosaic  # used for mosaic plots only
#from PIL import Image

#-----------------------------------------------------------------------------
#                        LIST OF FUNCTIONS IN FILE
#-----------------------------------------------------------------------------
# ArticleList_Plot01
# ArticleList_Plot02
# ArticleList_Plot02b
# ArticleList_Plot02dot  # unused
# ArticleList_Plot03mosaic
# ArticleList_Plot03heat
# ArticleList_Plot03ice
# ArticleList_Plot03sun  # unused
# create_plotly_mosaic  # unused
# ArticleList_Plot04  # unused
# Neural_Plot00
# Neural_Plot01a
# Neural_Plot01b
# Neural_Plot02
# Neural_Plot03


#-----------------------------------------------------------------------------
#                          DATA VISUALIZATIONS
#-----------------------------------------------------------------------------
#print(fig)
#fig.show()
#-----------------------------------------------------------------------------
# [Manuscript Fig] Plots Num. Publications vs. Year Published
def ArticleList_Plot01(SaveLocation,SaveFolderHTML,year_unique_count):
    #-----------------------------------------------------------------------------
    # plot 1
    # !!!!!!! features/formatting to add:
        # color papers with multiple category labels
        # add subplot: 
            # ridgeline; by category, each = pub count (y) vs. time (x)
            # -or- nested circles, each category percentage% vs gray total
            # scale total circle area vs count by decade (see word doc)
    fig0 = px.scatter(year_unique_count,range_x=[1970,2030],range_y=[0,20],
                      title="SiC Publications Over Time")
    fig = go.Figure(fig0)
    fig.update_layout(showlegend=False)
    fig.update_traces(marker=dict(size=12,color='black'))
    fig.update_traces(hovertemplate="Year: %{x} <br> Publications: %{y}<extra></extra>")
    fig.update_xaxes(title='Publication Year',
                     minor=dict(ticks='inside',showgrid=True))
    fig.update_yaxes(title='Number of Articles',
                     minor=dict(ticks='inside',showgrid=True))
    # plot 1 save
    plot01nameh = SaveFolderHTML + "fig_article_gen_count-by-year.html"
    plot01namep = SaveLocation + "fig_article_gen_count-by-year.png"
    plot01names = SaveLocation + "fig_article_gen_count-by-year.svg"
    #
    fig.write_html(plot01nameh,full_html=False)
    fig.write_image(plot01namep)
    fig.write_image(plot01names, format="svg")
    #fig.write_html("Outputs\\fig_article-count-by-year.html",full_html=False)
    #fig.write_image("Outputs\\fig_article-count-by-year.png")
    #
    return 

#-----------------------------------------------------------------------------
# Plots Num. Publications vs. Decade from Year Published
def ArticleList_Plot02(SaveLocation,SaveFolderHTML,c_greys,Cat_by_Yr_melted,cat_by_decade_totals):
    # plot 2
        # !!! in progress list:
            # add total count per decade at top of bars, 
            # change total value with add/remove data series in legend
            # display refID on hover
    # fig0.update_layout(barmode='overlay')
    #fig0.add_trace(px.bar(
    #    x=cat_by_decade_totals['pub_decade'], 
    #    y=cat_by_decade_totals['Number of Articles'],
    #    name='Total Publications',
    #    marker=dict(opacity=0,line=dict(color='black', width=1)),base=0))
    #
    # Define colors to highlight Neural Engineering
    plt2_colors = c_greys[1:8]
    plt2_colors[0] = 'rgb(35,138,141)'
    #
    fig0 = px.bar(Cat_by_Yr_melted, x='pub_decade', y='Number of Articles', 
                  color='Category', color_discrete_sequence=plt2_colors,
                  title="SiC Publications Over Time by Category", 
                  barmode='stack', range_y=[0,100],
                  custom_data=['Category','decade_end'])
    #
    fig = go.Figure(fig0)
    fig.update_xaxes(title='Publication Decade', type='category')
    fig.update_layout(yaxis=dict(dtick=10),
                      legend=dict(orientation="v",yanchor="top",y=0.95,
                                  xanchor="left",x=0.05),
                      legend_title_text=None)
    fig.update_traces(hovertemplate="<b>%{customdata[0]}</b> <br> %{x} to %{customdata[1]} <br> %{y} Publication(s) <extra></extra>")
    #fig.update_layout(hoverlabel=dict(bordercolor='rgba(0,0,0,0)',
    #                                  font=dict(color="white")))
    # plot 2 save
    plot02nameh = SaveFolderHTML + "fig_gen_category-by-decade.html"
    plot02namep = SaveLocation + "fig_gen_category-by-decade.png"
    plot02names = SaveLocation + "fig_gen_category-by-decade.svg"
    #
    fig.write_html(plot02nameh,full_html=False)
    fig.write_image(plot02namep)
    fig.write_image(plot02names, format="svg")
    #fig.write_html("Outputs\\fig_article-category-by-decade.html",full_html=False)
    #fig.write_image("Outputs\\fig_article-category-by-decade.png")
    #
    return 

#-----------------------------------------------------------------------------
# [Manuscript Fig] Plots Num. Publications vs. Decade from Year Published
def ArticleList_Plot02b(SaveLocation,SaveFolderHTML,c_greys,ArticleListDF_exploded):
    # plot 2 version b (after creating ArticleListDF_exploded)
    # !!! in progress list:
        # add total count per decade at top of bars 
        # match formatting to ArticleList_Plot02 function:
            # colors
            # category order
            # legend position
            # axes labels
        
    # Define colors to highlight Neural Engineering
    plt2_colors = c_greys[2:9]
    plt2_colors[0] = 'rgb(35,138,141)'
    #
    #DF_temp = ArticleListDF_exploded.drop(['doi','pubmed_id','title','authors','journal','month','day'],axis=1)
    #DF_info = DF_temp.describe(include=['category'])
    #exclude=['doi','pubmed_id','title','authors','journal','month','day']
    DF_temp = ArticleListDF_exploded.reset_index()
    cat_by_decade_list = DF_temp.groupby(['pub_decade','Reported_Category'],observed=True)['refID'].nunique()
    cat_by_decade_list = cat_by_decade_list.reset_index()
    cat_by_decade_list = cat_by_decade_list.rename(columns={'refID':'Number of Articles'})
    #
    condition = cat_by_decade_list['pub_decade'] == 2020
    val_true = cat_by_decade_list['pub_decade'] + 5
    val_false = cat_by_decade_list['pub_decade'] + 9
    cat_by_decade_list['decade_end'] = np.where(condition, val_true, val_false)
    # Replace category names for plot labels:
    cat_by_decade_list['Reported_Category'] = cat_by_decade_list['Reported_Category'].str.replace('Neural', 'Neural Interfaces')
    #cat_by_decade_list['Reported_Category'] = cat_by_decade_list['Reported_Category'].str.replace('Biosensors', 'Biosensors')
    cat_by_decade_list['Reported_Category'] = cat_by_decade_list['Reported_Category'].str.replace('Cardio', 'Cardiovascular')
    cat_by_decade_list['Reported_Category'] = cat_by_decade_list['Reported_Category'].str.replace('Ortho/Dental', 'Orthopedic/Dental')
    #cat_by_decade_list['Reported_Category'] = cat_by_decade_list['Reported_Category'].str.replace('Drug Release', 'DrugRelease')
    cat_by_decade_list['Reported_Category'] = cat_by_decade_list['Reported_Category'].str.replace('OtherTech', 'Other Implants')
    # Define custom category order:
    decade_order = sorted(cat_by_decade_list['pub_decade'].unique())
    cat_order=['Neural Interfaces','Biosensors','Cardiovascular','Orthopedic/Dental','Drug Release','Other Implants']
    #
    fig0 = px.bar(cat_by_decade_list,x='pub_decade',y='Number of Articles',
                  color='Reported_Category',barmode='stack',
                  #color='Reported_Category',barmode='group',
                  category_orders={"pub_decade": decade_order, "Reported_Category": cat_order},
                  title="SiC Publications Over Time by Category",
                  color_discrete_sequence=plt2_colors,
                  range_y=[0,100],
                  custom_data=['Reported_Category','decade_end'],
                  text_auto=True)
    #
    fig0.update_xaxes(title='Publication Decade', type='category')
    fig0.update_traces(textfont_size=12, textangle=0, insidetextanchor="middle",
                       hovertemplate="<b>%{customdata[0]}</b> <br> %{x} to %{customdata[1]} <br> %{y} Publication(s) <extra></extra>")
    fig0.update_layout(yaxis=dict(dtick=10),
                       uniformtext_minsize=12, uniformtext_mode='show',
                       legend=dict(orientation="v",yanchor="top",y=0.95,
                                   xanchor="left",x=0.05),
                       legend_title_text=None)
    #
    fig = go.Figure(fig0)
    #fig.update_xaxes(title='Publication Decade', type='category')
    #fig.update_layout(yaxis=dict(dtick=10),
    #                  legend=dict(orientation="v",yanchor="top",y=0.95,
    #                              xanchor="left",x=0.05),
    #                  legend_title_text=None)
    #fig.update_traces(hovertemplate="<b>%{Reported_Category}</b> %{x} <br> %{y} Publication(s) <extra></extra>")
    #fig.update_traces(hovertemplate="<b>%{customdata[0]}</b> <br> %{x} to %{customdata[1]} <br> %{y} Publication(s) <extra></extra>")
    #fig.update_layout(hoverlabel=dict(bordercolor='rgba(0,0,0,0)',
    #                                  font=dict(color="white")))
    # plot 2 save
    plot02nameh = SaveFolderHTML + "fig_article_gen_category-by-decade.html"
    plot02namep = SaveLocation + "fig_article_gen_category-by-decade.png"
    plot02names = SaveLocation + "fig_article_gen_category-by-decade.svg"
    #
    fig.write_html(plot02nameh,full_html=False)
    fig.write_image(plot02namep)
    fig.write_image(plot02names, format="svg")
    
    return

#-----------------------------------------------------------------------------
def ArticleList_Plot02dot(SaveLocation,SaveFolderHTML,c_greys,ArticleListDF_exploded):
    # !!! in progress list:
        # TBD
    # plot 2 (circle plot version)
        # plot count of each category vs. decade as separate data series
        # scale area of each circle/datapoint with % of total papers that decade
        # subplot (above) = nested circles, each category % vs gray total
        # scale total circle area vs count by decade
        
    return

#-----------------------------------------------------------------------------
def ArticleList_Plot03mosaic(SaveLocation,SaveFolderHTML,ArticleListDF_exploded):
    # plot 3 (mosaic version)
    # !!! in progress list:
        # remove y-axis labels only
        # change interior labels to y category only (remove study category)
        # set minimum col width / row height (handle 0 values)
        # create the other 2 category comparisons:
            # ['Reported_Category','Reported_Data']
            # ['Reported_SiC','Reported_Data']
    #
    #labelizer=lambda k: ""  # turns labels off
    #labelizer = lambda k: {('a',): 'first', ('b',): 'second', ('c',): 'third'}[k]
    #mosaic(ArticleListDF_exploded, ['Reported_Category','Reported_Data'],
    #       title='Mosaic Plot of Categories vs. Reported Data',
    #       labelizer=None,axes_label=False)
    fig0, ax = mosaic(ArticleListDF_exploded, ['Reported_Category','Reported_SiC'],
           title='Mosaic Plot of Categories vs. SiC Types',
           labelizer=None,gap=0.01,axes_label=True)
    # Turn off the y-axis labels
    #ax.set_ylabel('')
    #ax.set_yticklabels([])
    #ax.set_ylabel('SiC Type')
    #ax.set_xlabel('Publication Category')
    #xlabel='Publication Category',ylabel='SiC Type'
    #ax.set_xticklabels(['Biosensor','Neural','Ortho/Dental',''])
    #mosaic(ArticleListDF_exploded, ['Reported_SiC','Reported_Data'],
    #      title='Mosaic Plot of SiC Type vs Reported Data',
    #      labelizer=None,axes_label=False)
    #fig0, _  = mosaic(ArticleListDF_exploded, ['Reported_SiC','Reported_Data'],
    #                  title='Mosaic Plot of SiC Publications',
    #                  labelizer=None,axes_label=False)
    #fig0 = mosaic(ArticleListDF_exploded, ['Reported_Category','Reported_SiC','Reported_Data'])
    #
    # plot 3 mosaic save
    plot03nameh = SaveFolderHTML + "fig_gen_mosaic-SiC-publications.html"
    plot03namep = SaveLocation + "fig_gen_mosaic-SiC-publications.png"
    plot03names = SaveLocation + "fig_gen_mosaic-SiC-publications.svg"
    plt.savefig(plot03nameh)
    plt.savefig(plot03namep)
    plt.savefig(plot03names, format="svg")
    plt.show()
    #
    #fig = go.Figure(plt)
    #plot03nameh = SaveLocation + "fig_mosaic-SiC-publications.html"
    #fig.write_html(plot03nameh,full_html=False)
    #
    #fig0.savefig(plot03namep)
    #
    #image = Image.open(plot03namep)
    #fig = go.Figure(go.Image(z=image))
    #fig.update_layout(
    #title='Static Mosaic Plot in Plotly HTML',
    #xaxis_visible=False,
    #yaxis_visible=False)
    #
    #fig.write_html(plot03nameh,full_html=False)
    #
    return

#-----------------------------------------------------------------------------
# [Manuscript Fig] Plots heatmap Device Category vs. SiC Type
def ArticleList_Plot03heatA(SaveLocation,SaveFolderHTML,ArticleListDF_exploded):
    # plot 3 (heatmap version)
    # !!! in progress list:
        # [ ] correlate heatmap color range for A, B, and C figures
    #
    #
    heat_vals = ArticleListDF_exploded.reset_index().groupby(['Reported_Category','Reported_SiC'],observed=False)['refID'].nunique().reset_index()
    #
    target_r6 = ['a-SiC']
    target_r5 = ['3C-SiC']
    target_r4 = ['4H-SiC']
    target_r3 = ['6H-SiC']
    target_r2 = ['Crystalline']
    target_r1 = ['Other']
    #
    heat_row_aSiC = heat_vals.loc[heat_vals['Reported_SiC'].isin(target_r6)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    heat_row_3C = heat_vals.loc[heat_vals['Reported_SiC'].isin(target_r5)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    heat_row_4H = heat_vals.loc[heat_vals['Reported_SiC'].isin(target_r4)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    heat_row_6H = heat_vals.loc[heat_vals['Reported_SiC'].isin(target_r3)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    heat_row_cr = heat_vals.loc[heat_vals['Reported_SiC'].isin(target_r2)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    heat_row_other = heat_vals.loc[heat_vals['Reported_SiC'].isin(target_r1)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    #
    heat_vals_arranged = [heat_row_other,heat_row_cr,heat_row_6H,heat_row_4H,heat_row_3C,heat_row_aSiC]
    #
    fig0 = px.imshow(heat_vals_arranged, text_auto=True, zmin=0, zmax=66, 
                     aspect = 'equal',
                     title="Type of SiC<br>vs. Publication Category",
                     labels=dict(#x="Publication Category",
                                 #y="Type of SiC Reported",
                                 color="Count"),
                     x=['Biosensors','Cardio','Drug Release','Neural','Ortho/Dental','OtherTech'],
                     y=['Other','Crystalline','6H-SiC','4H-SiC','3C-SiC','a-SiC']
                     )
    
    # Increase left and bottom margins to fit long labels
    #
    cell_size = 80
    #margin_size = 100
    #
    fig0.update_layout(
        margin=dict(l=140, r=20, b=120, t=100),
        width=(len(heat_vals_arranged[0])*cell_size),
        height=(len(heat_vals_arranged[0])*cell_size)
        )
    # force x labels angle
    fig0.update_xaxes(tickangle=-45, automargin=False)
    fig0.update_yaxes(tickangle=0, automargin=False)
    #Custom colorbar labels to include max value = 66
        # hard-coded max, future update = dynamic max value from data
    fig0.update_coloraxes(
        colorbar_tickvals=[0,10,20,30,40,50,60,66]
        )
    #
    fig = go.Figure(fig0)
    
    # plot 3 heatmap save
    plot03nameh = SaveFolderHTML + "fig_article_gen_heatmapA-SiC-publications.html"
    plot03namep = SaveLocation + "fig_article_gen_heatmapA-SiC-publications.png"
    plot03names = SaveLocation + "fig_article_gen_heatmapA-SiC-publications.svg"
    #
    fig.write_html(plot03nameh,full_html=False)
    fig.write_image(plot03namep)
    fig.write_image(plot03names, format="svg")
    #
    return 

#-----------------------------------------------------------------------------
# [Manuscript Fig] plots heatmap Device Category vs. Data Type
def ArticleList_Plot03heatB(SaveLocation,SaveFolderHTML,ArticleListDF_exploded):
    # plot 3 (heatmap version)
    # !!! in progress list:
        # [ ] correlate heatmap color range for A, B, and C figures
    #
    heat_vals = ArticleListDF_exploded.reset_index().groupby(['Reported_Category','Reported_Data'],observed=False)['refID'].nunique().reset_index()
    #
    target_r7 = ['Fabrication']
    target_r6 = ['Material Properties']
    target_r5 = ['Benchtop']
    target_r4 = ['In Vitro']
    target_r3 = ['Ex Vivo']
    target_r2 = ['Animal']
    target_r1 = ['Human']
    #
    
    # Fab
    heat_row_7 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r7)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    # Mat Prop
    heat_row_6 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r6)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    # Bench
    heat_row_5 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r5)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    # In Vitro
    heat_row_4 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r4)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    # Ex Vivo
    heat_row_3 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r3)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    # Animal
    heat_row_2 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r2)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    # Human
    heat_row_1 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r1)
                                  ].sort_values(
                                      by='Reported_Category',
                                      ascending=True
                                      )['refID'].tolist()
    #
    heat_vals_arranged = [heat_row_7,heat_row_6,heat_row_5,heat_row_4,heat_row_3,heat_row_2,heat_row_1]
    #
    fig0 = px.imshow(heat_vals_arranged, text_auto=True, zmin=0, zmax=66, 
                     aspect = 'equal', 
                     title="Type of Data<br>vs. Publication Category",
                     labels=dict(#x="Publication Category",
                                 #y="Type of Data Reported",
                                 color="Count"),
                     x=['Biosensors','Cardio','Drug Release','Neural','Ortho/Dental','OtherTech'],
                     y=['Fabrication','Mat. Prop.','Benchtop','In Vitro','Ex Vivo','Animal','Human']
                     )
    
    # Increase left and bottom margins to fit long labels
    #
    cell_size = 80
    #margin_size = 100
    #
    fig0.update_layout(
        margin=dict(l=140, r=20, b=120, t=100),
        width=(len(heat_vals_arranged[0])*cell_size),
        height=(len(heat_vals_arranged[0])*cell_size)
        )
    # force x labels angle
    fig0.update_xaxes(tickangle=-45, automargin=False)
    fig0.update_yaxes(tickangle=0, automargin=False)
    #Custom colorbar labels to include max value = 66
        # hard-coded max, future update = dynamic max value from data
    fig0.update_coloraxes(
        colorbar_tickvals=[0,10,20,30,40,50,60,66]
        )
    #
    fig = go.Figure(fig0)
    # plot 3 heatmap save
    plot03nameh = SaveFolderHTML + "fig_article_gen_heatmapB-SiC-publications.html"
    plot03namep = SaveLocation + "fig_article_gen_heatmapB-SiC-publications.png"
    plot03names = SaveLocation + "fig_article_gen_heatmapB-SiC-publications.svg"
    #
    fig.write_html(plot03nameh,full_html=False)
    fig.write_image(plot03namep)
    fig.write_image(plot03names, format="svg")
    #
    return 

#-----------------------------------------------------------------------------
# [Manuscript Fig] plots heatmap SiC type vs. Data type
def ArticleList_Plot03heatC(SaveLocation,SaveFolderHTML,ArticleListDF_exploded):
    # plot 3 (heatmap version)
    # !!! in progress list:
        # [] make order of SiC categories match Plot03heatA
    #
    heat_vals_start = ArticleListDF_exploded.reset_index().groupby(['Reported_SiC','Reported_Data'],observed=False)['refID'].nunique().reset_index()
    heat_vals = pd.concat([
        heat_vals_start.iloc[35:42],    # put a-SiC rows at start
        heat_vals_start.iloc[:35],      # add all other rows in default order
                           ]).reset_index(drop=True)
    #sort_SiC_order = CategoricalDtype(['a-SiC', '3C-SiC', '4H-SiC', '6H-SiC', 'Crystalline', 'Other'], ordered=True)
    #heat_vals['Reported_SiC'] = heat_vals['Reported_SiC'].astype(sort_SiC_order)
    #
    target_r7 = ['Fabrication']
    target_r6 = ['Material Properties']
    target_r5 = ['Benchtop']
    target_r4 = ['In Vitro']
    target_r3 = ['Ex Vivo']
    target_r2 = ['Animal']
    target_r1 = ['Human']
    #
    
    # Fab
    heat_row_7 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r7)
                                  ].sort_values(
                                      by='Reported_SiC',
                                      ascending=False
                                      )['refID'].tolist()
    # Mat Prop
    heat_row_6 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r6)
                                  ].sort_values(
                                      by='Reported_SiC',
                                      ascending=False
                                      )['refID'].tolist()
    # Bench
    heat_row_5 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r5)
                                  ].sort_values(
                                      by='Reported_SiC',
                                      ascending=False
                                      )['refID'].tolist()
    # In Vitro
    heat_row_4 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r4)
                                  ].sort_values(
                                      by='Reported_SiC',
                                      ascending=False
                                      )['refID'].tolist()
    # Ex Vivo
    heat_row_3 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r3)
                                  ].sort_values(
                                      by='Reported_SiC',
                                      ascending=False
                                      )['refID'].tolist()
    # Animal
    heat_row_2 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r2)
                                  ].sort_values(
                                      by='Reported_SiC',
                                      ascending=False
                                      )['refID'].tolist()
    # Human
    heat_row_1 = heat_vals.loc[heat_vals['Reported_Data'].isin(target_r1)
                                  ].sort_values(
                                      by='Reported_SiC',
                                      ascending=False
                                      )['refID'].tolist()
    #
    heat_vals_arranged = [heat_row_7,heat_row_6,heat_row_5,heat_row_4,heat_row_3,heat_row_2,heat_row_1]
    #
    fig0 = px.imshow(heat_vals_arranged, text_auto=True, zmin=0, zmax=66, 
                     aspect = 'equal',
                     title="Type of Data<br>vs. Type of SiC",
                     labels=dict(#x="Type of SiC Reported",
                                 #y="Type of Data Reported",
                                 color="Count"),
                     x=['a-SiC','3C-SiC','4H-SiC','6H-SiC','Crystalline','Other'],
                     y=['Fabrication','Mat. Prop.','Benchtop','In Vitro','Ex Vivo','Animal','Human']
                     )
    
    # Increase left and bottom margins to fit long labels
    #
    cell_size = 80
    #margin_size = 100
    #
    fig0.update_layout(
        margin=dict(l=140, r=20, b=120, t=100),
        width=(len(heat_vals_arranged[0])*cell_size),
        height=(len(heat_vals_arranged[0])*cell_size)
        )
    # force x labels angle
    fig0.update_xaxes(tickangle=-45, automargin=False)
    fig0.update_yaxes(tickangle=0, automargin=False)
    #Custom colorbar labels to include max value = 66
        # hard-coded max, future update = dynamic max value from data
    fig0.update_coloraxes(
        colorbar_tickvals=[0,10,20,30,40,50,60,66]
        )
    #
    fig = go.Figure(fig0)
    # plot 3 heatmap save
    plot03nameh = SaveFolderHTML + "fig_article_gen_heatmapC-SiC-publications.html"
    plot03namep = SaveLocation + "fig_article_gen_heatmapC-SiC-publications.png"
    plot03names = SaveLocation + "fig_article_gen_heatmapC-SiC-publications.svg"
    #
    fig.write_html(plot03nameh,full_html=False)
    fig.write_image(plot03namep)
    fig.write_image(plot03names, format="svg")
    #
    return 

#-----------------------------------------------------------------------------
def ArticleList_Plot03ice(SaveLocation,SaveFolderHTML,ArticleListDF_exploded):
    # plot 3 (icicle version)
    # !!! in progress list:
        # fix counts ! (use groupby? or reset index?)
        # match colors to Plot 2 palette?
    #
    #ALdf_counts = ArticleListDF_exploded.groupby(['Reported_Category', 'Reported_SiC', 'Reported_Data']).size().reset_index(name='publications_count')
    fig0 = px.icicle(ArticleListDF_exploded,
                     path=[px.Constant("All SiC Publications"),
                           'Reported_Category',
                           'Reported_SiC',
                           'Reported_Data'])
    fig0.update_traces(tiling_orientation='v',root_color="black",
                       textfont=dict(color='white'))
    fig = go.Figure(fig0)
    #fig = go.Figure(
    #    go.Icicle(
    #        ids = ArticleListDF_exploded.Reported_Category,
    #        labels = ArticleListDF_exploded.Reported_Data,
    #        parents = ArticleListDF_exploded.Reported_SiC,
    #        root_color="lightgrey",
    #        tiling = dict(
    #            orientation='v'
    #        )
    #    )
    #)
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    #
    # plot 3 icicle save
    plot03nameh = SaveFolderHTML + "fig_icicle-SiC-publications.html"
    plot03namep = SaveLocation + "fig_icicle-SiC-publications.png"
    plot03names = SaveLocation + "fig_icicle-SiC-publications.svg"
    #
    fig.write_html(plot03nameh,full_html=False)
    fig.write_image(plot03namep)
    fig.write_image(plot03names, format="svg")
    #
    return 

#-----------------------------------------------------------------------------
def ArticleList_Plot03sun(SaveLocation,SaveFolderHTML,ArticleListDF_exploded):
    # !!!  in progress list:
        # ???
    # plot 3 (sunburst version)
    
    return

#-----------------------------------------------------------------------------
def create_plotly_mosaic(df, index, colors):
    # !!! in progress list:
        # fix counts?
        # 
    
    fig = go.Figure()
    
    # Calculate widths and positions based on the first categorical variable
    total_count = df.groupby(index[0]).size().sum()
    widths = df.groupby(index[0]).size() / total_count
    x_positions = widths.cumsum() - widths/2
    
    # Create the stacked bar chart
    last_y_pos = pd.DataFrame(0, index=df[index[0]].unique(), columns=['y_start'])

    for j, (col_val, df_col) in enumerate(df.groupby(index[1])):
        for i, (row_val, df_row) in enumerate(df_col.groupby(index[0])):
            
            # Calculate height and position for each tile
            count = len(df_row)
            height = count / (widths.loc[row_val] * total_count)
            y_start = last_y_pos.loc[row_val, 'y_start']
            
            fig.add_trace(go.Bar(
                x=[x_positions.loc[row_val]],
                y=[height],
                width=[widths.loc[row_val]],
                marker_color=colors[j],
                name=f'{index[0]}: {row_val}, {index[1]}: {col_val}',
                hovertemplate=f"<b>{index[0]}</b>: {row_val}<br>"
                              f"<b>{index[1]}</b>: {col_val}<br>"
                              f"<b>Count</b>: {count}<br>"
                              f"<extra></extra>"
            ))
            last_y_pos.loc[row_val, 'y_start'] += height
            
    # Update layout for a clean mosaic look
    fig.update_layout(
        barmode='stack',
        title=f'Mosaic Plot of {index[0]} vs {index[1]}',
        xaxis_title=index[0],
        yaxis_title="Proportional Frequency",
        xaxis={'tickvals': x_positions, 'ticktext': widths.index},
        yaxis={'tickformat': '.0%'},
        bargap=0,
        showlegend=True
    )
    
    return fig

#-----------------------------------------------------------------------------
# [Manuscript Fig] Plots SiC Type vs Data Type Reported
def ArticleList_Plot04(SaveLocation,SaveFolderHTML,DF1,DF2,DF3):    
    # !!! in progress list:
        # see: https://plotly.com/python/parallel-categories-diagram/
            # Parallel Categories with Multi-Color Linked Brushing
        # see: https://plotly.com/python/icicle-charts/
            # Down Direction (Icicle)
    fig0 = px.scatter(DF1,
                      title="SiC Types vs. Data Reported")
    fig = go.Figure(fig0)
    fig.update_layout(showlegend=False)
    fig.update_traces(marker=dict(size=10,color='black'))
    fig.update_traces(hovertemplate="Year: %{x} <br> Publications: %{y}<extra></extra>")
    fig.update_xaxes(title='Publication Year',
                     minor=dict(ticks='inside',showgrid=True))
    fig.update_yaxes(title='Number of Articles')
    # plot 1 save
    plot01nameh = SaveFolderHTML + "fig_article_gen_SiCtype-by-DataReported.html"
    plot01namep = SaveLocation + "fig_article_gen_SiCtype-by-DataReported.png"
    plot01names = SaveLocation + "fig_article_gen_SiCtype-by-DataReported.svg"
    #
    fig.write_html(plot01nameh,full_html=False)
    fig.write_image(plot01namep)
    fig.write_image(plot01names, format="svg")
    #fig.write_html("Outputs\\fig_article-count-by-year.html",full_html=False)
    #fig.write_image("Outputs\\fig_article-count-by-year.png")
    #
    return 




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#-----------------------------------------------------------------------------
# NEURAL INTERFACE CATEGORY DATA:
#-----------------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# [Manuscript Fig] Plots all in vivo data subject statistics
def Neural_Plot00T(SaveLocation,SaveFolderHTML,Neural_InVivo_DF01_Selected):
    
    #Option 1 = Plot All Data Separately/Overlayed
    inputDF = Neural_InVivo_DF01_Selected
    #-------------------------------------------------------------------------
    # create figure
    fig = go.Figure()

    #-------------------------------------------------------------------------
    # add table to figure...
    #-------------------------------------------------------------------------

    # (table) "SiC Use in Neuro: In Vivo Experiments Overview"
    fig0t = go.Table(
        header=dict(values=list(inputDF.columns)),
        cells=dict(values=[inputDF[cols] for cols in inputDF.columns])
        )
    fig.add_trace(fig0t)
    #-------------------------------------------------------------------------
    # update formatting for the whole figure:
    fig.update_layout(title_text='SiC Use in Neuro: In Vivo Experiments Data',  #height=1200
                      )
    for trace in fig.data:
        if isinstance(trace, go.Table):
            # Update header properties for all tables
            trace.header.update(
                font=dict(family="Arial", size=12, color="black"),
                fill_color='lightgray', # Apply a consistent color
                height=26
            )
            # Update cells properties for all tables
            trace.cells.update(
                font=dict(family="Arial", size=10, color="black"),
                #fill_color='rgb(245,245,245)', # Apply a consistent color
                height=26
            )
    #-------------------------------------------------------------------------
    # plot save
    NEplot00Tnameh = SaveFolderHTML + "fig_article_InVivo_data.html"
    NEplot00Tnamep = SaveLocation + "fig_article_InVivo_data.png"
    NEplot00Tnames = SaveLocation + "fig_article_InVivo_data.svg"
    #
    fig.write_html(NEplot00Tnameh,full_html=False)
    fig.write_image(NEplot00Tnamep)
    fig.write_image(NEplot00Tnames, format="svg")
    
    return 

#-----------------------------------------------------------------------------
# [Manuscript Fig] Plots all in vivo data subject statistics
def Neural_Plot00(SaveLocation,SaveFolderHTML,Neural_InVivo_DF01_Selected):
#!!! in-progress list:
    # [ ] adjust spacing/widths inside box plot
    # [X] split main data table to separate file & fix formatting
    
    # define colors for plotting
    species_colors = {'Rat':'orange',
                      'Mouse':'red',
                      'Rabbit':'yellow',
                      'Zebra Finch':'green',
                      'Pig':'blue',
                      'Non-Human Primate':'gray',
                      'Human':'black'}
    #Option 1 = Plot All Data Separately/Overlayed
    inputDF = Neural_InVivo_DF01_Selected
    #-------------------------------------------------------------------------
    # create subplots layout for figure
    fig = go.Figure()
    fig = make_subplots(
        rows=2, cols=3,
        vertical_spacing=0.08,
        horizontal_spacing=0.04,
        specs=[
           [{"colspan":2,"type":"box"}, None, {"type":"table"}],  # row info
           [{"type":"table"}, {"type":"table"}, {"type":"table"}]  # row info
           ],
        subplot_titles=("","Number of Subjects","Study Duration (Days)",
                        "Implanted Devices per Subject","Number of Implanted Devices")
        )
    #-------------------------------------------------------------------------
    # add traces to figure...
    #-------------------------------------------------------------------------
    # ROW 1 COL 1-2 = (boxplot) "Study Subjects Counts by Gender & Species"
    # see https://plotly.com/python/box-plots/ for more info on box plots
    # create figure:
    fig1 = px.box(inputDF,
                  x="Sex",
                  y="SubjectCount",
                  color="Sex",
                  #color="Species",
                  #boxmode="group",
                  points="all",
                  hover_data=["Species","ReferenceID"],
                  )
    # add to subplot figure object:
    fig.add_traces(fig1.data, rows=1, cols=1)
    fig.update_traces(row=1, col=1, boxmean=True, line_width=2)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(row=1, col=1, categoryorder='category ascending')
    fig.update_yaxes(row=1, col=1, title_text="Number of Subjects")
    #-------------------------------------------------------------------------
    # (tables) SubjectCount, Devices_total, Implant_Duration_days
    # Total, Avg., Std.Dev., Max., Min. Values
    # reduce dataframe:
    subsetinputDF = inputDF[['ReferenceID','SubjectCount','Species','Strain',
                            'Sex','Age','Implant_Region','Implant_Location',
                            'Device_Category','Devices_per_subject','Devices_total',
                            'Devices_per_subject_average',
                            'Implant_Duration_days',
                            'Implant_Duration_weeks']]
    # replace Non-Human Primate with NHP for shorter label in figure tables:
    tempcat = subsetinputDF.loc[:,"Species"].astype('category')
    subsetinputDF.loc[:,"Species"] = tempcat.cat.rename_categories({"Non-Human Primate":"NHP","Zebra Finch":"ZF"})
    # stats for only SubjectCount column:
    inputDFstats_subj = subsetinputDF.groupby(['Species'],observed=True).agg(
        #
        Total=('SubjectCount','sum'),
        Max=('SubjectCount','max'),
        Min=('SubjectCount','min'),
        Avg=('SubjectCount','mean'),
        #StdDev=('SubjectCount','std'),   # not calculating correctly, TBD
        #
        ).reset_index()
    inputDFstats_subj = inputDFstats_subj.round(2)
    # stats for only Devices_per_subject_average column:
    inputDFstats_devices = subsetinputDF.groupby(['Species'],observed=True).agg(
        #
        Max=('Devices_per_subject_average','max'),
        Min=('Devices_per_subject_average','min'),
        Avg=('Devices_per_subject_average','mean'),
        #StdDev=('Devices_per_subject_average','stddev'),
        #
        ).reset_index()
    inputDFstats_devices = inputDFstats_devices.round(2)
    # stats for only Devices_total column:
    inputDFstats_devicesT = subsetinputDF.groupby(['Species'],observed=True).agg(
        #
        Total=('Devices_total','sum'),
        Max=('Devices_total','max'),
        Min=('Devices_total','min'),
        Avg=('Devices_total','mean'),
        #StdDev=('Devices_total','stddev'),
        #
        ).reset_index()
    inputDFstats_devicesT = inputDFstats_devicesT.round(2)
    # stats for only Implant_Duration_days column:
    inputDFstats_duration = subsetinputDF.groupby(['Species'],observed=True).agg(
        #
        #Total=('Implant_Duration_days','sum'),
        Max=('Implant_Duration_days','max'),
        Min=('Implant_Duration_days','min'),
        Avg=('Implant_Duration_days','mean'),
        #StdDev=('Implant_Duration_days','stddev'),
        #
        ).reset_index()
    inputDFstats_duration = inputDFstats_duration.round(2)
    # create holder for data values for each of the 4 tables to display:
    datavals_subj = [inputDFstats_subj[col].tolist() for col in inputDFstats_subj.columns]
    datavals_devices = [inputDFstats_devices[col].tolist() for col in inputDFstats_devices.columns]
    datavals_devicesT = [inputDFstats_devicesT[col].tolist() for col in inputDFstats_devicesT.columns]
    datavals_duration = [inputDFstats_duration[col].tolist() for col in inputDFstats_duration.columns]
    #-------------------------------------------------------------------------
    # ROW 1 COL 3 = Table for SubjectCount data
    fig2 = go.Table(
        header=dict(values=list(inputDFstats_subj.columns)),
        cells=dict(values=datavals_subj),
        )
    fig.add_traces(fig2, rows=1,cols=3)
    #-------------------------------------------------------------------------
    # ROW 2 COL 1 = Table for Implant_Duration_days data
    fig3 = go.Table(
        header=dict(values=list(inputDFstats_duration.columns)),
        cells=dict(values=datavals_duration),
        )
    fig.add_traces(fig3, rows=2,cols=1)
    #-------------------------------------------------------------------------
    # ROW 2 COL 2 = Table for Devices_per_subject_average data
    fig4 = go.Table(
        header=dict(values=list(inputDFstats_devices.columns)),
        cells=dict(values=datavals_devices),
        )
    fig.add_traces(fig4, rows=2,cols=2)
    #-------------------------------------------------------------------------
    # ROW 2 COL 3 = Table for Devices_total data
    fig5 = go.Table(
        header=dict(values=list(inputDFstats_devicesT.columns)),
        cells=dict(values=datavals_devicesT),
        )
    fig.add_traces(fig5, rows=2,cols=3)

    #-------------------------------------------------------------------------
    # update formatting for the whole figure:
    fig.update_layout(title_text='SiC Use in Neuro: In Vivo Experiments Overview',
                      width=1200, height=690, 
                      margin=dict(
                          b=0,  # bottom margin
                          pad=0   # padding
                          ),
                      font=dict(size=16)
                      )
    for trace in fig.data:
        if isinstance(trace, go.Table):
            # Update header properties for all tables
            trace.header.update(
                #font=dict(size=12), #family="Arial",color="white"
                fill_color='lightgray', # Apply a consistent color
                height=30
            )
            # Update cells properties for all tables
            trace.cells.update(
                #font=dict(size=12), #family="Arial",color="white"
                #fill_color='rgb(245,245,245)', # Apply a consistent color
                height=30
            )
    #-------------------------------------------------------------------------
    # plot save
    NEplot00nameh = SaveFolderHTML + "fig_article_InVivo_overview.html"
    NEplot00namep = SaveLocation + "fig_article_InVivo_overview.png"
    NEplot00names = SaveLocation + "fig_article_InVivo_overview.svg"
    #
    fig.write_html(NEplot00nameh,full_html=False)
    fig.write_image(NEplot00namep)
    fig.write_image(NEplot00names, format="svg")
    
    return 

#-----------------------------------------------------------------------------
# Plots implant duration vs. tissue location (each study separately)
def Neural_Plot01a(SaveLocation,SaveFolderHTML,bubblesizeunit,Neural_InVivo_DF01_Selected):
#!!! in-progress list:
    # [ ] add minor ticks to both axes
    # [ ] move legend to top, with horizontal orientation
    # [ ] add color coding scheme for species
    # [ ] add legend for smallest value & largest value circle size ???
    # [ ] add background color for each Implant Region column ???

#Option 1 = Plot All Data Separately/Overlayed
    inputDF = Neural_InVivo_DF01_Selected

#Define Circle Area
    #bubblesizeunit = 2.*max(Neural_InVivo_DF01_Selected['SubjectCount'])/(40**2)  # define range of bubble sizes'
        # To scale the bubble size, use the attribute sizeref. 
        # We recommend using the following formula to calculate a sizeref value:
        # sizeref = 2. * max(array of size values) / (desired maximum marker size ** 2)
    # Create stand-along scatter plots
    fig00 = px.scatter(inputDF,
        y="Implant_Duration_days",
        x="Implant_Region",
        color="Species",      # legend categories = species
        #symbol="Species",    # !!! update with animal icons?
        size='SubjectCount',  # Make marker size proportional to number of subjects
        #text="SubjectCount",  # label each bubble with subject count
        category_orders={"Species": ['Rat', 'Mouse', 'Zebra Finch', 'Rabbit', 'Pig', 'Non-Human Primate', 'Human'],
                         "Implant_Region": ['Brain','Nerve','Eye','Skin']}, # Explicitly set custom order
        hover_data=['ReferenceID','Strain', 'Sex', 'Implant_Location', 'SubjectCount']
        )
    #
    fig = go.Figure(fig00)
    fig.update_traces(marker=dict(sizemode='area',
                                  sizeref=bubblesizeunit,
                                  opacity=0.6,
                                  line=dict(width=1,color='black')
                                  ),
                      selector=dict(mode='markers'),
                      #textposition='inside',
                      #textfont_size=(bubblesizeunit/10),
                      )
    fig.update_layout(scattermode='group',scattergap=0.8,
                      title_text='Study Duration vs. Implant Region')
    fig.update_xaxes(title_text='Implant Region')
    fig.update_yaxes(title_text='Implant Study Duration (days)',
                     range=[-30,240])

    # plot save
    NEplot01anameh = SaveFolderHTML + "fig_InVivo_duration-vs-region-individual.html"
    NEplot01anamep = SaveLocation + "fig_InVivo_duration-vs-region-individual.png"
    NEplot01anames = SaveLocation + "fig_InVivo_duration-vs-region-individual.svg"
    #
    fig.write_html(NEplot01anameh,full_html=False)
    fig.write_image(NEplot01anamep)
    fig.write_image(NEplot01anames, format="svg")
    return

#-----------------------------------------------------------------------------
# [Manuscript Fig] Plots implant duration vs. tissue location
def Neural_Plot01b(SaveLocation,SaveFolderHTML,bubblesizeunit,Neural_InVivo_DF01_Selected):
#!!! in-progress list:
    # [ ] add minor ticks to both axes
    # [ ] move legend to top, with horizontal orientation
    # [ ] add color coding scheme for species
    # [ ] add legend for smallest value & largest value circle size ???
    # [ ] add background color for each Implant Region column ???
    
#Option 2 = Group first, then plot
    inputDF = Neural_InVivo_DF01_Selected.groupby(['Implant_Region','Species','Implant_Duration_days'],
                                                  as_index=False,
                                                  observed=True)['SubjectCount'].sum()
#Define Circle Area
    # define range of bubble sizes', 
    # scale to match max subject count = 8 in split 
    # vs. max subject count = 26 when grouped
    #bubblesizeunit = 2.*max(Neural_InVivo_DF01_Selected['SubjectCount'])/(40**2)  # define range of bubble sizes'
        # To scale the bubble size, use the attribute sizeref. 
        # We recommend using the following formula to calculate a sizeref value:
        # sizeref = 2. * max(array of size values) / (desired maximum marker size ** 2)
    # Create stand-along scatter plots
    fig00 = px.scatter(inputDF,
        y="Implant_Duration_days",
        x="Implant_Region",
        color="Species",      # legend categories = species
        #symbol="Species",    # !!! update with animal icons?
        size='SubjectCount',  # Make marker size proportional to number of subjects
        #text="SubjectCount",  # label each bubble with subject count
        category_orders={"Species": ['Rat', 'Mouse', 'Zebra Finch', 'Rabbit', 'Pig', 'Non-Human Primate', 'Human'],
                         "Implant_Region": ['Brain','Nerve','Eye','Skin']}, # Explicitly set custom order
        #hover_data=['Strain', 'Sex', 'Implant_Location', 'SubjectCount']
        )
    #
    fig = go.Figure(fig00)
    fig.update_traces(marker=dict(sizemode='area',
                                  sizeref=bubblesizeunit,
                                  opacity=0.8,
                                  line=dict(width=1,color='black')
                                  ),
                      selector=dict(mode='markers'),
                      #textposition='inside',
                      #textfont_size=(bubblesizeunit/10),
                      )
    fig.update_layout(scattermode='group',scattergap=0.8,
                      title_text='Study Duration vs. Implant Region')
    fig.update_xaxes(title_text='Implant Region')
    fig.update_yaxes(title_text='Implant Study Duration (Days)',
                     range=[-30,240])

    # plot save
    NEplot01bnameh = SaveFolderHTML + "fig_article_InVivo_duration-vs-region-grouped.html"
    NEplot01bnamep = SaveLocation + "fig_article_InVivo_duration-vs-region-grouped.png"
    NEplot01bnames = SaveLocation + "fig_article_InVivo_duration-vs-region-grouped.svg"
    #
    fig.write_html(NEplot01bnameh,full_html=False)
    fig.write_image(NEplot01bnamep)
    fig.write_image(NEplot01bnames, format="svg")
    
    return

#-----------------------------------------------------------------------------
# [Manuscript Fig] Plots num. devices per subject vs. implant duration
def Neural_Plot02(SaveLocation,SaveFolderHTML,bubblesizeunit,Neural_InVivo_DF01_Selected):
#!!! in-progress list:
    # [ ] add minor ticks to both axes
    # [X] swap Device_ID with Device_Category
    # [ ] move legend to top, with horizontal orientation
    # [ ] add color coding scheme for device categories
    # [ ] add legend for smallest value & largest value circle size ???
    
#Option 2 = Group first, then plot
    Neural_InVivo_DF01_Selected = Neural_InVivo_DF01_Selected.rename(columns={
                                  'Device_Category':'Device Category'})
    inputDF = Neural_InVivo_DF01_Selected.groupby(['Implant_Duration_days','Device Category','Devices_per_subject_average'],
                                                  as_index=False,
                                                  observed=True).agg({'Devices_total':'sum','SubjectCount':'sum','Species':'nunique'})
    # inputDF = Neural_InVivo_DF01_Selected.groupby(['Implant_Duration_days','Device Category','Devices_per_subject_average'],
    #                                               as_index=False,
    #                                               observed=True).agg(
    #                                                   devicestotal=('Devices_total','sum'),
    #                                                   subjcount=('SubjectCount','sum'),
    #                                                   uniquesubjs=('Species','nunique'))
#Define Circle Area
    # define range of bubble sizes', 
    # scale to match max subject count = 8 in split 
    # vs. max subject count = 26 when grouped
    #bubblesizeunit = 2.*max(Neural_InVivo_DF01_Selected['Devices_total'])/(80**2)  # define range of bubble sizes'
        # To scale the bubble size, use the attribute sizeref. 
        # We recommend using the following formula to calculate a sizeref value:
        # sizeref = 2. * max(array of size values) / (desired maximum marker size ** 2)
    category_order_by_count = inputDF['Device Category'].value_counts().index.tolist()
    # Create stand-along scatter plots
    fig00 = px.scatter(inputDF,
        y="Devices_per_subject_average",
        x="Implant_Duration_days",
        color="Device Category",      # legend categories = species
        size='Devices_total',  # Make marker size proportional to number of subjects
        #text="SubjectCount",  # label each bubble with subject count
        category_orders={"Device Category": category_order_by_count}, # Explicitly set custom order
        hover_data=['SubjectCount','Species']
        )
    #
    fig = go.Figure(fig00)
    fig.update_traces(marker=dict(sizemode='area',
                                  sizeref=bubblesizeunit,
                                  opacity=0.8,
                                  line=dict(width=1,color='black')
                                  ),
                      selector=dict(mode='markers'),
                      #textposition='inside',
                      #textfont_size=(bubblesizeunit/10),
                      )
    fig.update_layout(#scattermode='group',scattergap=0.3,
                      title_text='Implanted Devices vs. Study Duration')
    fig.update_xaxes(title_text='Implant Study Duration (Days)')
    fig.update_yaxes(title_text='Devices per Subject',
                     )  #range=[-30,240]

    # plot save
    NEplot02nameh = SaveFolderHTML + "fig_article_InVivo_devicespersubj-vs-duration-grouped.html"
    NEplot02namep = SaveLocation + "fig_article_InVivo_devicespersubj-vs-duration-grouped.png"
    NEplot02names = SaveLocation + "fig_article_InVivo_devicespersubj-vs-duration-grouped.svg"
    #
    fig.write_html(NEplot02nameh,full_html=False)
    fig.write_image(NEplot02namep)
    fig.write_image(NEplot02names, format="svg")
    
    return

#-----------------------------------------------------------------------------
# [Manuscript Fig] Generates Table of In Vivo Histology Data
def Neural_Plot03(SaveLocation,SaveFolderHTML,Neural_InVivo_DF02):
    fig0 = go.Table(
        header=dict(values=list(Neural_InVivo_DF02.columns)),
        cells=dict(values=[Neural_InVivo_DF02.refID, 
                           Neural_InVivo_DF02.doi,
                           Neural_InVivo_DF02.year, 
                           Neural_InVivo_DF02.pub_decade,
                           Neural_InVivo_DF02.SubjectCount, 
                           Neural_InVivo_DF02.Species,
                           Neural_InVivo_DF02.Implant_Region, 
                           Neural_InVivo_DF02.Device_Category,
                           Neural_InVivo_DF02.Implant_duration_days, 
                           Neural_InVivo_DF02.Histo_EmbeddingMedia, 
                           Neural_InVivo_DF02.Histo_Primary_Antibodies,
                           Neural_InVivo_DF02.Histo_Secondary_Antibodies,
                           Neural_InVivo_DF02.Histo_Stain, 
                           Neural_InVivo_DF02.Histo_Imaging_Method, 
                           Neural_InVivo_DF02.Histo_Distance_from_Implant_min_um, 
                           Neural_InVivo_DF02.Histo_Distance_from_Implant_max_um
                           ]),
        columnwidth=[],
        )
    fig = go.Figure()
    fig.add_traces(fig0)
    
    # table save
    NEplot03nameh = SaveFolderHTML + "fig_article_InVivo_histology.html"
    NEplot03namep = SaveLocation + "fig_article_InVivo_histology.png"
    NEplot03names = SaveLocation + "fig_article_InVivo_histology.svg"
    #
    fig.show()
    fig.write_html(NEplot03nameh,full_html=False)
    fig.write_image(NEplot03namep)
    fig.write_image(NEplot03names, format="svg")
    
    return

#-----------------------------------------------------------------------------
# [Manuscript Fig] Plots Insertion and Buckling Force Figures
def Neural_Plot04a(SaveLocation,SaveFolderHTML,bubblesizeunit,Neural_Benchtop_DF01):    
    Neural_Benchtop_DF01['SiC_Thickness_um'] = Neural_Benchtop_DF01['SiC_Thickness_um'].astype('category')
    Neural_Benchtop_DF01_sorted = Neural_Benchtop_DF01.sort_values(by='SiC_Thickness_um', ascending=True)
    
    # Create stand-alone scatter plots
    Neural_Benchtop_DF01_fig1 = Neural_Benchtop_DF01_sorted
    #Neural_Benchtop_DF01_fig1 = Neural_Benchtop_DF01_sorted.dropna(subset=['Buckling_Force_mN'])
    styles = ["dot", "solid", "solid", "solid", "solid", "solid",
              "solid", "solid", "solid", "solid", "solid", "solid"]
    #
    fig1 = px.scatter(Neural_Benchtop_DF01_fig1,
                      x='Shank_Length_mm',
                      y='Buckling_Force_mN',  
                      color='SiC_Thickness_um',      # legend categories 
                      symbol='Species',
                      facet_col='Shank_Xsection_Area_um^2',
                      facet_col_wrap=4,
                      labels={
                          "Shank_Length_mm": "Length (mm)",
                          "Buckling_Force_mN": "Buckling Force (mN)",
                          "SiC_Thickness_um": "a-SiC Thickness (um)",
                          "Shank_Xsection_Area_um^2": "Area(um^2)"
                          },
                      )
    # fig1 = px.scatter_3d(Neural_Benchtop_DF01_fig1,
    #     x="Shank_Xsection_Area_um^2",
    #     y="Buckling_Force_mN",
    #     z="Shank_Length_mm",
    #     color="SiC_Thickness_um",      # legend categories 
    #     symbol="Species"
    #     #size='SiC_Thickness_um',  # Make marker size proportional to film thickness
    #     #text="Species",  # label for each bubble 
    #     #category_orders={"Device Category": category_order_by_count}, # Explicitly set custom order
    #     #hover_data=['SubjectCount','Species','Insertions_Successful_count']
    #     )
    
    #
    # fig1.update_traces(marker=dict(sizemode='area',
    #                               sizeref=bubblesizeunit,
    #                               opacity=0.8,
    #                               line=dict(width=1,color='black')
    #                               ),
    #                   selector=dict(mode='markers'),
    #                   #textposition='inside',
    #                   #textfont_size=(bubblesizeunit/10),
    #                   )
    fig1.update_traces(#overwrite=True, 
                       marker=dict(opacity=0.8, 
                                   size=14, 
                                   line=dict(#dash="solid", 
                                             color="black", 
                                             width=1
                                             )
                                   ))
    fig1.update_layout(title_text="Buckling Force vs. Shank Length",
                       #showlegend=False,
                       #margin=dict(l=100, r=40, t=60, b=60),
                       scene=dict(
                           xaxis = dict(title="Cross Section Area (um^2)"),
                           yaxis = dict(title="Buckling Force (mN)"),
                           zaxis = dict(title="Shank Length (mm)")))
    # fig1.update_xaxes(title_text="Cross Section Area (um^2)")
    # fig1.update_yaxes(title_text="Buckling Force (mN)")
    # fig1.update_zaxes(title_text="Shank Length (mm)")
    
    # figure 1 save
    fig01 = go.Figure(fig1)
    #    
    NEplot04nameh1 = SaveFolderHTML + "fig_article_Benchtop_Buckling.html"
    NEplot04namep1 = SaveLocation + "fig_article_Benchtop_Buckling.png"
    NEplot04names1 = SaveLocation + "fig_article_Benchtop_Buckling.svg"
    #
    fig01.write_html(NEplot04nameh1,full_html=False)
    fig01.show("png", width=1200, height=600)
    fig01.write_image(NEplot04namep1)
    fig01.show("svg", width=1200, height=600)
    fig01.write_image(NEplot04names1, format="svg")
    
    return
    

def Neural_Plot04b(SaveLocation,SaveFolderHTML,bubblesizeunit,Neural_Benchtop_DF01):    
    Neural_Benchtop_DF01['SiC_Thickness_um'] = Neural_Benchtop_DF01['SiC_Thickness_um'].astype('category')
    Neural_Benchtop_DF01_sorted = Neural_Benchtop_DF01.sort_values(by='SiC_Thickness_um', ascending=True)
    
    # generate subplots 
    Neural_Benchtop_DF01_fig2 = Neural_Benchtop_DF01_sorted
    #Neural_Benchtop_DF01_fig2 = Neural_Benchtop_DF01_sorted.dropna(subset=['Insertion_Force_mN'])
    styles = ["dot", "solid", "solid", "solid", "solid", "solid",
              "solid", "solid", "solid", "solid", "solid", "solid"]
    #
    fig2 = px.scatter(Neural_Benchtop_DF01_fig2,
                      x='Shank_Length_mm',
                      y='Insertion_Force_mN',  
                      color='SiC_Thickness_um',      # legend categories 
                      symbol='Species',
                      facet_col='Shank_Xsection_Area_um^2',
                      facet_col_wrap=4,
                      labels={
                          "Shank_Length_mm": "Length (mm)",
                          "Insertion_Force_mN": "Insertion Force (mN)",
                          "SiC_Thickness_um": "a-SiC Thickness (um)",
                          "Shank_Xsection_Area_um^2": "Area(um^2)"
                          }
                      )
    # fig2_42 = px.scatter(Neural_Benchtop_DF01_fig2[Neural_Benchtop_DF01_fig2['Shank_Xsection_Area_um^2']=='42'],
    #     x="Shank_Length_mm",
    #     y="Insertion_Force_mN",  
    #     color="SiC_Thickness_um",      # legend categories 
    #     symbol="Species"
    #     )
    # #
    # fig2_60 = px.scatter(Neural_Benchtop_DF01_fig2[Neural_Benchtop_DF01_fig2['Shank_Xsection_Area_um^2']=='60'],
    #     x="Shank_Length_mm",
    #     y="Insertion_Force_mN",  
    #     color="SiC_Thickness_um",      # legend categories 
    #     symbol="Species"
    #     )
    # #
    # fig2_80 = px.scatter(Neural_Benchtop_DF01_fig2[Neural_Benchtop_DF01_fig2['Shank_Xsection_Area_um^2']=='80'],
    #     x="Shank_Length_mm",
    #     y="Insertion_Force_mN",  
    #     color="SiC_Thickness_um",      # legend categories 
    #     symbol="Species"
    #     )
    # #
    # fig2_120 = px.scatter(Neural_Benchtop_DF01_fig2[Neural_Benchtop_DF01_fig2['Shank_Xsection_Area_um^2']=='120'],
    #     x="Shank_Length_mm",
    #     y="Insertion_Force_mN",  
    #     color="SiC_Thickness_um",      # legend categories 
    #     symbol="Species"
    #     )
    # #
    # fig2_161 = px.scatter(Neural_Benchtop_DF01_fig2[Neural_Benchtop_DF01_fig2['Shank_Xsection_Area_um^2']=='161'],
    #     x="Shank_Length_mm",
    #     y="Insertion_Force_mN",  
    #     color="SiC_Thickness_um",      # legend categories 
    #     symbol="Species"
    #     )
    # #
    # fig2_200 = px.scatter(Neural_Benchtop_DF01_fig2[Neural_Benchtop_DF01_fig2['Shank_Xsection_Area_um^2']=='200'],
    #     x="Shank_Length_mm",
    #     y="Insertion_Force_mN",  
    #     color="SiC_Thickness_um",      # legend categories 
    #     symbol="Species"
    #     )
    # #
    # fig2_207 = px.scatter(Neural_Benchtop_DF01_fig2[Neural_Benchtop_DF01_fig2['Shank_Xsection_Area_um^2']=='207'],
    #     x="Shank_Length_mm",
    #     y="Insertion_Force_mN",  
    #     color="SiC_Thickness_um",      # legend categories 
    #     symbol="Species"
    #     )
    # #
    # fig2_300 = px.scatter(Neural_Benchtop_DF01_fig2[Neural_Benchtop_DF01_fig2['Shank_Xsection_Area_um^2']=='300'],
    #     x="Shank_Length_mm",
    #     y="Insertion_Force_mN",  
    #     color="SiC_Thickness_um",      # legend categories 
    #     symbol="Species"
    #     )
    #
    #
    # fig2 = make_subplots(rows=4,cols=4,shared_xaxes=True,
    #                      shared_yaxes=True,print_grid=True)
    # #
    # #
    # fig2.add_trace(fig2_42,row=1,col=1)
    # fig2.add_trace(fig2_60,row=1,col=2)
    # fig2.add_trace(fig2_80,row=1,col=3)
    # fig2.add_trace(fig2_120,row=1,col=4)
    # #
    # fig2.add_trace(fig2_161,row=2,col=1)
    # fig2.add_trace(fig2_200,row=2,col=2)
    # fig2.add_trace(fig2_207,row=2,col=3)
    # fig2.add_trace(fig2_300,row=2,col=4)
    #
    #
    fig2.update_traces(#overwrite=True, 
                       marker=dict(opacity=0.8, 
                                   size=14, 
                                   line=dict(#dash="solid", 
                                             color="black", 
                                             width=1
                                             )
                                   ))
    fig2.update_layout(title_text="Insertion Force vs. Shank Length",
                       #margin=dict(l=100, r=40, t=60, b=60),
                       scene=dict(
                           xaxis = dict(title="Cross Section Area (um^2)"),
                           yaxis = dict(title="Buckling Force (mN)"),
                           zaxis = dict(title="Shank Length (mm)")))
    # fig2.update_xaxes(title_text="Cross Section Area (um^2)")
    # fig2.update_yaxes(title_text="Insertion Force (mN)")
    # fig2.update_zaxes(title_text="Shank Length (mm)")
    
    # figure 2 save
    fig02 = go.Figure(fig2)
    fig02.show()
    #  
    NEplot04nameh2 = SaveFolderHTML + "fig_article_Benchtop_Insertion.html"
    NEplot04namep2 = SaveLocation + "fig_article_Benchtop_Insertion.png"
    NEplot04names2 = SaveLocation + "fig_article_Benchtop_Insertion.svg"
    #
    fig02.write_html(NEplot04nameh2,full_html=False)
    fig02.show("png", width=1200, height=600)
    fig02.write_image(NEplot04namep2)
    fig02.show("svg", width=1200, height=600)
    fig02.write_image(NEplot04names2, format="svg")
    
    return


#-----------------------------------------------------------------------------
# [Manuscript Fig] Plots SiC Dissolution Rates
def Neural_Plot05(SaveLocation,SaveFolderHTML,Neural_Benchtop_DF02):
    #
    Neural_Benchtop_DF02['Temperature_degC'] = Neural_Benchtop_DF02['Temperature_degC'].astype('category')
    Neural_Benchtop_DF02['Material'] = Neural_Benchtop_DF02['Material'].astype('category')
    Neural_Benchtop_DF02_sorted = Neural_Benchtop_DF02.sort_values(by='Temperature_degC', ascending=True)
    Neural_Benchtop_DF02_sorted = Neural_Benchtop_DF02_sorted.sort_values(by='Material', ascending=True)
    #
    fig = px.scatter(Neural_Benchtop_DF02_sorted,
        x="Duration_days",
        y="Dissolution_nm/day",  
        color="Temperature_degC",      # legend categories 
        symbol="Material"
        #size='SiC_Thickness_um',  # Make marker size proportional to film thickness
        #text="Species",  # label for each bubble 
        #category_orders={"Device Category": category_order_by_count}, # Explicitly set custom order
        #hover_data=['SubjectCount','Species','Insertions_Successful_count']
        )
    #
    #fig.update_traces(marker=dict(sizemode='area',
    #                              sizeref=bubblesizeunit,
    #                              opacity=0.8,
    #                              line=dict(width=1,color='black')
    #                              ),
    #                  selector=dict(mode='markers'),
    #                  #textposition='inside',
    #                  #textfont_size=(bubblesizeunit/10),
    #                  )
    fig.update_traces(marker=dict(size=20, opacity=0.8, line=dict(width=2,
                                                     color='Black')))
    fig.update_layout(title_text="Material Dissolution vs. Aging Parameters",
                      legend=dict(
                          yanchor='top',
                          y=0.95,
                          xanchor='right',
                          x=0.95))
    fig.update_xaxes(title_text="Study Duration (days)")
    fig.update_yaxes(title_text="Dissolution Rate (nm/day)",
                     title_standoff=80)
    
    # figure 2 save
    fig0 = go.Figure(fig)
    fig0.show()
    #  
    NEplot05nameh = SaveFolderHTML + "fig_article_Benchtop_Dissolution.html"
    NEplot05namep = SaveLocation + "fig_article_Benchtop_Dissolution.png"
    NEplot05names = SaveLocation + "fig_article_Benchtop_Dissolution.svg"
    #
    fig0.write_html(NEplot05nameh,full_html=False)
    fig0.write_image(NEplot05namep)
    fig0.write_image(NEplot05names, format="svg")
    
    return


#-----------------------------------------------------------------------------
# END OF FILE
#-----------------------------------------------------------------------------