import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
from simplestyle import *

import lc


class PlateJoinEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('-w', '--width', action = 'store',
          type = 'float', dest = 'width', default = '10',
          help = 'width')
        self.OptionParser.add_option('-o', '--iwidth', action = 'store',
          type = 'inkbool', dest = 'iwidth', default = 'True',
          help = 'inner width')
        self.OptionParser.add_option('-p', '--height', action = 'store',
          type = 'float', dest = 'height', default = '10',
          help = 'height')
        self.OptionParser.add_option('-l', '--iheight', action = 'store',
          type = 'inkbool', dest = 'iheight', default = 'True',
          help = 'inner height')
        self.OptionParser.add_option('-t', '--thickness', action = 'store',
          type = 'float', dest = 'thickness', default = '3',
          help = 'thickness')
        self.OptionParser.add_option('--bottom', action = 'store',
          type = 'string', dest = 'bottom', default = 'm',
          help = 'bottom type')
        self.OptionParser.add_option('--bottomshift', action = 'store',
          type = 'inkbool', dest = 'bottomshift', default = 'False',
          help = 'bottom shift')
        self.OptionParser.add_option('--right', action = 'store',
          type = 'string', dest = 'right', default = 'm',
          help = 'right type')
        self.OptionParser.add_option('--rightshift', action = 'store',
          type = 'inkbool', dest = 'rightshift', default = 'False',
          help = 'right shift')
        self.OptionParser.add_option('--top', action = 'store',
          type = 'string', dest = 'top', default = 'm',
          help = 'top type')
        self.OptionParser.add_option('--topshift', action = 'store',
          type = 'inkbool', dest = 'topshift', default = 'False',
          help = 'top shift')
        self.OptionParser.add_option('--left', action = 'store',
          type = 'string', dest = 'left', default = 'm',
          help = 'left type')
        self.OptionParser.add_option('--leftshift', action = 'store',
          type = 'inkbool', dest = 'leftshift', default = 'False',
          help = 'left shift')
        self.OptionParser.add_option('-s', '--wsplit', action = 'store',
          type = 'int', dest = 'wsplit', default = '3',
          help = 'horizontal splite')
        self.OptionParser.add_option('-m', '--hsplit', action = 'store',
          type = 'int', dest = 'hsplit', default = '3',
          help = 'vertical splite')
        self.OptionParser.add_option('-u', '--unit', action = 'store',
          type = 'string', dest = 'unit', default = 'mm',
          help = 'unit')
        
    def effect(self):
        width = self.unittouu(str(self.options.width)+self.options.unit)
        height = self.unittouu(str(self.options.height)+self.options.unit)
        thickness = self.unittouu(str(self.options.thickness)+self.options.unit)

        points=lc.make_plate(width,self.options.iwidth,height,self.options.iheight,
                             thickness,self.options.wsplit,self.options.hsplit,
                             self.options.bottom,self.options.bottomshift,
                             self.options.top,self.options.topshift,
                             self.options.left,self.options.leftshift,
                             self.options.right,self.options.rightshift)
        
        # wsplit=self.options.wsplit * 2+1
        # hsplit=self.options.hsplit * 2+1

        # if self.options.iwidth==False:
        #     width-=thickness*2
        # if self.options.iheight==False:
        #     height-=thickness*2
        
        # wstep=width/wsplit
        # hstep=height/hsplit        
        # points= []
        # x=0
        # y=0
        # direction = 1
        # if self.options.bottom in "f":
        #     direction=-1
        #     y=thickness

        # if self.options.bottomshift:
        #     y+=thickness
        # if self.options.leftshift:
        #     x+=thickness
            
        # if self.options.bottom=='-':            
        #     points.append((x,y))
        #     x+=wsplit*wstep
        #     if self.options.leftshift:
        #         x-=thickness
        #     if self.options.rightshift:
        #         x-=thickness
        #     points.append((x,y))
        # else:
        #     for i in range(wsplit):                 
        #         points.append((x,y))
        #         if i==0 and self.options.leftshift:   
        #             x=x+wstep-thickness
        #         elif i==wsplit-1 and self.options.rightshift:
        #             x=x+wstep-thickness
        #         else:
        #             x=x+wstep
        #         points.append((x,y))
        #         y=y+direction*thickness
        #         direction*=-1
        #     y=y+direction*thickness
            
        # if self.options.right == self.options.bottom:
        #     direction*=-1
        # if self.options.bottom=='-':
        #     if self.options.right=='f':
        #         direction=-1
        #     else:
        #         direction=1
        # if self.options.right == '-':
        #     points.append((x,y))
        #     y=y-hstep*hsplit
        #     if self.options.bottomshift:
        #         y+=thickness
        #     if self.options.topshift:
        #         y+=thickness
        #     points.append((x,y))
        # else:                
        #     for i in range(hsplit):
        #         points.append((x,y))
        #         if i==0 and self.options.bottomshift:
        #             y=y-hstep+thickness
        #         elif i==hsplit-1 and self.options.topshift:
        #             y=y-hstep+thickness
        #         else:
        #             y=y-hstep
        #         points.append((x,y))
        #         x=x+direction*thickness
        #         direction*=-1            
        #     x=x+direction*thickness
        # if self.options.top != self.options.right:
        #     direction*=-1
        # if self.options.right=='-':
        #     if self.options.top=='m':
        #         direction=-1
        #     else:
        #         direction=1
        # if self.options.top == '-':
        #     points.append((x,y))
        #     x=x-wstep*wsplit
        #     if self.options.rightshift:
        #         x+=thickness
        #     if self.options.leftshift:
        #         x+=thickness
        #     points.append((x,y))            
        # else:
        #     for i in range(wsplit):
        #         points.append((x,y))
        #         if i==0 and self.options.rightshift:
        #             x=x-wstep+thickness
        #         elif i==wsplit-1 and self.options.leftshift:
        #             x=x-wstep+thickness
        #         else:
        #             x=x-wstep
        #         points.append((x,y))
        #         y=y+direction*thickness
        #         direction*=-1            
        #     y=y+direction*thickness
        # if self.options.left == self.options.top:
        #     direction*=-1
        # if self.options.top=='-':
        #     if self.options.left=='m':
        #         direction=-1
        #     else:
        #         direction=1
        # if self.options.left == '-':
        #     points.append((x,y))
        #     y=y+hstep*hsplit
        #     if self.options.topshift:
        #         y-=thickness
        #     if self.options.bottomshift:
        #         y-=thickness
        #     points.append((x,y))                
        # else:
        #     for i in range(hsplit):
        #         points.append((x,y))
        #         if i==0 and self.options.topshift:
        #             y=y+hstep-thickness
        #         elif i==hsplit-1 and self.options.bottomshift:
        #             y=y+hstep-thickness
        #         else:
        #             y=y+hstep
        #         points.append((x,y))
        #         x=x+direction*thickness
        #         direction*=-1
                
        path = lc.points_to_svgd(points)

        t = 'translate(' + str(self.view_center[0]) + ',' + \
            str(self.view_center[1]) + ')'
        g_attribs = {
            inkex.addNS('label', 'inkscape'): 'Box' + str(width) + "x"+str(height),
            'transform': t}
        g = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)

        # Create SVG Path for plate
        style = {'stroke': '#000000', 'fill': 'none', 'stroke-width': str(self.unittouu('1px'))}
        box_attribs = {
            'style': formatStyle(style),
            'd': path}
        box = inkex.etree.SubElement(
            g, inkex.addNS('path', 'svg'), box_attribs)    
        
effect = PlateJoinEffect()
effect.affect()
