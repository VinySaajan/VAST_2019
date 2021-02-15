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
from bokeh.models import (GeoJSONDataSource, Button, Panel, ColorBar, ColumnDataSource, HoverTool, LinearColorMapper, LogColorMapper)
from bokeh.models.widgets import (RadioButtonGroup, Tabs, Select, MultiSelect, Slider, Div)
from bokeh.layouts import column, row, WidgetBox, gridplot
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral6, Spectral3
from bokeh.palettes import BuPu, grey
from bokeh.resources import CDN
from bokeh.embed import file_html
import json

def state_count_tab(): 
    
    plotter, StHimark, gsource = displayMap()
    url = join(basename(split(dirname(__file__))[0]), 'data', 'sensor_count.csv')
    state_count = pd.read_csv(url)
    palette = grey(19)
    palette = palette[::-1]
    color_mapper = LinearColorMapper(palette = palette, low = state_count['count'].min(), high = state_count['count'].max())
    grey_merged = StHimark.merge(state_count, left_on = 'Nbrhood', right_on = 'Neighbourhood')
    merged_json = json.loads(grey_merged.to_json())
    json_data = json.dumps(merged_json)
    
    geosource = GeoJSONDataSource(geojson = json_data)
    plotter.patches('xs', 'ys', source=geosource, fill_color = {'field' :'count', 'transform' : color_mapper},
                    line_color="black", line_width=0.05, fill_alpha=1.0)
    tick_labels = {'0': '0', '10': '10', '20':'20', '30':'30', '40':'40', '50':'>50'}
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=5,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    plotter.add_layout(color_bar, 'below')
    layout = column(plotter)
    tab = Panel(child=layout, title='State Uncertainity')
    return tab