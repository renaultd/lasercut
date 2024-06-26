#!/usr/bin/python

import lxml
import sys
# sys.path.append('/usr/share/inkscape/extensions')

import inkex
from simplestyle import *

import simpletransform

import lc
import math
import random

PI = math.pi

def rotate(p, ang):
    return (p[0]*math.cos(ang) - p[1]*math.sin(ang),
            p[0]*math.sin(ang) + p[1]*math.cos(ang))

def star_path(n, radius):
    ang = 0; dang = 2*PI / n; res = []
    # Create random external path
    efactor = 0.5; eradius = radius; eangle = 0
    path = [ ]
    points = [ (radius, 0) ]
    numi   = random.randint(3,8)
    for i in range(numi):
        eradius = radius*(1-(1-efactor)*float(i+1)/(numi+1))
        eangle  = 0.1 + (dang*0.5-0.2)*random.random()
        points.append(rotate((eradius, 0), eangle))
    points.append(rotate((efactor*radius, 0),dang/2))
    # Reverse it
    pointssym = list(map(lambda p : (p[0],-p[1]), points))
    pointssym.pop(0)
    for i in range(n):
        newpoints = list(map(lambda p : rotate(p,ang), points))
        path.extend(newpoints)
        newpoints = reversed(list(map(lambda p : rotate(p,ang+dang), pointssym)))
        path.extend(newpoints)
        ang += dang
    path.append((radius,0))
    res.append(path)
    # Create internal paths
    ang = 0
    eradius = efactor*radius
    points = [ rotate((eradius*0.85,0),dang*0.5),
               rotate((eradius*0.85,0),eangle) ]
    points.append(rotate((eradius*0.65,0),0.2))
    points.append(rotate((eradius*0.45,0),eangle))
    points.append(rotate((eradius*0.45,0),dang*0.5))
    # Reverse it
    pointssym = list(map(lambda p : rotate((p[0],-p[1]), dang), points))
    pointssym.reverse()
    pointssym.pop(0)
    points.extend(pointssym)
    #points.append(rotate((eradius*0.9,0),eangle))
    for i in range(n):
        path = list(map(lambda p : rotate(p, ang), points))
        res.append(path)
        ang += dang
    return res

class StarsEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument('--width', action = 'store',
          type = lc.arg_int, dest = 'width', default = '5',
          help = 'width')
        self.arg_parser.add_argument('--height', action = 'store',
          type = lc.arg_int, dest = 'height', default = '5',
          help = 'height')
        self.arg_parser.add_argument('--maxsides', action = 'store',
          type = lc.arg_int, dest = 'maxsides', default = '5',
          help = 'maxsides')
        self.arg_parser.add_argument('--minsides', action = 'store',
          type = lc.arg_int, dest = 'minsides', default = '5',
          help = 'minsides')
        self.arg_parser.add_argument('--radius', action = 'store',
          type = lc.arg_float, dest = 'radius', default = '5',
          help = 'radius')
        self.arg_parser.add_argument('--unit', action = 'store',
          type = lc.arg_string, dest = 'unit', default = 'mm',
          help = 'unit')

    def effect(self):
        width     = self.options.width
        height    = self.options.height
        minsides  = self.options.minsides
        maxsides  = self.options.maxsides
        radius    = self.options.radius
        g = lxml.etree.SubElement(self.svg.get_current_layer(), 'g', {})
        style = str(inkex.Style({ 'stroke': '#000000', \
                              'fill': 'none', \
                              'font-size' : "12px", \
                              'stroke-width': str(self.svg.unittouu('0.1mm')), \
                              'text-anchor' : 'middle'  }))

        for x in range(width):
            for y in  range(height):
                sn   = random.randint(minsides, maxsides)
                for p in star_path(sn, radius):
                    path = lc.translate_points(p,
                                               x*radius*2.1, y*radius*2.1)
                    lc.insert_path(g, path, style)

effect = StarsEffect()
effect.run()
