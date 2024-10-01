#!/usr/bin/python
from enum import Enum, auto


################################################################
class Point:
    """A class that represents a 2D-point. And also potentially a
    2D-vector."""
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self): return self._x
    @property
    def y(self): return self._y

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def sub(self, other):
        return Point(self.x - other.x, self.y - other.y)
    def mult(self, scalar):
        return Point(self.x*scalar, self.y*scalar)
    def length(self):
        return (self.x**2 + self.y**2)**0.5
    def unit(self):
        len = self.length()
        return Point(self.x/len, self.y/len)
    def perp(self):
        return Point(-self.y, self.x)

    def min(self, other):
        return Point(min(self.x, other.x), min(self.y, other.y))

    def max(self, other):
        return Point(max(self.x, other.x), max(self.y, other.y))

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __repr__(self):
        return f"({self.x},{self.y})"

# Alias for the Point constructor
def P(x,y):
    return Point(x, y)


################################################################
class BoundingBox:
    """ A class that represents a 2D bounding box """
    def __init__(self, min, max):
        self._min = min
        self._max = max

    @property
    def min(self):  return self._min
    @property
    def max(self):  return self._max
    @property
    def xmin(self): return self._min.x
    @property
    def xmax(self): return self._max.x
    @property
    def ymin(self): return self._min.y
    @property
    def ymax(self): return self._max.y
    @property
    def lowerleft(self): return self._min
    @property
    def lowerright(self): return Point(self.xmax, self.ymin)
    @property
    def upperright(self): return self._max
    @property
    def upperleft(self): return Point(self.xmin, self.ymax)
    @property
    def width(self): return self._max.x - self._min.x
    @property
    def height(self): return self._max.y - self._min.y

    # Side-effects methods
    def union(self, other):
        self._min = self._min.min(other.min)
        self._max = self._max.max(other.max)

    def translate(self, a_point):
        self._min = self._min.add(a_point)
        self._max = self._max.add(a_point)
    def translate_to_origin(self):
        self.translate(self._min)

    def __repr__(self):
        return f"BB(({self.xmin},{self.ymin})->({self.xmax},{self.ymax}))"


################################################################
class Edge(BoundingBox):
    """A class that represents an edge in a 2D-box

    It is *not* just a segment in the plane, it is a part of the
    decomposition of the 2D-box in the plane. Also, it is *not* a part
    of the final printing, it remains in the 2D-world.

    """
    def __init__(self, min, max):
        super().__init__(min, max)
        self._touch  = []    # Edges on the extremities
        self._attch  = []    # Other edges touching this one

    @property
    def origin(self):   return self._min
    @property
    def dest(self):     return self._max
    @property
    def length(self):   return ((self.dest.x-self.origin.x)**2. +
                                (self.dest.y-self.origin.y)**2.)**0.5
    @property
    def attached_lengths(self):
        def al(an_edge):
            touching = an_edge.origin if self.contains(an_edge.origin) \
                else an_edge.dest
            return touching.sub(self.origin).length()
        return list(map(al, self._attch))

    # Given a point p, test if p is colinear with the edge
    def colinear(self, p, precision = 0.001):
        v1 = p.sub(self.origin)
        v2 = self.dest.sub(self.origin)
        return abs(v1.x*v2.y-v1.y*v2.x) < precision

    # Given a point p that is colinear with the edge, returns
    # the distance relative to the origin (0 means the origin, 1 means
    # the dest, the result can be negative)
    def distorig(self, p):
        v1  = p.sub(self.origin)
        nv1 = (v1.x**2. + v1.y**2.)**0.5
        v2  = self.dest.sub(self.origin)
        nv2 = (v2.x**2. + v2.y**2.)**0.5
        if (v1.x*v2.x + v1.y*v2.y < 0):
            return -nv1/nv2
        else:
            return nv1/nv2

    # Test if a point p belongs strictly to the edge
    def contains(self, p):
        if self.colinear(p):
            do = self.distorig(p)
            return (do > 0) and (do < 1)
        else:
            return False

    def attach_extremity(self, edge):
        self._touch.append(edge)
    def attach_middle(self, edge):
        self._attch.append(edge)

    def __repr__(self):
        return f"Edge(({self.xmin},{self.ymin})->({self.xmax},{self.ymax}))"


################################################################
class Hole(Edge):
    """A class that represents an edge only for holes.

    Typically, it represents a set of holes into which another edge
    can possibly attach itself.

    """
    def __init__(self, _min, _max, _type):
        super().__init__(_min, _max)
        self._type = _type

    @property
    def type(self): return self._type

    def __repr__(self):
        return f"Hole(({self.xmin},{self.ymin})->({self.xmax},{self.ymax}))"


################################################################
class SvgPrinter:
    """ A class that represents a svg printer object """
    def __init__(self, edges, filename, margin = 10,
                 color="black", stroke_width=0.01):
        self._edges = edges
        self._file = open(filename, "w")
        self._margin = margin
        self._color = color
        self._stroke_width = stroke_width

    def write(self, a_string):
        self._file.write(a_string + "\n")

    def set_color(self, a_color):
        self._color = a_color
    def set_stroke_width(self, a_length):
        self._stroke_width = a_length

    def print_header(self, bb):
        self.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        viewBox = f"{bb.xmin} " + \
            f"{bb.ymin} " + \
            f"{bb.width} " + \
            f"{bb.height}"
        self.write(f"<svg width='{bb.width}cm' " +
                   f"viewBox='{viewBox}' " +
                   f"height='{bb.height}cm' " +
                   f"xmlns='http://www.w3.org/2000/svg'>")

    def print_rectangle(self, min, max, color=None, stroke_width=None):
        col = self._color if color is None else color
        sw  = self._stroke_width if stroke_width is None else stroke_width
        min_x = min.x if min.x < max.x else max.x
        min_y = min.y if min.y < max.y else max.y
        width = abs(max.x - min.x)
        height = abs(max.y - min.y)
        # print("print rectangle", min, max, width, height)
        self.write(f"  <rect width='{width}' height='{height}' " +
                   f"x='{min_x}' y='{min_y}' " +
                   f"style='fill:none;stroke-width:{sw};stroke:{col}' " +
                   f"/>")

    def print_segment(self, min, max, color=None, stroke_width=None):
        col = self._color if color is None else color
        sw  = self._stroke_width if stroke_width is None else stroke_width
        self.write(f"<path d='M{min.x} {min.y} L{max.x} {max.y}' " +
                   f"style='stroke-width:{sw};stroke:{col}'/>")

    def start_group(self, id, label):
        self.write(f"<g>")
        # self.write(f"<g id='{id}' inkscape:label='{label} ' " + \
        #            f"inkscape:groupmode='layer'>")

    def end_group(self):
        self.write(f"</g>")

    def print_footer(self):
        self.write("</svg>")

    def dump_profile_to_svg(self):
        self.print_header(self._edges.bb)
        self.start_group(0, "Global rectangle")
        self.print_rectangle(self._edges.bb.lowerleft,
                             self._edges.bb.upperright)
        self.end_group()
        for an_edge in self._edges.edges:
            self.print_segment(an_edge.origin, an_edge.dest)
        self.close()

    def dump_plates_to_svg(self):
        plates = self._edges.plates
        self.print_header(plates.bb)
        self.start_group(0, "Global rectangle")
        self.print_rectangle(plates.bb.lowerleft, plates.bb.upperright,
                             color="red")
        self.end_group()
        for id_plate, a_plate in enumerate(plates):
            a_plate.dump_to_svg(self, f"layer{id_plate}")
        self.close()

    def close(self):
        self.print_footer()
        self._file.close()


################################################################
class PlateBorderStyle(Enum):
    NONE = auto()                    # No border is drawn
    STRAIGHT = auto()                # Border is straight
    CRENELATED_PROTRUDING = auto()   # Border starts |̅|_|...
    CRENELATED_CAVING_IN = auto()    # Border starts _|̅|_|...

    def __repr__(self):
        match self:
            case PlateBorderStyle.NONE:
                return "none"
            case PlateBorderStyle.STRAIGHT:
                return "straight"
            case PlateBorderStyle.CRENELATED_PROTRUDING:
                return "crenelated protruding"
            case PlateBorderStyle.CRENELATED_CAVING_IN:
                return "crenelated caving in"
            case _:
                return "unknown"


################################################################
class PlateBorderType:
    def __init__(self, style, start, end):
        self._style = style
        self._start_offset = start
        self._end_offset = end
        self._depth = None
    @property
    def style(self): return self._style
    @property
    def start_offset(self): return self._start_offset
    @property
    def end_offset(self): return self._end_offset
    @property
    def depth(self): return self._depth

    @staticmethod
    def none():
        return PlateBorderType(PlateBorderStyle.NONE, 0, 0)
    @staticmethod
    def straight(start=0, end=0):
        return PlateBorderType(PlateBorderStyle.STRAIGHT, start, end)
    @staticmethod
    def crenelated_protruding(start=0, end=0, depth=None):
        p = PlateBorderType(PlateBorderStyle.CRENELATED_PROTRUDING, start, end)
        if depth:
            p._depth = depth
        return p

    @staticmethod
    def crenelated_caving_in(start=0, end=0, depth=None):
        p = PlateBorderType(PlateBorderStyle.CRENELATED_CAVING_IN, start, end)
        if depth:
            p._depth = depth
        return p

    def __repr__(self):
        d_str = f",depth={self._depth}" if self._depth else ""
        return f"Style({PlateBorderStyle.__repr__(self._style)}," + \
            f"start={self._start_offset},end={self._end_offset}{d_str})"


################################################################
class PlateBorder:
    """Encodes the style of the border of a plate"""

    def __init__(self, type=PlateBorderType.straight(),
                 start=None, end=None, length=0, min_width=None,
                 upper=1, lower=1, depth=1):
        self._type  = type
        if start and end:
            length = end.sub(start).length()
        if start and end and min_width:
            num = int((length / min_width - 1) / 2 + 1)
            self._sides  = 2*num+1
            self._upper = length/self._sides
            self._lower = length/self._sides
        else:
            self._sides = int(length / (upper + lower)) + 1
            self._upper = upper
            self._lower = lower
        self._depth = depth

    @property
    def type(self):        return self._type
    @property
    def style(self):        return self._type.style
    @property
    def upper(self):        return self._upper
    @property
    def lower(self):        return self._lower
    @property
    def depth(self):
        return self._depth
    @property
    def start_offset(self): return self._type.start_offset
    @property
    def end_offset(self):   return self._type.end_offset
    @property
    def sides(self):        return self._sides

    def __repr__(self):
        return f"PlateBorder({self._type},depth={self.depth},sides={self.sides})"

################################################################
class Plate(BoundingBox):
    """A class representing a 2D-rectangular plate, in the 3D-world.

    Meaning it can represent all the "sides" of the box in the end.

    """
    def __init__(self, min, max, label=None, min_width=None, depth=None,
                 border_types=[], holes=[]):
        assert all( isinstance(b, PlateBorderType) for b in border_types ), \
            "Plate.__init__ : border_types are not PlateBorderType"
        upperright = P(max.x-min.x, max.y-min.y)
        super().__init__(P(0,0), upperright)
        self._label = label
        self._depth = depth
        self._min_width = min_width
        self._position = Point(0, 0)
        # Borders are arranged in order S E N W
        if border_types:
            vertices = [self.lowerleft, self.lowerright, self.upperright,
                        self.upperleft, self.lowerleft]
            bt = lambda i: border_types[i] if i < len(border_types) else PlateBorderType.STRAIGHT
            self._borders = list(map(lambda i: \
                                     PlateBorder(type=bt(i), start=vertices[i], end=vertices[i+1],
                                                 min_width=min_width, depth=depth),
                                     range(4)))
        else:
            self._borders = [ PlateBorder() ]*4
        self._holes = holes

    @property
    def label(self):     return self._label
    @property
    def depth(self):     return self._depth
    @property
    def min_width(self): return self._min_width

    def translate(self, a_point):
        super().translate(a_point)
        for i in range(len(self._holes)):
            self._holes[i].translate(a_point)

    def dump_to_svg(self, a_printer, an_id):
        # print("Dumping plate to svg", self.lowerleft, self.upperright)
        a_printer.start_group(an_id, f"Layer {self.label}")
        self.dump_segment_to_svg(a_printer, self.lowerleft,  self.lowerright, self._borders[0])
        self.dump_segment_to_svg(a_printer, self.lowerright, self.upperright, self._borders[1])
        self.dump_segment_to_svg(a_printer, self.upperright, self.upperleft,  self._borders[2])
        self.dump_segment_to_svg(a_printer, self.upperleft,  self.lowerleft,  self._borders[3])
        if len(self._holes) > 0:
            # print(self._holes)
            # ltor = self.lowerright.sub(self.lowerleft).unit()
            # dtou = self.upperleft.sub(self.lowerleft)
            for an_edge in self._holes:
                hole_start = an_edge.origin
                hole_end   = an_edge.dest
                border     = PlateBorder(type=an_edge.type,
                                         start=hole_start, end=hole_end, min_width=self.min_width, depth=self.depth)
                self.dump_holes_to_svg(a_printer, hole_start, hole_end, border)
        a_printer.end_group()

    def dump_crenelation_to_svg(self, a_printer, a_border, min, max, precision=0.01):
        assert a_border.style == PlateBorderStyle.CRENELATED_PROTRUDING or \
            a_border.style == PlateBorderStyle.CRENELATED_CAVING_IN, \
            "dump_to_svg: invalid crenelation"
        vector        = max.sub(min)
        direction     = vector.unit()
        perpendicular = direction.perp()
        length_done   = 0
        length_todo   = vector.length() - a_border.start_offset - a_border.end_offset
        if a_border.style == PlateBorderStyle.CRENELATED_PROTRUDING:
            position      = min.add(direction.mult(a_border.start_offset))
            is_upper      = True
        else:
            position      = min.add(direction.mult(a_border.start_offset)).\
                add(perpendicular.mult(a_border.depth))
            is_upper      = False
        for i in range(a_border.sides):
            if i == 0:
                next_length = a_border.upper - a_border.start_offset
            elif i == a_border.sides-1:
                next_length = a_border.upper - a_border.end_offset
            else:
                next_length = a_border.upper
            next_segment = direction.mult(next_length)
            next_position = position.add(next_segment)
            a_printer.print_segment(position, next_position)
            length_done += next_segment.length()
            if length_done >= (1-precision)*length_todo and \
               a_border.style == PlateBorderStyle.CRENELATED_CAVING_IN:
                break
            # HERE DEPTH
            here_depth = a_border.type.depth if a_border.type.depth else a_border.depth
            last_segment = perpendicular.mult(here_depth * (1 if is_upper else -1))
            last_position = next_position.add(last_segment)
            a_printer.print_segment(next_position, last_position)
            position = last_position
            is_upper = not(is_upper)

    def dump_segment_to_svg(self, a_printer, min, max, a_border, precision=0.01):
        a_printer.set_color("blue")
        match a_border.style:
            case PlateBorderStyle.NONE:
                pass
            case PlateBorderStyle.STRAIGHT:
                vector = max.sub(min)
                direction = vector.unit()
                a_printer.print_segment(min.add(direction.mult(a_border.start_offset)),
                                        max.sub(direction.mult(a_border.end_offset)))
            case PlateBorderStyle.CRENELATED_PROTRUDING:
                self.dump_crenelation_to_svg(a_printer, a_border, min, max, precision=precision)
            case PlateBorderStyle.CRENELATED_CAVING_IN:
                self.dump_crenelation_to_svg(a_printer, a_border, min, max, precision=precision)
            case _:
                assert False, f"dump_segment_to_svg: unknown type {type}"

    def dump_holes_to_svg(self, a_printer, min, max, a_border):
        """ Print the rectangles corresponding to holes inside a plate
            min and max correspond to the extremities of the edge
        """
        vector = max.sub(min)
        direction = vector.unit()
        perpendicular = direction.perp()
        position      = min
        is_upper      = False # Do we print the hole ?
        length_done   = 0
        # print(direction, perpendicular, position, a_border.upper)
        # length_todo   = vector.length() - a_border.start_offset - a_border.end_offset
        for i in range(a_border.sides):
            next_length = a_border.upper
            next_segment = direction.mult(next_length)
            next_position = position.add(next_segment)
            if (is_upper):
                # print("C1", position.add(perpendicular.mult(a_border.depth/2)))
                # print("C2", next_position.add(perpendicular.mult(-a_border.depth/2)))
                a_printer.print_rectangle(position.add(perpendicular.mult(a_border.depth/2)),
                                          next_position.add(perpendicular.mult(-a_border.depth/2)))
            length_done += next_segment.length()
            position = next_position
            is_upper = not(is_upper)

    def __repr__(self):
        if self._label:
            return f"{self._label}(({self.xmin},{self.ymin})->({self.xmax},{self.ymax}))"
        else:
            return f"Plate(({self.xmin},{self.ymin})->({self.xmax},{self.ymax}))"

################################################################
class Plates:
    """ A class handling a list of 2D-plates """
    def __init__(self, margin=1):
        self._plates = []
        self._bb = BoundingBox(P(0,0),P(0,0))
        self._margin = margin

    @property
    def bb(self):     return self._bb
    @property
    def margin(self): return self._margin

    def is_empty(self):
        return len(self._plates) <= 1

    def append(self, a_plate):
        """Appends a plate to a list of existing plates. Should
        probably try to pack the plates if possible.
        """
        a_plate.translate_to_origin()
        a_plate.translate(self._bb.lowerright)
        if self._bb.xmax > 0: # Add small margin between plates
            a_plate.translate(P(self.margin, 0))
        self._bb.union(a_plate)
        self._plates.append(a_plate)

    def __iter__(self):
        for a_plate in self._plates:
            yield a_plate


################################################################
class Edges:
    """ A class that represents a 2D-box with subdivisions.

    depth:     the thickness of the wooden plate used
    min_width: the minimal width for the crenelations
               min_width should be >= depth
    height:    the height of the box

    """

    def __init__(self, min, max, height=10, depth=0.5, min_width=None,
                 bottom=True):
        self._bb    = BoundingBox(min, max)
        self._edges = [
            Edge(P(self.bb.xmin, self.bb.ymin), P(self.bb.xmax, self.bb.ymin)),
            Edge(P(self.bb.xmax, self.bb.ymin), P(self.bb.xmax, self.bb.ymax)),
            Edge(P(self.bb.xmax, self.bb.ymax), P(self.bb.xmin, self.bb.ymax)),
            Edge(P(self.bb.xmin, self.bb.ymax), P(self.bb.xmin, self.bb.ymin)),
        ]
        self._height = height
        self._depth  = depth
        self._min_width = min_width if min_width else 2*depth
        self._bottom = bottom
        self._plates = Plates()

    @property
    def bb(self):           return self._bb
    @property
    def bounding_box(self): return self._bb
    @property
    def edges(self):        return self._edges
    @property
    def height(self):       return self._height
    @property
    def depth(self):        return self._depth
    @property
    def min_width(self):    return self._min_width
    @property
    def plates(self):
        assert not(self._plates.is_empty()), "Edges : plates not computed"
        return self._plates

    # Add an edge to the subdivision
    # The edge is supposed to be attached to two existing edges
    def add_edge(self, edge):
        for an_edge in self._edges:
            if an_edge.contains(edge.origin):
                edge.attach_extremity(an_edge)
                an_edge.attach_middle(edge)
            if an_edge.contains(edge.dest):
                edge.attach_extremity(an_edge)
                an_edge.attach_middle(edge)
        self._edges.append(edge)

    def debug_edges(self):
        print("[")
        for an_edge in self.edges:
            print("  ", an_edge, end="")
            if an_edge._touch:
                print(f" touches {an_edge._touch}", end="")
            if an_edge._attch:
                print(f" is attached to {an_edge._attch}", end="")
            print("")
        print("]")

    def debug_plates(self):
        print("[")
        for a_plate in self.plates:
            print("  ", a_plate, end="")
            print("")
        print("]")

    def is_attached_to_border(self, a_point):
        return any(a_border.contains(a_point) for a_border in self._edges[:4])

    def is_attached_to_inside_edge(self, a_point):
        return any(an_edge.contains(a_point) for an_edge in self._edges[4:])

    def is_meeting_multiple_edges(self, a_point):
        def edges_meeting_at(a_point):
            return [ an_edge for an_edge in self._edges[4:] if (an_edge.origin == a_point) or (an_edge.dest == a_point) ]
        # print(a_point, edges_meeting_at(a_point))
        return len(edges_meeting_at(a_point)) > 1

    def compute_plates(self):
        # Add the global bottom plate
        if self._bottom:
            holes = [ ]
            for id_edge, an_edge in enumerate(self.edges):
                if id_edge >= 4: # Not the global border
                    vector = an_edge.dest.sub(an_edge.origin).unit()
                    if not(self.is_attached_to_border(an_edge.origin)):
                        hole_start = an_edge.origin.add(vector.mult(-self.depth/2))
                    else:
                        hole_start = an_edge.origin
                    if not(self.is_attached_to_border(an_edge.dest)):
                        hole_end = an_edge.dest.add(vector.mult(self.depth/2))
                    else:
                        hole_end = an_edge.dest
                    holes.append(Hole(hole_start, hole_end, PlateBorderType.straight()))
            # print("holes", holes)
            self._plates.append(Plate(self.bb.lowerleft, self.bb.upperright,
                                      label="Bottom Plate", depth=self.depth, min_width=self.min_width,
                                      border_types=[ PlateBorderType.crenelated_protruding() ] * 4,
                                      holes=holes))
        # Add the border plates and inner plates
        labels = {
            0: "South Plate",
            1: "Right Plate",
            2: "North Plate",
            3: "Left Plate",
        }
        for id_edge, an_edge in enumerate(self.edges):
            # Compute concrete edge length (taking into account attachments)
            length = an_edge.length
            # print(an_edge,
            #       "ATTACHED MIN?:", self.is_attached_to_inside_edge(an_edge.min),
            #       "MAX?:", self.is_attached_to_inside_edge(an_edge.max),
            #       "MULTIPLE MIN?:", self.is_meeting_multiple_edges(an_edge.min),
            #       "MAX?:", self.is_meeting_multiple_edges(an_edge.max))
            if self.is_attached_to_inside_edge(an_edge.min):
                length += self.depth / 2
            if self.is_attached_to_inside_edge(an_edge.max):
                length += self.depth / 2

            label = labels[id_edge] if id_edge in labels else "Inner Plate"
            if label != "Inner Plate": # The border plates
                bottom_edge = PlateBorderType.crenelated_caving_in(start=self.depth) \
                    if self._bottom else PlateBorderType.straight(start=self.depth)
                right_edge  = PlateBorderType.crenelated_protruding(start=self.depth) \
                    if self._bottom else PlateBorderType.crenelated_protruding()
                left_edge   = PlateBorderType.crenelated_caving_in(end=self.depth) \
                    if self._bottom else PlateBorderType.crenelated_caving_in()
                top_edge    = PlateBorderType.straight(end=self.depth)
                bts = [
                    bottom_edge, right_edge, top_edge, left_edge,
                ]
            else: # The inner plates
                if self.is_meeting_multiple_edges(an_edge.max):
                    right_depth = self.depth / 2
                else:
                    right_depth = self.depth
                if self.is_meeting_multiple_edges(an_edge.min):
                    left_depth = self.depth / 2
                else:
                    left_depth = self.depth
                bottom_edge = PlateBorderType.crenelated_caving_in(start=self.depth, end=self.depth) \
                    if self._bottom else PlateBorderType.straight(start=self.depth, end=self.depth)
                right_edge  = PlateBorderType.crenelated_caving_in(start=self.depth, depth=right_depth) \
                    if self._bottom else PlateBorderType.crenelated_caving_in(start=0, depth=right_depth)
                top_edge    = PlateBorderType.straight(start=self.depth, end=self.depth)
                left_edge   = PlateBorderType.crenelated_caving_in(end=self.depth, depth=left_depth) \
                    if self._bottom else PlateBorderType.crenelated_caving_in(end=0, depth=left_depth)
                bts = [
                    bottom_edge, right_edge, top_edge, left_edge,
                ]

            # Compute the holes
            holes = [ Hole(P(a_length,0), P(a_length,self.height),
                           PlateBorderType.straight())
                      for a_length in an_edge.attached_lengths ]
            self._plates.append(Plate(P(0, 0), P(length, self.height),
                                      label=label, depth=self.depth,
                                      min_width=self.min_width,
                                      border_types=bts, holes=holes))

    def dump_profile_to_svg(self, filename):
        SvgPrinter(self, filename).dump_profile_to_svg()
    def dump_plates_to_svg(self, filename):
        assert not(self.plates.is_empty()), "Edges : plates not computed"
        SvgPrinter(self, filename).dump_plates_to_svg()

    def boxify(self):
        pass


################################################################
if __name__ == '__main__':
    test_cases = []
    ########################################################
    # Test cases

    # # Only a rectangle
    # tc1 = Edges(P(0,0), P(10,10), height=3, bottom=False)
    # test_cases.append(tc1)

    # # Rectangle with horizontal inner separation
    # tc2 = Edges(P(0,0), P(10,10), height=3, bottom=False)
    # tc2.add_edge(Edge(P(0,5),P(10,5)))
    # test_cases.append(tc2)

    # # Rectangle with vertical inner separation
    # tc3 = Edges(P(0,0), P(10,10), height=3, bottom=False)
    # tc3.add_edge(Edge(P(5,0),P(5,10)))
    # test_cases.append(tc3)

    # # Rectangle with vertical inner separation, not in the middle
    # tc4 = Edges(P(0,0), P(10,10), height=3, min_width=2.5, bottom=False)
    # tc4.add_edge(Edge(P(6.5,0),P(6.5,10)))
    # test_cases.append(tc4)

    # # Rectangle with three separations not meeting
    # tc5 = Edges(P(0,0), P(10,10), height=3, min_width=2.5, bottom=False)
    # tc5.add_edge(Edge(P(5,0),P(5,10)))
    # tc5.add_edge(Edge(P(5,7),P(10,7)))
    # tc5.add_edge(Edge(P(0,3),P(5,3)))
    # test_cases.append(tc5)

    # # Rectangle with three separations meeting at the same height
    # tc6 = Edges(P(0,0), P(10,10), height=3, min_width=1, bottom=False)
    # tc6.add_edge(Edge(P(4,0),P(4,10)))
    # tc6.add_edge(Edge(P(4,2),P(10,2)))
    # tc6.add_edge(Edge(P(0,2),P(4,2)))
    # test_cases.append(tc6)

    # # Rectangle with three separations meeting at the same width
    # tc7 = Edges(P(0,0), P(10,10), height=3, min_width=1, bottom=False)
    # tc7.add_edge(Edge(P(0,4),P(10,4)))
    # tc7.add_edge(Edge(P(7,0),P(7,4)))
    # tc7.add_edge(Edge(P(7,10),P(7,4)))
    # test_cases.append(tc7)

    # Rectangle with five separations meeting at the same height
    tc8 = Edges(P(0,0), P(10,10), height=3, min_width=1, bottom=False)
    tc8.add_edge(Edge(P(4,0),P(4,10)))
    tc8.add_edge(Edge(P(6.5,0),P(6.5,10)))
    tc8.add_edge(Edge(P(6.5,2),P(10,2)))
    tc8.add_edge(Edge(P(4,2),P(6.5,2)))
    tc8.add_edge(Edge(P(0,2),P(4,2)))
    test_cases.append(tc8)

    ########################################################
    # Tests
    for tc in test_cases:
        bb = tc.bounding_box
        assert bb.xmin == 0 and bb.xmax == 10
        assert bb.ymin == 0 and bb.ymax == 10
        tc.debug_edges()
        tc.compute_plates()
        tc.debug_plates()
        tc.dump_profile_to_svg("profile.svg")
        tc.dump_plates_to_svg("plates.svg")

################################################################
# Test usage :
# clear && ./lc2.py && cat file.svg && inkview file.svg &> /dev/null
# clear && ./lc2.py && cat profile.svg && inkview -s 0.5 plates.svg &> /dev/null
