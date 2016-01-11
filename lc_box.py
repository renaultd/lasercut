import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
from simplestyle import *

def points_to_svgd(p):
    """
    p: list of 2 tuples (x, y coordinates)
    """
    f = p[0]
    p = p[1:]
    svgd = 'M%.3f,%.3f' % f
    for x in p:
        svgd += 'L%.3f,%.3f' % x
    return svgd


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
          help = 'type')
        self.OptionParser.add_option('--right', action = 'store',
          type = 'string', dest = 'right', default = 'm',
          help = 'type')
        self.OptionParser.add_option('--top', action = 'store',
          type = 'string', dest = 'top', default = 'm',
          help = 'type')
        self.OptionParser.add_option('--left', action = 'store',
          type = 'string', dest = 'left', default = 'm',
          help = 'type')
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
        wsplit=self.options.wsplit * 2+1
        hsplit=self.options.hsplit * 2+1

        if self.options.iwidth==False:
            width-=thickness*2
        if self.options.iheight==False:
            height-=thickness*2
        
        wstep=width/wsplit
        hstep=height/hsplit        
        points= []
        x=0
        y=0
        direction = 1
        if self.options.bottom in "f":
            direction=-1
            y=thickness

        if self.options.bottom=='-':            
            points.append((x,y))
            x+=wsplit*wstep            
            points.append((x,y))
        else:
            for i in range(wsplit):
                points.append((x,y))
                points.append((x+wstep,y))
                y=y+direction*thickness
                x=x+wstep
                direction*=-1
            y=y+direction*thickness
            
        if self.options.right == self.options.bottom:
            direction*=-1
        if self.options.bottom=='-':
            if self.options.right=='f':
                direction=-1
            else:
                direction=1
        if self.options.right == '-':
            points.append((x,y))
            y=y-hstep*hsplit
            points.append((x,y))
        else:                
            for i in range(hsplit):
                points.append((x,y))
                points.append((x,y-hstep))
                y=y-hstep
                x=x+direction*thickness
                direction*=-1            
            x=x+direction*thickness
        if self.options.top != self.options.right:
            direction*=-1
        if self.options.right=='-':
            if self.options.top=='m':
                direction=-1
            else:
                direction=1
        if self.options.top == '-':
            points.append((x,y))
            x=x-wstep*wsplit
            points.append((x,y))            
        else:
            for i in range(wsplit):
                points.append((x,y))
                points.append((x-wstep,y))
                y=y+direction*thickness
                x=x-wstep
                direction*=-1            
            y=y+direction*thickness
        if self.options.left == self.options.top:
            direction*=-1
        if self.options.top=='-':
            if self.options.left=='m':
                direction=-1
            else:
                direction=1
        if self.options.left == '-':
            points.append((x,y))
            y=y+hstep*hsplit
            points.append((x,y))                
        else:
            for i in range(hsplit):            
                points.append((x,y))
                points.append((x,y+hstep))
                y=y+hstep
                x=x+direction*thickness
                direction*=-1          
            
        
        path = points_to_svgd(points)

        t = 'translate(' + str(self.view_center[0]) + ',' + \
            str(self.view_center[1]) + ')'
        g_attribs = {
            inkex.addNS('label', 'inkscape'): 'Box' + str(width) + "x"+str(height),
            'transform': t}
        g = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)

        # Create SVG Path for gear
        style = {'stroke': '#000000', 'fill': 'none', 'stroke-width': str(self.unittouu('1px'))}
        gear_attribs = {
            'style': formatStyle(style),
            'd': path}
        gear = inkex.etree.SubElement(
            g, inkex.addNS('path', 'svg'), gear_attribs)

        
#        what = self.options.what
#        svg = self.document.getroot()        
        # Again, there are two ways to get the attibutes:
#        width  = self.unittouu(svg.get('width'))
#        height = self.unittouu(svg.get('height'))
#        layer = inkex.etree.SubElement(svg, 'g')
#        layer.set(inkex.addNS('label', 'inkscape'), 'Hello %s Layer' % (what))
#        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')        
#        text = inkex.etree.Element(inkex.addNS('text','svg'))
#        l=self.options.length
#        text.text = "%f %f %f" % (self.unittouu(str(l)+"cm"),self.unittouu(str(l)+"mm"),self.unittouu(str(l)+"px"))
#        text.text = 'Hello %f %f %s %i!' % (self.options.length,self.options.thickness,self.options.jtype,self.options.split)
#        text.set('x', str(width / 2))
#        text.set('y', str(height / 2))
#        layer.append(text)
        
effect = PlateJoinEffect()
effect.affect()
