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
#                          DATA VISUALIZATIONS
#-----------------------------------------------------------------------------
#print(fig)
#fig.show()
#-----------------------------------------------------------------------------
def ArticleList_Plot01(SaveLocation,SaveFolderHTML,year_unique_count):
    #-----------------------------------------------------------------------------
    # plot 1
    # !!!!!!! features/formatting to add:
        # color papers with multiple category labels
        # add subplot: 
            # ridgeline; by category, each = pub count (y) vs. time (x)
            # -or- nested circles, each category percentage% vs gray total
            # scale total circle area vs count by decade (see word doc)
    fig0 = px.scatter(year_unique_count,range_x=[1975,2030],range_y=[0,18],
                      title="SiC Publications Over Time")
    fig = go.Figure(fig0)
    fig.update_layout(showlegend=False)
    fig.update_traces(marker=dict(size=10,color='black'))
    fig.update_traces(hovertemplate="Year: %{x} <br> Publications: %{y}<extra></extra>")
    fig.update_xaxes(title='Publication Year',
                     minor=dict(ticks='inside',showgrid=True))
    fig.update_yaxes(title='Number of Articles')
    # plot 1 save
    plot01nameh = SaveFolderHTML + "fig_article-count-by-year.html"
    plot01namep = SaveLocation + "fig_article-count-by-year.png"
    #
    fig.write_html(plot01nameh,full_html=False)
    fig.write_image(plot01namep)
    #fig.write_html("Outputs\\fig_article-count-by-year.html",full_html=False)
    #fig.write_image("Outputs\\fig_article-count-by-year.png")
    #
    return 

#-----------------------------------------------------------------------------
def ArticleList_Plot02(SaveLocation,SaveFolderHTML,c_greys,Cat_by_Yr_melted,cat_by_decade_totals):
    # plot 2
        # !!!!!!! features/formatting to add:
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
                  title="SiC Publication Category Over Time", 
                  barmode='stack', range_y=[0,110],
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
    plot02nameh = SaveFolderHTML + "fig_article-category-by-decade.html"
    plot02namep = SaveLocation + "fig_article-category-by-decade.png"
    #
    fig.write_html(plot02nameh,full_html=False)
    fig.write_image(plot02namep)
    #fig.write_html("Outputs\\fig_article-category-by-decade.html",full_html=False)
    #fig.write_image("Outputs\\fig_article-category-by-decade.png")
    #
    return 

#-----------------------------------------------------------------------------
def ArticleList_Plot02b(SaveLocation,SaveFolderHTML,c_greys,ArticleListDF_exploded):
    # plot 2 version b (after creating ArticleListDF_exploded)
    # !!!!!!! features/formatting to add:
        # fix counts from groupby !
        # re-order/sort categories ('Neural Engineering' 1st, 'Other' last)
        # match colors to ArticleList_Plot02 function
    #
    #DF_temp = ArticleListDF_exploded.drop(['doi','pubmed_id','title','authors','journal','month','day'],axis=1)
    #DF_info = DF_temp.describe(include=['category'])
    #exclude=['doi','pubmed_id','title','authors','journal','month','day']
    DF_temp = ArticleListDF_exploded.reset_index()
    cat_by_decade_list = DF_temp.groupby(['pub_decade','Reported_Category'],observed=True)['refID'].count()
    cat_by_decade_list = cat_by_decade_list.reset_index()
    cat_by_decade_list = cat_by_decade_list.rename(columns={'refID':'publications'})
    #cat_by_decade_list = ArticleListDF_exploded.groupby(['pub_decade','Reported_Category']).count()
    # Define colors to highlight Neural Engineering
    #plt2_colors = c_greys[1:8]
    #plt2_colors[0] = 'rgb(35,138,141)'
    #
    fig0 = px.bar(cat_by_decade_list,x='pub_decade',y='publications',
                  color='Reported_Category',barmode='stack',
                  title="SiC Publication Category Over Time")
#                  color_discrete_sequence=plt2_colors,
                  #, range_y=[0,110])#,
                  #custom_data=['CategoryLabel','decade_end'])
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
    plot02nameh = SaveFolderHTML + "fig_article-category-by-decade-vB.html"
    plot02namep = SaveLocation + "fig_article-category-by-decade-vB.png"
    #
    fig.write_html(plot02nameh,full_html=False)
    fig.write_image(plot02namep)
    return

#-----------------------------------------------------------------------------
# !!!!!!!  in progress 2025 Sept
def ArticleList_Plot02dot(SaveLocation,SaveFolderHTML,c_greys,ArticleListDF_exploded):
    # plot 2 (circle plot version)
        # plot count of each category vs. decade as separate data series
        # scale area of each circle/datapoint with % of total papers that decade
        # subplot (above) = nested circles, each category % vs gray total
        # scale total circle area vs count by decade
        
    return

#-----------------------------------------------------------------------------
def ArticleList_Plot03mosaic(SaveLocation,SaveFolderHTML,ArticleListDF_exploded):
    # plot 3 (mosaic version)
    # !!!!!!! features/formatting to add:
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
    plot03namep = SaveLocation + "fig_mosaic-SiC-publications.png"
    plt.savefig(plot03namep)
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
def ArticleList_Plot03heat(SaveLocation,SaveFolderHTML,ArticleListDF_exploded):
    # plot 3 (heatmap version)
    # !!!!!!! features/formatting to add:
        # fix counts ! (use groupby? or reset index?)
        # fix x- and y- axes labels
        # update legend label to "Number of Publications"
        # add title
        # create the other 2 category comparisons:
            # x="Reported_Category",y="Reported_Data"
            # x="Reported_SiC",y="Reported_Data"
    #
    fig0 = px.density_heatmap(ArticleListDF_exploded, x="Reported_Category",
                             y="Reported_SiC")#,facet_col="Reported_Data")
    fig = go.Figure(fig0)
    # plot 3 heatmap save
    plot03nameh = SaveFolderHTML + "fig_heatmap-SiC-publications.html"
    plot03namep = SaveLocation + "fig_heatmap-SiC-publications.png"
    #
    fig.write_html(plot03nameh,full_html=False)
    fig.write_image(plot03namep)
    #
    return 

#-----------------------------------------------------------------------------
def ArticleList_Plot03ice(SaveLocation,SaveFolderHTML,ArticleListDF_exploded):
    # plot 3 (icicle version)
    # !!!!!!! features/formatting to add:
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
    #
    fig.write_html(plot03nameh,full_html=False)
    fig.write_image(plot03namep)
    #
    return 

#-----------------------------------------------------------------------------
# !!!!!!!  in progress 2025 Sept
def ArticleList_Plot03sun(SaveLocation,SaveFolderHTML,ArticleListDF_exploded):
    # plot 3 (sunburst version)
    
    return

#-----------------------------------------------------------------------------
# !!!!!!!  in progress 2025 Sept
def create_plotly_mosaic(df, index, colors):
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
# !!!!!!!  in progress 2025 Sept
def ArticleList_Plot04(SaveLocation,SaveFolderHTML,DF1,DF2,DF3):    
    # !!!!
    # in progress
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
    plot01nameh = SaveFolderHTML + "fig_article-SiCtype-by-DataReported.html"
    plot01namep = SaveLocation + "fig_article-SiCtype-by-DataReported.png"
    #
    fig.write_html(plot01nameh,full_html=False)
    fig.write_image(plot01namep)
    #fig.write_html("Outputs\\fig_article-count-by-year.html",full_html=False)
    #fig.write_image("Outputs\\fig_article-count-by-year.png")
    #
    return 




#-----------------------------------------------------------------------------
# END OF FILE
#-----------------------------------------------------------------------------