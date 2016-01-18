#!/usr/bin/python


def make_plate(width,iwidth,height,iheight,thickness,wsplit,hsplit,bottom,bottomshift,top,topshift,left,leftshift,right,rightshift):
    wsplit=wsplit * 2+1
    hsplit=hsplit * 2+1

    if iwidth==False:
        width-=thickness*2
    if iheight==False:
        height-=thickness*2


    wstep=width/wsplit
    hstep=height/hsplit        
    points= []
    x=0
    y=0
    direction = 1
    
    if bottom in "f":
        direction=-1
        y=thickness

    if bottomshift:
        y+=thickness
    if leftshift:
        x-=thickness

    if bottom=='-':            
        points.append((x,y))
        x+=wsplit*wstep
        if leftshift:
            x+=thickness
        if rightshift:
            x+=thickness
        points.append((x,y))
    else:
        for i in range(wsplit):                 
            points.append((x,y))
            if i==0 and leftshift:   
                x=x+wstep+thickness
            elif i==wsplit-1 and rightshift:
                x=x+wstep+thickness
            else:
                x=x+wstep
            points.append((x,y))
            y=y+direction*thickness
            direction*=-1
        y=y+direction*thickness

    if right == bottom:
        direction*=-1
    if bottom=='-':
        if right=='f':
            direction=-1
        else:
            direction=1
    if right == '-':
        points.append((x,y))
        y=y-hstep*hsplit
        if bottomshift:
            y-=thickness
        if topshift:
            y-=thickness
        points.append((x,y))
    else:                
        for i in range(hsplit):
            points.append((x,y))
            if i==0 and bottomshift:
                y=y-hstep-thickness
            elif i==hsplit-1 and topshift:
                y=y-hstep-thickness
            else:
                y=y-hstep
            points.append((x,y))
            x=x+direction*thickness
            direction*=-1            
        x=x+direction*thickness
    if top != right:
        direction*=-1
    if right=='-':
        if top=='m':
            direction=-1
        else:
            direction=1
    if top == '-':
        points.append((x,y))
        x=x-wstep*wsplit
        if rightshift:
            x-=thickness
        if leftshift:
            x-=thickness
        points.append((x,y))            
    else:
        for i in range(wsplit):
            points.append((x,y))
            if i==0 and rightshift:
                x=x-wstep-thickness
            elif i==wsplit-1 and leftshift:
                x=x-wstep-thickness
            else:
                x=x-wstep
            points.append((x,y))
            y=y+direction*thickness
            direction*=-1            
        y=y+direction*thickness
    if left == top:
        direction*=-1
    if top=='-':
        if left=='m':
            direction=-1
        else:
            direction=1
    if left == '-':
        points.append((x,y))
        y=y+hstep*hsplit
        if topshift:
            y+=thickness
        if bottomshift:
            y+=thickness
        points.append((x,y))                
    else:
        for i in range(hsplit):
            points.append((x,y))
            if i==0 and topshift:
                y=y+hstep+thickness
            elif i==hsplit-1 and bottomshift:
                y=y+hstep+thickness
            else:
                y=y+hstep
            points.append((x,y))
            x=x+direction*thickness
            direction*=-1

    return points


def translate_points(p,x,y):
    return [(a+x,b+y) for (a,b) in p]

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

if __name__ == '__main__':
    print make_plate(100,True,100,True,3,5,5,'m',False,'m',False,'m',False,'m',False)
