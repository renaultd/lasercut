#!/usr/bin/python

import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
from simplestyle import *

import simpletransform

import lc
import re

class HDistanceEffect(inkex.Effect):    
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('--distance', action = 'store',
          type = 'float', dest = 'distance', default = '10',
          help = 'distance')
        self.OptionParser.add_option('--moving', action = 'store',
          type = 'string', dest = 'moving', default = 'right',
          help = 'moving')
        self.OptionParser.add_option('--left', action = 'store',
          type = 'string', dest = 'left', default = 'right',
          help = 'left')
        self.OptionParser.add_option('--right', action = 'store',
          type = 'string', dest = 'right', default = 'right',
          help = 'right')
        self.OptionParser.add_option('--unit', action = 'store',
          type = 'string', dest = 'unit', default = 'mm',
          help = 'unit')        
    def effect(self):
        distance=self.unittouu(str(self.options.distance)+self.options.unit)
        if len(self.options.ids)!=2:
            print >>sys.stderr,"you must select exactly two objects"
            return
        id1=self.options.ids[0]
        id2=self.options.ids[1]
        b1=simpletransform.computeBBox([self.selected[id1],])
        b2=simpletransform.computeBBox([self.selected[id2],])        
        if b1[0]>b2[0]:
            b1,b2=(b2,b1)
            id1,id2=(id2,id1)
        # id1,b1 is for the left element
        # id2,b2 is for the right element
        if self.options.left=='l':
            left=b1[0]
        else:
            left=b1[1]
        if self.options.right=='l':
            right=b2[0]
        else:
            right=b2[1]
        # left is the reference coord for the left element
        # right ..............................right.......        
        if self.options.moving=='l':
            moving=self.selected[id1]
            delta=(right-left)-distance
        else:
            moving=self.selected[id2]
            delta=-(right-left)+distance
        #print >>sys.stderr,distance,left,right,delta         
        #print >>sys.stderr,self.selected,b1,b2,delta,distance
        # translate
        #print >>sys.stderr,self.selected[id2].attrib['transform']
        m=re.search('translate.*\(([0-9-.]+),.*',moving.attrib.get('transform',''))
        #print >>sys.stderr,"match is:",m
        if m!=None:
            delta=delta+float(m.group(1))
        #print >>sys.stderr,"delta is:",delta
        moving.attrib['transform']='translate('+str(delta)+',0)'
        
            

effect = HDistanceEffect()
effect.affect()
