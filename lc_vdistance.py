#!/usr/bin/python

import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
from simplestyle import *

import simpletransform

import lc
import re

class VDistanceEffect(inkex.Effect):    
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('--distance', action = 'store',
          type = 'float', dest = 'distance', default = '10',
          help = 'distance')
        self.OptionParser.add_option('--moving', action = 'store',
          type = 'string', dest = 'moving', default = 't',
          help = 'moving')
        self.OptionParser.add_option('--top', action = 'store',
          type = 'string', dest = 'top', default = 't',
          help = 'top')
        self.OptionParser.add_option('--bottom', action = 'store',
          type = 'string', dest = 'bottom', default = 't',
          help = 'bottom')
    def effect(self):
        distance=self.unittouu(str(self.options.distance)+self.getDocumentUnit())
        if len(self.options.ids)!=2:
            print >>sys.stderr,"you must select exactly two objects"
            return
        id1=self.options.ids[0]
        id2=self.options.ids[1]
        b1=simpletransform.computeBBox([self.selected[id1],])
        b2=simpletransform.computeBBox([self.selected[id2],])
        if b1[2]>b2[2]:
            b1,b2=(b2,b1)
            id1,id2=(id2,id1)
        # id1,b1 is for the top element
        # id2,b2 is for the bottom element
        if self.options.top=='t':
            top=b1[2]
        else:
            top=b1[3]
        if self.options.bottom=='t':
            bottom=b2[2]
        else:
            bottom=b2[3]
        if self.options.moving=='t':
            moving=self.selected[id1]
            delta=(bottom-top)-distance
        else:
            moving=self.selected[id2]
            delta=-(bottom-top)+distance
        #print >>sys.stderr,distance,top,bottom,delta         
        #print >>sys.stderr,self.selected,b1,b2,delta,distance
        # translate
        #print >>sys.stderr,self.selected[id2].attrib['transform']
        m=re.search('translate.*\([0-9-.]+,([0-9-.]+).*\)',moving.attrib.get('transform',''))
        #print >>sys.stderr,"match is:",m
        if m!=None:
            delta=delta+float(m.group(1))
        #print >>sys.stderr,"delta is:",delta
        moving.attrib['transform']='translate(0,'+str(delta)+')'
        
            

effect = VDistanceEffect()
effect.affect()
