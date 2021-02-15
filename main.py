# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# Each tab is drawn by one script
from scripts.mapViz import map_viz_tab
from scripts.dataViz import data_viz_tab
from scripts.sensors import sensor_uncertainity_tab
from scripts.states import state_count_tab



# Create each of the tabs
#db_filename = "static/dinofun_small.db"
tab1 = map_viz_tab()
tab2 = state_count_tab()
tab3 = sensor_uncertainity_tab()
tab4 = data_viz_tab()


# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2, tab3, tab4])

# Put the tabs in the current document for display
curdoc().add_root(tabs)