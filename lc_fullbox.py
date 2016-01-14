import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
from simplestyle import *

import lc


class FullBoxEffect(inkex.Effect):    
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('--width', action = 'store',
          type = 'float', dest = 'width', default = '10',
          help = 'width')
        self.OptionParser.add_option('--depth', action = 'store',
          type = 'float', dest = 'depth', default = '10',
          help = 'depth')
        self.OptionParser.add_option('--height', action = 'store',
          type = 'float', dest = 'height', default = '10',
          help = 'height')
        self.OptionParser.add_option('--thickness', action = 'store',
          type = 'float', dest = 'thickness', default = '3',
          help = 'thickness')
        self.OptionParser.add_option('--wsplit', action = 'store',
          type = 'int', dest = 'wsplit', default = '3',
          help = 'horizontal splite')
        self.OptionParser.add_option('--dsplit', action = 'store',
          type = 'int', dest = 'dsplit', default = '3',
          help = 'depth splite')
        self.OptionParser.add_option('--hsplit', action = 'store',
          type = 'int', dest = 'hsplit', default = '3',
          help = 'vertical splite')
        self.OptionParser.add_option('--unit', action = 'store',
          type = 'string', dest = 'unit', default = 'mm',
          help = 'unit')        
        self.OptionParser.add_option('--inner', action = 'store',
          type = 'inkbool', dest = 'inner', default = 'True',
          help = 'inner')
    def effect(self):
        width=self.unittouu(str(self.options.width)+self.options.unit)
        height=self.unittouu(str(self.options.height)+self.options.unit)
        depth=self.unittouu(str(self.options.depth)+self.options.unit)
        thickness=self.unittouu(str(self.options.thickness)+self.options.unit)


        t = 'translate(' + str(self.view_center[0]) + ',' + \
            str(self.view_center[1]) + ')'
        g_attribs = {
            inkex.addNS('label', 'inkscape'): 'Box' + str(width) + "x"+str(height),
            'transform': t}
        g = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)

        # Create SVG Path for plate
        style = {'stroke': '#000000', 'fill': 'none', 'stroke-width': str(self.unittouu('1px'))}

        #make bottom plate:
        points=lc.make_plate(width,self.options.inner,depth,self.options.inner,
                             thickness,self.options.wsplit,self.options.dsplit,
                             'm',False,
                             'm',False,
                             'm',False,
                             'm',False)
        
        path = lc.points_to_svgd(points)        
        
        box_attribs = {
            'style': formatStyle(style),
            'd': path}
        box = inkex.etree.SubElement(
            g, inkex.addNS('path', 'svg'), box_attribs)
        
        #make top plate:
        points=lc.make_plate(width,self.options.inner,depth,self.options.inner,
                             thickness,self.options.wsplit,self.options.dsplit,
                             'm',False,
                             'm',False,
                             'm',False,
                             'm',False)

        points=lc.translate_points(points,width*1.1,depth*1.1)              
        path = lc.points_to_svgd(points)  

        
        box_attribs = {
            'style': formatStyle(style),
            'd': path}
        box = inkex.etree.SubElement(
            g, inkex.addNS('path', 'svg'), box_attribs)
        
        #make back plate:
        points=lc.make_plate(width,self.options.inner,height,self.options.inner,
                             thickness,self.options.wsplit,self.options.hsplit,
                             'f',False,
                             'f',False,
                             'f',True,
                             'm',False)
        points=lc.translate_points(points,0,-(depth*1.1))
        path = lc.points_to_svgd(points)        
        
        box_attribs = {
            'style': formatStyle(style),
            'd': path}
        box = inkex.etree.SubElement(
            g, inkex.addNS('path', 'svg'), box_attribs)
        
        #make front plate:
        points=lc.make_plate(width,self.options.inner,height,self.options.inner,
                             thickness,self.options.wsplit,self.options.hsplit,
                             'f',False,
                             'f',False,
                             'm',False,
                             'f',True)
        points=lc.translate_points(points,0,height*1.1)
        path = lc.points_to_svgd(points)        
        
        box_attribs = {
            'style': formatStyle(style),
            'd': path}
        box = inkex.etree.SubElement(
            g, inkex.addNS('path', 'svg'), box_attribs)
        
        #make left plate:
        points=lc.make_plate(height,self.options.inner,depth,self.options.inner,
                             thickness,self.options.hsplit,self.options.dsplit,
                             'f',True,
                             'm',False,
                             'f',False,
                             'f',False)
        points=lc.translate_points(points,-(height*1.1),0)
        path = lc.points_to_svgd(points)        
        
        box_attribs = {
            'style': formatStyle(style),
            'd': path}
        box = inkex.etree.SubElement(
            g, inkex.addNS('path', 'svg'), box_attribs)
        
        #make right plate:
        points=lc.make_plate(height,self.options.inner,depth,self.options.inner,
                             thickness,self.options.dsplit,self.options.hsplit,
                             'm',False,
                             'f',True,
                             'f',False,
                             'f',False)
        points=lc.translate_points(points,width*1.1,0)
        path = lc.points_to_svgd(points)        
        
        box_attribs = {
            'style': formatStyle(style),
            'd': path}
        box = inkex.etree.SubElement(
            g, inkex.addNS('path', 'svg'), box_attribs)
        


effect = FullBoxEffect()
effect.affect()


            
        
