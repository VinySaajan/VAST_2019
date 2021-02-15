# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 23:07:55 2019

@author: Krishna Kinger
"""
from os.path import dirname, basename, split, join
import geopandas as gpd
from bokeh.plotting import figure
from pyproj import Proj, transform
from bokeh.models import (Button, Panel, ColorBar, ColumnDataSource, HoverTool)
from scipy.spatial import Voronoi
from collections import OrderedDict
from bokeh.models.glyphs import Patches
import numpy as np

def getPolyCoords(r, geom, coord_type):
    """Returns the coordinates ('x' or 'y') of edges of a Polygon exterior"""
    # Parse the exterior of the coordinate
    exterior = r[geom].exterior
    if coord_type == 'x':
        # Get the x coordinates of the exterior
        return list( exterior.coords.xy[0] )
    elif coord_type == 'y':
        # Get the y coordinates of the exterior
        return list( exterior.coords.xy[1] )

def displayMap():
    """ Method to display map and return the figure object """
    x_min,y_min = -13358338.895192828, 0.0
    x_max,y_max = -13326251.16329116, 26559.160710913176
    url = join(basename(split(dirname(__file__))[0]), 'data/StHimarkNeighborhoodShapefile', 'StHimark.shp')
    stHimarkShapeFile = gpd.read_file(url)
    stHimarkShape = gpd.read_file(url)
    stHimarkShape['x'] = stHimarkShape.apply(getPolyCoords, geom='geometry', coord_type='x', axis=1)
    stHimarkShape['y'] = stHimarkShape.apply(getPolyCoords, geom='geometry', coord_type='y', axis=1)
    g_df = stHimarkShape.drop('geometry', axis=1).copy()
    gsource = ColumnDataSource(g_df)
    map_shape = figure(title="StHimark map", x_range=(x_min, x_max), y_range=(y_min,y_max))
    glyph = Patches(xs= "x", ys="y", fill_alpha=0.6, fill_color='lightslategrey', line_color="black", line_width=0.1)
    #glyph = Patches(xs="x", ys="y", fill_color='lightslategrey')
    map_shape.add_glyph(gsource, glyph)
    map_shape.axis.visible = False
    map_shape.xgrid.visible = False
    map_shape.ygrid.visible = False
    return map_shape, stHimarkShapeFile, gsource
    

def get_voronoi(coord_x, coord_y):
        points = list(zip(coord_x, coord_y))
        #Get Voronoi points
        vor = Voronoi(points)
        
        x_patch, y_patch = [], []
        x1_patch, y1_patch = [], []
        # The Voronoi has 2 parts. The actual patches and the unbounded lines (that run #indefinitely)
        for region in vor.regions:
            if not -1 in region:
                x1_patch, y1_patch = [], []
                for i in region:
                    x1_patch.append(vor.vertices[i][0])
                    y1_patch.append(vor.vertices[i][1])
            x_patch.append(np.array(x1_patch))
            y_patch.append(np.array(y1_patch))
        
        #This code that gets the multi lines that run indefinitely
        center = vor.points.mean(axis=0)
        ptp_bound = vor.points.ptp(axis=0)
        
        line_segments = []
        for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
            simplex = np.asarray(simplex)
            if np.any(simplex < 0):
                i = simplex[simplex >= 0][0] # finite end Voronoi vertex
            
                t = vor.points[pointidx[1]] - vor.points[pointidx[0]] # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]]) # normal
                
                midpoint = vor.points[pointidx].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = vor.vertices[i] + direction * ptp_bound.max()
                
                line_segments.append([(vor.vertices[i, 0], vor.vertices[i, 1]),
                (far_point[0], far_point[1])])
        
        x_vor_ls, y_vor_ls = [], []
        for region in line_segments:
            x1, y1 = [], []
            for i in region:
                x1.append(i[0])
                y1.append(i[1])
        
            x_vor_ls.append(np.array(x1))
            y_vor_ls.append(np.array(y1))
        
        #Removing patches that were added multiple times.
        x_patch = list(OrderedDict((tuple(x), x) for x in x_patch).values())
        y_patch = list(OrderedDict((tuple(x), x) for x in y_patch).values())
        x_vor_ls = list(OrderedDict((tuple(x), x) for x in x_vor_ls).values())
        y_vor_ls = list(OrderedDict((tuple(x), x) for x in y_vor_ls).values())
        
        return x_patch, y_patch, x_vor_ls, y_vor_ls