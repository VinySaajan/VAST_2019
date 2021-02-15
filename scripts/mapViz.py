# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 20:53:19 2019

@author: Krishna Kinger, Viny
"""

import pandas as pd
from pandas.core.frame import DataFrame
from os.path import dirname, basename, split, join
import numpy as np
from scipy.spatial import Voronoi
from collections import OrderedDict
from bokeh.io import curdoc
import sqlite3 as sq
import collections
from scripts.himarkmap import displayMap, get_voronoi
from datetime import datetime
import geopandas as gpd
from bokeh.plotting import figure
from pyproj import Proj, transform
from bokeh.models import (GeoJSONDataSource,Button, Panel, ColorBar, ColumnDataSource, HoverTool, LinearColorMapper, LogColorMapper, Label, LabelSet)
from bokeh.models.widgets import (RadioButtonGroup, Tabs, Select, MultiSelect, Slider, Div, CheckboxButtonGroup)
from bokeh.layouts import column, row, WidgetBox, gridplot
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral6, Spectral3
from bokeh.models.glyphs import Line, MultiLine, Patches, ImageURL
from bokeh.colors import RGB
from bokeh.palettes import brewer, grey
import json

def map_viz_tab(): 
    
    def plot_sensor_path(sensors, df_final):
        for i in sensors:
            #plotter.line(x=path_data.get_group(i).x, y=path_data.get_group(i).y, name=str(i), color="black")
            plotter.line(x=df_final['x'].loc[df_final['sid']==i], y=df_final['y'].loc[df_final['sid']==i], color="orange")
    
    def updateOverlays(attr, old, new):
        overlays = checkbox_btn_group.active
        if 0 in overlays:
            img_hsp = "https://upload.wikimedia.org/wikipedia/commons/d/d0/Flag_for_hospital_ship_of_the_Regia_Marina.svg"
            hospital_data = dict(url=[img_hsp]*8,x=df_hospitalLocation.x, y = df_hospitalLocation.y)
            source_hospital.data = hospital_data

        else:
            h_x, h_y,h_url = [], [], []
            hospital_data = dict(url=h_url,x=h_x, y = h_y)
            source_hospital.data = hospital_data
            
        if 1 in overlays:
            x_patch, y_patch, x_vor_ls, y_vor_ls = get_voronoi(df_hospitalLocation.x, df_hospitalLocation.y)
            patch_data = dict(xs=x_patch, ys=y_patch)
            lines_data = dict(xs=x_vor_ls, ys=y_vor_ls)
            source_vor.data = patch_data
            source_vor_ls.data = lines_data
        else:
            x_patch, y_patch, x_vor_ls, y_vor_ls = [], [], [], []
            patch_data = dict(xs=x_patch, ys=y_patch)
            lines_data = dict(xs=x_vor_ls, ys=y_vor_ls)
            source_vor.data = patch_data
            source_vor_ls.data = lines_data

        if 2 in overlays:
            color_mapper = LinearColorMapper(palette = palette, low = 0, high = 50)
            mp.fill_color = {'field' :'Value', 'transform' : color_mapper}
            mp.fill_alpha = 1.0
            tick_labels = {'0': '0', '10': '10', '20':'20', '30':'30', '40':'40', '50':'>50'}
            color_bar = ColorBar(color_mapper=color_mapper, label_standoff=5,width = 500, height = 20,
            border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
            plotter.add_layout(color_bar, 'below')
        else:
            mp.fill_color = 'lightslategrey'
            mp.fill_alpha = 0.5
        
    def updateMotionMap(attr, old, new):
        check = checkbox_btn_group1.active
        xmin = -13326251
        if 0 in check:
            img_state = ["https://i.imgur.com/IBpHIs1.png",
                         "https://i.imgur.com/oawpbdU.png",
                         "https://i.imgur.com/kigeppa.png",
                         "https://i.imgur.com/mHAUX9K.png",
                         "https://i.imgur.com/pxbaYlp.png",
                         "https://i.imgur.com/QNhcnRn.png",
                         "https://i.imgur.com/GB2fRMS.png",
                         "https://i.imgur.com/qXfEJNL.png",
                         "https://i.imgur.com/QZOTgG9.png",
                         "https://i.imgur.com/sE1U89y.png",
                         "https://i.imgur.com/vAxwSQE.png",
                         "https://i.imgur.com/yO1iOCw.png",
                         "https://i.imgur.com/jFpJ2UQ.png",
                         "https://i.imgur.com/lVkwzYH.png",
                         "https://i.imgur.com/Q519cud.png",
                         "https://i.imgur.com/FtnTUAC.png",
                         "https://i.imgur.com/j2D9ud6.png",
                         "https://i.imgur.com/Tb4tWI5.png",
                         "https://i.imgur.com/yhl5nAX.png"]
            states_x = [xmin-28000, xmin-22500, xmin-16000, xmin-12000, xmin-22000, xmin-22500, xmin-1000, xmin-6000,
                        xmin-14000, xmin-8000, xmin-4700, xmin-4700, xmin-9000,  xmin-16000,  xmin-19500,  xmin-19500,
                        xmin-14000, xmin-13000, xmin-16500]
            states_y = [19000, 19700, 20000, 17000, 12000, 16000, 11000, 3800,
                        6000, 5900, 7000, 10500, 12500, 17000, 17000, 13500,
                        9200, 13500, 13000]
            w = [4000, 5000, 4000, 4000, 4000, 4000, 3000, 4800, 5000, 2500, 4000, 4000, 4000, 3000, 3000, 3000, 4300, 3500, 3500]
            h = [3600, 3000, 3000, 3000, 3000, 3000, 6000, 4800, 3000, 5000, 4000, 3000, 4000, 2000, 2000, 3000, 2700, 3500, 3500]
            states_data = dict(url=img_state,x=states_x, y = states_y, w=w, h=h)
            source_states.data = states_data
        else:
            h_x, h_y,h_url,w, h = [], [], [],[],[]
            states_data = dict(url=h_url,x=h_x, y = h_y, w=w, h=h)
            source_states.data = states_data
            
        if 1 in check:
            source_path1.data = data_path1
        else:
            source_path1.data = data_path

            
    def update_time_frame(attr, old, new):
        """ update the time frame and load new dataframes
        """
        timeline.value = time_start
        time_current = time_start
        if time_frame.active == 0: 
            timeline.step=5
            df_mobile_location_cur = df_mobileLocation_raw
            df_static_reading_cur = df_staticSensors_raw
            df_mobile_reading_cur = df_mobileSensors_raw
        
        if time_frame.active == 1:
            timeline.step=60
            df_mobile_location_cur = df_mobileLocation_min
            df_static_reading_cur = df_staticSensors_min
            df_mobile_reading_cur = df_mobileSensors_min
            
        if time_frame.active == 2:
            timeline.step=3600
            df_mobile_location_cur = df_mobileLocation_hr
            df_static_reading_cur = df_staticSensors_hr
            df_mobile_reading_cur = df_mobileSensors_hr
            
        static_sensors_update(attr, old, new)
        mobile_sensors_update(attr, old, new)
        
        
    def getDFfromDB(table_name):
        url = join(basename(split(dirname(__file__))[0]), 'data', 'StHimarkDB.db')
        conn = sq.connect(url)
        df = pd.read_sql_query("select * from "+ table_name + ";", conn)
        return df
    
        
    def static_sensors_update(attr, old, new):
        time_current = datetime.fromtimestamp(timeline.value + baseTime)
        sid,x,y,val,user=[],[],[],[],[]
        data_new = collections.OrderedDict({
                'sid':sid,
                'x_loc': x,
                'y_loc': y,
                'value':val,
                'user':user,
                })
        source_static.data = data_new
        #clean(source_static_locations)
        selected = static_sensors_ms.value
        selectedStaticSensors.clear()
        for name in selected:
            selectedStaticSensors.append(name.split("_",1)[1])
        for sensor in selectedStaticSensors:
            sid.append(sensor)
            x.append(df_staticLocation['x'].loc[df_staticLocation['sid']==int(sensor)].values.item())
            y.append(df_staticLocation['y'].loc[df_staticLocation['sid']==int(sensor)].values.item())
            val.append(df_static_reading_cur[sensor].loc[df_static_reading_cur['Timestamp']==time_current].values.item())
            user.append('Sensor '+sensor)
         
        data_new = collections.OrderedDict({
                'sid':sid,
                'x_loc': x,
                'y_loc': y,
                'value':val,
                'user':user,
                })
        source_static.data = data_new 


    def mobile_sensors_update(attr, old, new):
        time_current = datetime.fromtimestamp(timeline.value + baseTime)
        greencar = 'https://i.imgur.com/YyWzmgH.png'
        selected = mobile_sensors_ms.value
        overlays = checkbox_btn_group.active
        path_flag = False
        if 3 in overlays:
            path_flag = True
        selectedMobileSensors.clear()
        sid,x,y,clr,val,user, x_path, y_path,img=[],[],[],[],[],[],[],[],[]
        
        data_new_mobile = collections.OrderedDict({
                'sid':sid,
                'x_loc': x,
                'y_loc': y,
                'colo':clr,
                'value':val,
                'user':user,
                'url':img,
                })
        source_mobile.data = data_new_mobile
        
        df_path = pd.DataFrame(columns=['sid','x', 'y'])
        data_path = collections.OrderedDict({
            'x_path': x_path,
            'y_path': y_path,
            })
        source_path.data = data_path
        safety_thresh = safe_threshold.value
        for name in selected:
            selectedMobileSensors.append(name.split("_",1)[1])
        
        img=[greencar]*len(selectedMobileSensors)                
        for sensor in selectedMobileSensors:
            col_x = '(\'x\', \'{}\')'.format(sensor)
            col_y = '(\'y\', \'{}\')'.format(sensor)
            sid.append(sensor)
            x.append(df_mobile_location_cur[col_x].loc[df_mobile_location_cur['Timestamp']==time_current].values.item())
            y.append(df_mobile_location_cur[col_y].loc[df_mobile_location_cur['Timestamp']==time_current].values.item())
            val1 = df_mobile_reading_cur[sensor].loc[df_mobile_reading_cur['Timestamp']==time_current].values.item()
            if val1 == None:
                val1 = 0
            user.append(df_mobileUsers['user'].loc[df_mobileUsers['sensor']==int(sensor)].values.item())
            if int(float(val1))>safety_thresh:
                clr.append('darkred')
                #clr.append(redcar)
            else:
                clr.append('lawngreen')
                #clr.append(greencar)
            val.append(val1)
            #clr.append(RGB( 255 - int(sensor), (int(sensor)*2)+50, int(sensor)*4))
            if path_flag == True:
                df_temp = pd.DataFrame()
                df_temp['x'] = df_mobile_location_cur[col_x]
                df_temp['y'] = df_mobile_location_cur[col_y]
                df_temp['sid'] = sensor
                df_path = df_path.append(df_temp)
            
        
        data_new_mobile = collections.OrderedDict({
                'sid':sid,
                'x_loc': x,
                'y_loc': y,
                'colo':clr,
                'value':val,
                'user':user,
                'url':img,
                })
        source_mobile.data = data_new_mobile
        
        if path_flag == True:
            data_path = collections.OrderedDict({
                'x_path': [df_path['x'].loc[df_path['sid']==i] for i in selectedMobileSensors],
                'y_path': [df_path['y'].loc[df_path['sid']==i] for i in selectedMobileSensors],
                })
            source_path.data = data_path
            #df_path.to_csv('total_path.csv', index=None, header=True)
        #path_data = df_path.groupby('sid')
        #plot_sensor_path(selectedMobileSensors, df_path)    
    
    def update_safeT(attr, old, new):
        global safety_thresh
        safety_thresh = safe_threshold.value
    
    def update_time(attr, old, new):
        greencar = 'https://i.imgur.com/YyWzmgH.png'
        safety_thresh = safe_threshold.value
        time_current = datetime.fromtimestamp(timeline.value + baseTime)
        text = template.format(curTime = time_current)
        label.text=str(time_current)
        some_div.text = text
        sid,x,y,clr,val,user,img=[],[],[],[],[],[],[]
        
        if 2 in checkbox_btn_group.active:
            radiationFlag = True
        else:
            radiationFlag = False
        if radiationFlag == True:
            time1 = str(time_current)
            new_data3 = json_data(time1)
            geosource.geojson = new_data3
            
  
        data_new_mobile = collections.OrderedDict({
                'sid':sid,
                'x_loc': x,
                'y_loc': y,
                'colo':clr,
                'value':val,
                'user':user,
                'url':img,
                })
        source_mobile.data = data_new_mobile
        
        data_new_static = collections.OrderedDict({
                'sid':sid,
                'x_loc': x,
                'y_loc': y,
                'value':val,
                'user':user,
                })
        source_static.data = data_new_static
        img=[greencar]*len(selectedMobileSensors)  
        for sensor in selectedMobileSensors:
            col_x = '(\'x\', \'{}\')'.format(sensor)
            col_y = '(\'y\', \'{}\')'.format(sensor)
            sid.append(sensor)
            x.append(df_mobile_location_cur[col_x].loc[df_mobile_location_cur['Timestamp']==time_current].values.item())
            y.append(df_mobile_location_cur[col_y].loc[df_mobile_location_cur['Timestamp']==time_current].values.item())
            val1 = df_mobile_reading_cur[sensor].loc[df_mobile_reading_cur['Timestamp']==time_current].values.item()
            if val1 == None:
                val1 = 0
            if int(float(val1))>safety_thresh:
                clr.append('red')
                #clr.append(redcar)
            else:
                clr.append('green')
                #clr.append(greencar)
            #clr.append(RGB( 255 - int(sensor), (int(sensor)*2)+50, int(sensor)*4))
            val.append(val1)
            user.append(df_mobileUsers['user'].loc[df_mobileUsers['sensor']==int(sensor)].values.item())

        data_new_mobile = collections.OrderedDict({
                'sid':sid,
                'x_loc': x,
                'y_loc': y,
                'colo':clr,
                'value':val,
                'user':user,
                'url':img,
                })
        source_mobile.data = data_new_mobile
        x,y,val,user,sid = [],[],[],[],[]
        for sensor in selectedStaticSensors:
            sid.append(sensor)
            x.append(df_staticLocation['x'].loc[df_staticLocation['sid']==int(sensor)].values.item())
            y.append(df_staticLocation['y'].loc[df_staticLocation['sid']==int(sensor)].values.item())
            val.append(df_static_reading_cur[sensor].loc[df_static_reading_cur['Timestamp']==time_current].values.item())
            user.append('Sensor '+sensor)
            
         
        data_new_static = collections.OrderedDict({
                'sid':sid,
                'x_loc': x,
                'y_loc': y,
                'value':val,
                'user':user,
                })
        source_static.data = data_new_static
        
    def clearStaticSensors():
        sid,x,y,clr,val,user=[],[],[],[],[],[]
        static_sensors_ms.value = []
        data_new_static = collections.OrderedDict({
                'sid':sid,
                'x_loc': x,
                'y_loc': y,
                'value':val,
                'user':user,
                })
        source_static.data = data_new_static
    def clearMobileSensors():
        mobile_sensors_ms.value = []
        sid,x,y,clr,val,user, x_path, y_path,img=[],[],[],[],[],[],[],[],[]
        data_path = collections.OrderedDict({
            'x_path': x_path,
            'y_path': y_path,
            })
        source_path.data = data_path
        data_new_mobile = collections.OrderedDict({
                'sid':sid,
                'x_loc': x,
                'y_loc': y,
                'colo':clr,
                'value':val,
                'user':user,
                'url':img,
                })
        source_mobile.data = data_new_mobile
     
    def animate_update():
        time_current = timeline.value + timeline.step
        if time_current > time_end:
            time_current = time_start
        timeline.value = time_current
        update_time(None, None, None)
        
    def animate():
        global callback_id
        if btn_animate.label == '► Play':
            btn_animate.label = '❚❚ Pause'
            callback_id = curdoc().add_periodic_callback(animate_update, 200)
        else:
            btn_animate.label = '► Play'
            curdoc().remove_periodic_callback(callback_id)
            
    def json_data(timestamp):
        #time = df_hour_data['Timestamp'].loc[df_hour_data['Timestamp'] ==timestamp]
        time1 = pd.to_datetime(timestamp)
        time1 = time1.replace(minute=0, second=0)
        timestamp = str(time1.to_pydatetime())
        df_temp = df_hour_data_group.get_group(timestamp)
        merged = stHimarkShape.merge(df_temp, left_on = 'Nbrhood', right_on ='Neighbourhood', how = 'left')
        merged_json = json.loads(merged.to_json())
        return json.dumps(merged_json)

    #Declare all the variables and datasources here     
    plotter, stHimarkShape, gsource = displayMap()
    selectedStaticSensors, selectedMobileSensors = [],[]
    time_start = 0
    time_end = 1
    time_current = 0
    safety_thresh = 40
    #Get Dataframe for static sensors
    sid,x,y,clr,val,user,x_path, y_path, img=[],[],[],[],[],[],[],[],[]
    data_static = collections.OrderedDict({
            'sid':sid,
            'x_loc': x,
            'y_loc': y,
            'value': val,
            })
    source_static = ColumnDataSource(data=data_static) 
    
    data_mobile = collections.OrderedDict({
            'sid': sid,
            'x_loc': x,
            'y_loc': y,
            'colo':clr,
            'value': val,
            'user':user,
            'url':img,
            })
    source_mobile = ColumnDataSource(data=data_mobile)
    
    
    data_path = collections.OrderedDict({
            'x_path': [x_path],
            'y_path': [y_path],
            })
    source_path = ColumnDataSource(data=data_path)
    
    url = join(basename(split(dirname(__file__))[0]), 'data', 'total_path.csv')
    df_tp = pd.read_csv(url)
    data_path1 = collections.OrderedDict({
                'x_path': [df_tp['x'].loc[df_tp['sid']==i] for i in range(1,51)],
                'y_path': [df_tp['y'].loc[df_tp['sid']==i] for i in range(1,51)],
                })
    source_path1 = ColumnDataSource(data=data_path)
     
    df_staticSensors_hr = getDFfromDB("StaticSensorReading_hours")
    df_mobileSensors_hr = getDFfromDB("MobileSensorReading_hours")
    
    df_staticSensors_min = getDFfromDB("StaticSensorReading_minutes")
    df_mobileSensors_min = getDFfromDB("MobileSensorReading_minutes")
    
    df_staticSensors_raw = getDFfromDB("StaticSensorReading_raw")
    df_mobileSensors_raw = getDFfromDB("MobileSensorReading_raw")
    
    df_staticLocation = getDFfromDB("StaticSensorLocation")
    df_hospitalLocation = getDFfromDB("HospitalLocation")
    df_mobileLocation_hr = getDFfromDB("MobileSensorLocation_hours")
    df_mobileLocation_min = getDFfromDB("MobileSensorLocation_minutes")
    df_mobileLocation_raw = getDFfromDB("MobileSensorLocation_raw")
    #read mobile sensor users data
    url = join(basename(split(dirname(__file__))[0]), 'data', 'mobileuser.csv')
    df_mobileUsers = pd.read_csv(url)
    
    
    df_mobileLocation_hr['Timestamp'] = pd.to_datetime(df_mobileLocation_hr['Timestamp'])
    df_mobileLocation_min['Timestamp'] = pd.to_datetime(df_mobileLocation_min['Timestamp'])
    df_mobileLocation_raw['Timestamp'] = pd.to_datetime(df_mobileLocation_raw['Timestamp'])
    df_mobileSensors_hr['Timestamp'] = pd.to_datetime(df_mobileSensors_hr['Timestamp'])
    df_mobileSensors_min['Timestamp'] = pd.to_datetime(df_mobileSensors_min['Timestamp'])
    df_mobileSensors_raw['Timestamp'] = pd.to_datetime(df_mobileSensors_raw['Timestamp'])
    df_staticSensors_hr['Timestamp'] = pd.to_datetime(df_staticSensors_hr['Timestamp'])
    df_staticSensors_min['Timestamp'] = pd.to_datetime(df_staticSensors_min['Timestamp'])
    df_staticSensors_raw['Timestamp'] = pd.to_datetime(df_staticSensors_raw['Timestamp'])
    
    df_static_reading_cur = df_staticSensors_raw
    df_mobile_reading_cur = df_mobileSensors_raw
    df_mobile_location_cur = df_mobileLocation_raw
    
    
    
    #Radiation Map
    url = join(basename(split(dirname(__file__))[0]), 'data', 'df_hour_combined.csv')
    df_hour_data = pd.read_csv(url)
    df_hour_data_group = df_hour_data.groupby('Timestamp')
    time = df_hour_data['Timestamp'][0]
    df_first = df_hour_data_group.get_group(time)
    merged = stHimarkShape.merge(df_first, left_on = 'Nbrhood', right_on = 'Neighbourhood')
    

    static_list = [1,4,6,9,11,12,13,14,15]
    mobile_list = list(range(1,51))
    static_sensor_list = {}
    mobile_sensor_list = {}
    for sensor in static_list:
        static_sensor_list.update({int(sensor): "Sensor_"+str(sensor)})
    for sensor in mobile_list:
        mobile_sensor_list.update({int(sensor): "Sensor_"+str(sensor)})
    static_sensor_list= collections.OrderedDict(sorted(static_sensor_list.items()))
    mobile_sensor_list= collections.OrderedDict(sorted(mobile_sensor_list.items()))
    
    
    df_staticSensors_hr['Timestamp'] = pd.to_datetime(df_staticSensors_hr['Timestamp'])
    time_start = df_staticSensors_hr['Timestamp'][0]
    time_current = time_start
    time_end = df_staticSensors_hr['Timestamp'][len(df_staticSensors_hr.index)-1]
    baseTime = datetime.timestamp(time_start)
    time_start = datetime.timestamp(time_start) - baseTime
    time_end = datetime.timestamp(time_end) - baseTime

    #Widget: Multiselect --- Create two multiselect widgets for static and mobile sensors
    static_sensors_ms = MultiSelect(title="Static Sensors:",
                           options=list(static_sensor_list.values()),
                           height=250)
    static_sensors_ms.on_change('value', static_sensors_update)
    
    mobile_sensors_ms = MultiSelect(title="Mobile Sensors:",
                           options=list(mobile_sensor_list.values()),
                           height=250)
    mobile_sensors_ms.on_change('value', mobile_sensors_update)
    controls = WidgetBox(row([static_sensors_ms,mobile_sensors_ms]))
    btn_staticClear = Button(label='Clear Static Selection')
    btn_mobileClear = Button(label='Clear Mobile Selection')
    btn_staticClear.on_click(clearStaticSensors)
    btn_mobileClear.on_click(clearMobileSensors)
    btn_group = WidgetBox(row([WidgetBox(btn_staticClear, width=310),WidgetBox(btn_mobileClear, width=310)]))
    overlay_div = Div(text='<b>Map Overlays</b>' , style={'font-size': '120%', 'color': 'black'})
    
    checkbox_btn_group = CheckboxButtonGroup(labels=['Show Hospitals', 'Hospital Vornoi Map', 'Radiation Map', 'Trace Paths'], active=[])
    checkbox_btn_group.on_change('active', updateOverlays)
    checkbox_btn_group1 = CheckboxButtonGroup(labels=['State Labels', 'Trace Motion Map'], active=[])
    checkbox_btn_group1.on_change('active', updateMotionMap)

    timeframe_div = Div(text='<b>Time Frame</b>' , style={'font-size': '120%', 'color': 'black'})
    time_frame = RadioButtonGroup(labels=["Raw", "By Minutes", "By Hours"], active=0, name="Sort By:")
    time_frame.on_change('active', update_time_frame)
    template=("""
              <b>Timestamp: </b> <span class='number'>{curTime}</span>
              """)
    text = template.format(curTime = time_current)
    some_div = Div(text=text , style={'font-size': '100%', 'color': 'black'})
    timeline = Slider(title="", value=0, start=time_start, end=time_end, step=5)
    timeline.show_value = False
    timeline.on_change('value', update_time)
    btn_animate = Button(label='► Play', width=180)
    btn_animate.on_click(animate)
    
    x_patch, y_patch, x_vor_ls, y_vor_ls = [], [], [], []
    patch_data = dict(xs=x_patch, ys=y_patch)
    lines_data = dict(xs=x_vor_ls, ys=y_vor_ls)
    source_vor = ColumnDataSource()
    source_vor_ls = ColumnDataSource()
    source_vor.data = patch_data
    source_vor_ls.data = lines_data
    h_x, h_y,h_url = [], [],[]
    hospital_data = dict(url=h_url, x=h_x, y = h_y)
    source_hospital = ColumnDataSource()
    source_hospital.data = hospital_data
    
    w_s, h_s=[],[]
    states_data = dict(url=h_url, x=h_x, y = h_y, w = w_s, h = h_s)
    source_states = ColumnDataSource()
    source_states.data = states_data
    
    
    palette = brewer['RdYlGn'][5]
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 50)
    merged_json = json.loads(merged.to_json())
    json_data1 = json.dumps(merged_json)
    geosource = GeoJSONDataSource(geojson = json_data1)
    
    tick_labels = {'0': '0', '10': '10', '20':'20', '30':'30', '40':'40', '50':'>50'}
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=5,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    plotter.add_layout(color_bar, 'below')

    mp = Patches(xs ='xs', ys='ys', fill_color = 'lightslategrey', line_color="black", line_width=0.05, fill_alpha=0.5)
    plotter.add_glyph(geosource, mp)

    plotter.patches('xs', 'ys', source=source_vor, alpha=0.3, line_width=1, fill_color='lightslategrey', line_color='black')
    plotter.multi_line('xs', 'ys', source=source_vor_ls, alpha=1, line_width=1, line_color='black')
    
    safe_threshold = Slider(title="Safety Threshold(In cpm)", value=safety_thresh, start=0, end=100, step=1)
    safe_threshold.on_change('value', update_safeT)
    layout = column(row([plotter,column([controls,btn_group,overlay_div, checkbox_btn_group,checkbox_btn_group1,timeframe_div, time_frame, row([some_div, btn_animate]), timeline, safe_threshold])]))

    glyph = MultiLine(xs="x_path", ys="y_path", line_color="saddlebrown", line_width=0.8, line_alpha=0.5)
    plotter.add_glyph(source_path1, glyph)
    glyph = MultiLine(xs="x_path", ys="y_path", line_color="darkred", line_width=2, line_alpha=0.9)
    plotter.add_glyph(source_path, glyph)


    image1 = ImageURL(url='url', x="x", y="y", w=600, h=600, anchor="center")
    plotter.add_glyph(source_hospital, image1)
    
    image_states = ImageURL(url='url', x="x", y="y", w="w", h="h", anchor="center")
    plotter.add_glyph(source_states, image_states)
    
    label = Label(x=-13358000, y=2000, text=str(time_current), text_font_size='20pt', text_color='yellowgreen')
    plotter.add_layout(label)
    plotter.hex(name = "static_hover", x='x_loc', y='y_loc', color = "yellow", size=12, alpha=1, source = source_static)
    
    carimage = ImageURL(url='url', x='x_loc', y='y_loc', w=600, h= 1100, anchor='center')
    plotter.add_glyph(source_mobile, carimage)
    
    plotter.circle(name = "dynamic_hover", x='x_loc', y='y_loc', fill_color = 'colo', line_color='colo', size=6, alpha=1, source = source_mobile)
    hover = HoverTool(names= ["static_hover", "dynamic_hover"], tooltips=[("Sensor","@sid"), ("Radiation","@value"), ("User","@user")], show_arrow=False)
    plotter.tools = [hover]
    #plotter.diamond(x='x', y ='y', color='green',size=15, source = source_hospital)
    img_path="https://upload.wikimedia.org/wikipedia/commons/b/b8/Nuclear_plant.svg"
    plotter.image_url(url=[img_path], x=-13334385.723761385, y=18109.34344275895, w=1000, h=1000, anchor='center')
    tab = Panel(child=layout, title='Visual Analysis')
    
    return tab