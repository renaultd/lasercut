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
        self.OptionParser.add_option('-l', '--length', action = 'store',
          type = 'float', dest = 'length', default = '10',
          help = 'length')
        self.OptionParser.add_option('-t', '--thickness', action = 'store',
          type = 'float', dest = 'thickness', default = '3',
          help = 'thickness')
        self.OptionParser.add_option('-k', '--type', action = 'store',
          type = 'string', dest = 'jtype', default = 'm',
          help = 'type')
        self.OptionParser.add_option('-s', '--split', action = 'store',
          type = 'int', dest = 'split', default = '3',
          help = 'splite')
        self.OptionParser.add_option('-u', '--unit', action = 'store',
          type = 'string', dest = 'unit', default = 'mm',
          help = 'unit')
        
    def effect(self):
        length = self.unittouu(str(self.options.length)+self.options.unit)
        thickness = self.unittouu(str(self.options.thickness)+self.options.unit)
        split=self.options.split

        points= []
        x=0
        step=length/split
        y=0
        direction = 1
        if self.options.jtype=="f":
            direction=-1
        while x < length:
            points.append((x,y))
            points.append((x+step,y))
            y=y+direction*thickness
            x=x+step
            direction*=-1

        path = points_to_svgd(points)

        t = 'translate(' + str(self.view_center[0]) + ',' + \
            str(self.view_center[1]) + ')'
        g_attribs = {
            inkex.addNS('label', 'inkscape'): 'RackGear' + str(length),
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
