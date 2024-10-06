from manim import *
from enum import Enum

class CircuitElementTemplate(VMobject):
	def __init__(self, components: List[VMobject], terminalCoords: List[List[float]], stroke_width = 15, **kwargs):
		self._terminal_scale_factor = 0.5
		VMobject.__init__(self, stroke_width=stroke_width, joint_type = LineJointType.ROUND, cap_style = CapStyleType.ROUND, **kwargs)

		self._terminals = [Dot(radius=self._terminal_scale_factor * stroke_width/200., color=self.color).shift(coord) for coord in terminalCoords]
		self._components = components

		self.add(*self._components, *self._terminals).set_color(self.color)

		def updater(cElem: CircuitElementTemplate):
			cElem.set_stroke_width(100*cElem._terminals[0].width / self._terminal_scale_factor)
			for i in range(len(self._components)):
				cElem._components[i].set_stroke_width(100*cElem._terminals[0].width / self._terminal_scale_factor)
		self.add_updater(updater)

	def get_terminal_coord(self, terminal_index: Enum):
		return self._terminals[terminal_index.value].get_center()
	def connect_terminals(self, source_terminal: Enum, dest: "CircuitElementTemplate", dest_terminal: Enum):
		return self.shift(dest.get_terminal_coord(dest_terminal) - self.get_terminal_coord(source_terminal))
	
class BJT_NPN(CircuitElementTemplate):
	ARROW_DIST_RATIO = 0.8
	
	class Terminals(Enum):
		LEFT 	= 0
		RIGHT 	= 1
		GATE 	= 2

	def __init__(self, stroke_width=15, **kwargs):
		circle = Circle(radius = stroke_width / 8., stroke_width = stroke_width)

		corners = [	[3, -1, 0], [1.3, -1, 0], [0.8, 0.8, 0], 
					[1.2, 0.8, 0], [0, 0.8, 0], [0, 2.3, 0], [0, 0.8, 0], [-1.2, 0.8, 0],
					[-0.8, 0.8, 0], [-1.3, -1, 0], [-3, -1, 0]]
		component = VMobject(stroke_width=stroke_width, joint_type = LineJointType.ROUND, cap_style = CapStyleType.ROUND).set_points_as_corners(corners)
		arrow = Line(start = [-0.8, 0.8, 0], end = [(-1.3 - -0.8) * BJT_NPN.ARROW_DIST_RATIO + -0.8, (-1 - 0.8) * BJT_NPN.ARROW_DIST_RATIO + 0.8, 0], buff = 0, stroke_width = stroke_width)
		arrow.add_tip(tip_shape=ArrowTriangleFilledTip, tip_width = stroke_width / 100. * 4, tip_length = stroke_width / 100. * 4)

		CircuitElementTemplate.__init__(self, 
								  components=[circle, component, arrow], 
								  terminalCoords=[	[-3, -1, 0],
						  							[3, -1, 0],
						  							[0, 2.3, 0]],
													**kwargs)

class Capacitor(CircuitElementTemplate):
	HEIGHT_RATIO = 1.5
	
	class Terminals(Enum):
		LEFT 	= 0
		RIGHT 	= 1

	def __init__(self, stroke_width=15, color=WHITE, **kwargs):

		cornersLeft  = [[-1.5, 0, 0], [-0.5, 0, 0], [-0.5, Capacitor.HEIGHT_RATIO, 0], [-0.5, -Capacitor.HEIGHT_RATIO, 0]]
		cornersRight = [[ 1.5, 0, 0], [ 0.5, 0, 0], [ 0.5, Capacitor.HEIGHT_RATIO, 0], [ 0.5, -Capacitor.HEIGHT_RATIO, 0]]
		
		left  = VMobject(stroke_width=stroke_width, color=color, joint_type = LineJointType.ROUND, cap_style = CapStyleType.ROUND).set_points_as_corners(cornersLeft)
		right = VMobject(stroke_width=stroke_width, color=color, joint_type = LineJointType.ROUND, cap_style = CapStyleType.ROUND).set_points_as_corners(cornersRight)
		
		CircuitElementTemplate.__init__(self, 
								  components=[left, right], 
								  terminalCoords=[	[-1.5, 0, 0],
						  							[1.5, 0, 0]],
													**kwargs)

class Resistor(CircuitElementTemplate):
	SPREAD_RATIO = 1.25
	
	class Terminals(Enum):
		LEFT 	= 0
		RIGHT 	= 1

	def __init__(self, stroke_width=15, color=WHITE, **kwargs):
		corners = [[Resistor.SPREAD_RATIO*(-2),  0, 0]]
		for i in range(-1, 1+1, 1):
			corners.extend([[Resistor.SPREAD_RATIO*(i-0.5),  0, 0],
				   			[Resistor.SPREAD_RATIO*(i-0.25),  1, 0],
							[Resistor.SPREAD_RATIO*(i+0.25), -1, 0],
							[Resistor.SPREAD_RATIO*(i+0.5),  0, 0]])
		corners.append([Resistor.SPREAD_RATIO*(2),  0, 0])
		
		component = VMobject(stroke_width=stroke_width, color=color, joint_type = LineJointType.ROUND, cap_style = CapStyleType.ROUND).set_points_as_corners(corners)

		CircuitElementTemplate.__init__(self, 
								  components=[component], 
								  terminalCoords=[	[Resistor.SPREAD_RATIO * -2, 0, 0],
						  							[Resistor.SPREAD_RATIO * 2, 0, 0]],
													**kwargs)