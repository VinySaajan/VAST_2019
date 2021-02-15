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

def data_viz_tab(): 
    def updateHeatMap(attr, old, new):
        if select_sensor.value == "Heatmap-Static Sensors":
            img_path="https://i.imgur.com/3yd44bL.png"
            plotter.image_url(url=[img_path], x=0, y=1, w=1, h=1)
        if select_sensor.value == "Heatmap-Mobile Sensors":
            img_path="https://i.imgur.com/HMekh7x.png"
            plotter.image_url(url=[img_path], x=0, y=1, w=1, h=1)
        if select_sensor.value == "Mobile Sensor 9 Radiation Plot":
            img_path="https://i.imgur.com/Mo8qsM9.png"
            plotter.image_url(url=[img_path], x=0, y=1, w=1, h=1)
        if select_sensor.value == "Radiation Clusters":
            img_path="https://i.imgur.com/jNhiALM.png"
            plotter.image_url(url=[img_path], x=0, y=1, w=1, h=1)
    
    
    select_sensor = Select(title="Heat Map: ", value="Heatmap-Mobile Sensors", options=["Heatmap-Static Sensors", "Heatmap-Mobile Sensors", "Mobile Sensor 9 Radiation Plot", "Radiation Clusters"])
    plotter = figure(title="Data Analysis Map", x_range=(0,1), y_range=(0,1), plot_width=840, plot_height=600)
    plotter.axis.visible = False
    plotter.xgrid.visible = False
    plotter.ygrid.visible = False
    img_path="https://i.imgur.com/HMekh7x.png"
    plotter.image_url(url=[img_path], x=0, y=1, w=1, h=1)
    select_sensor.on_change('value', updateHeatMap)
    layout = column(row([plotter,column([select_sensor])]))
    tab = Panel(child=layout, title='Data Analysis')
    return tab