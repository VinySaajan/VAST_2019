# -*- coding: utf-8 -*-
"""
Created on Mon Jan 06 14:58:29 2020

@author: Krishna Kinger, Viny
"""

import pandas as pd
from os.path import dirname, basename, split, join
import numpy as np
from scipy.spatial import Voronoi
from collections import OrderedDict
import collections
from scripts.himarkmap import displayMap, get_voronoi
from datetime import datetime
import geopandas as gpd
from bokeh.plotting import figure
from pyproj import Proj, transform
from bokeh.models import (Button, Panel, ColorBar, ColumnDataSource, HoverTool, LinearColorMapper, LogColorMapper)
from bokeh.models.widgets import (RadioButtonGroup, Tabs, Select, MultiSelect, Slider, Div)
from bokeh.layouts import column, row, WidgetBox, gridplot
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral6, Spectral3
from bokeh.palettes import BuPu
from bokeh.resources import CDN
from bokeh.embed import file_html

def sensor_uncertainity_tab(): 
    
    plotlist = list()
    plotter = figure(title="Data Analysis Map", plot_width=900, plot_height=600)
    plotter.axis.visible = False
    plotter.xgrid.visible = False
    plotter.ygrid.visible = False
    
    url = join(basename(split(dirname(__file__))[0]), 'data', 'mobile_mean_std.csv')
    mobile = pd.read_csv(url)
    group = mobile.groupby('static')
    url = join(basename(split(dirname(__file__))[0]), 'data', 'static_mean_std.csv')
    static = pd.read_csv(url)
    
    for key, item in group:
        x = key
        y = group.get_group(key)
        source = ColumnDataSource(y)
        source1 = ColumnDataSource(static[static['sensor_id']==x])
        # hover = HoverTool(names = ["sensors"], tooltips = [("Sensor_ID","@Sensor_id")], show_arrow=False)
        plot1 = figure(plot_width=275, plot_height=275)
        p11 = plot1.circle(x='mean', y='std', color="green", size=20, source=source1)
        plot1.add_tools(HoverTool(renderers=[p11], tooltips=[("Sensor_ID","@sensor_id")], show_arrow=False))
        p12 = plot1.circle(x='Mean', y='Std',name="sensors", color="red", size=10, source=source)
        plot1.add_tools(HoverTool(renderers=[p12], tooltips=[("Sensor_ID","@Sensor_id")], show_arrow=False))
        plot1.xaxis.axis_label = 'Mean'
        plot1.yaxis.axis_label = 'Standard Deviation'
        plotlist.append(plot1)
    
    
    p = gridplot([[plotlist[0], plotlist[1], plotlist[2]], [plotlist[3], plotlist[4], plotlist[5]], [plotlist[6], plotlist[7],plotlist[8]]])
    
    layout = column(p)
    tab = Panel(child=layout, title='Sensor Uncertainity')
    return tab