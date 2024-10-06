from manim import *

class BJT_NPN(VMobject):
	ARROW_DIST_RATIO = 0.8
	def __init__(self, stroke_size=15, color=WHITE, **kwargs):
		
		VMobject.__init__(self, stroke_width=stroke_size, color=color, joint_type = LineJointType.ROUND, cap_style = CapStyleType.ROUND)

		self._circle = Circle(radius = stroke_size / 8., color = self.color, stroke_width = self.stroke_width)

		corners = [	[3, -1, 0], [1.3, -1, 0], [0.8, 0.8, 0], 
					[1.2, 0.8, 0], [0, 0.8, 0], [0, 2.3, 0], [0, 0.8, 0], [-1.2, 0.8, 0],
					[-0.8, 0.8, 0], [-1.3, -1, 0], [-3, -1, 0]]
		self.set_points_as_corners(corners)

		self._arrow = Line(start = [-0.8, 0.8, 0], end = [(-1.3 - -0.8) * BJT_NPN.ARROW_DIST_RATIO + -0.8, (-1 - 0.8) * BJT_NPN.ARROW_DIST_RATIO + 0.8, 0], buff = 0, stroke_width = stroke_size, color=color)
		self._arrow.add_tip(tip_shape=ArrowTriangleFilledTip, tip_width = stroke_size / 100. * 4, tip_length = stroke_size / 100. * 4)

		self._left_terminal = Dot(radius=stroke_size/200., color=self.color).set_x(-3).set_y(-1)
		self._right_terminal = Dot(radius=stroke_size/200., color=self.color).set_x(3).set_y(-1)
		self._gate_terminal = Dot(radius=stroke_size/200., color=self.color).set_y(2.3)

		def stroke_update(capacitor): 
			capacitor.set_stroke_width(100*capacitor._left_terminal.width)
			capacitor._arrow.set_stroke_width(100*capacitor._left_terminal.width)
			capacitor._circle.set_stroke_width(100*capacitor._left_terminal.width)

		self.add_updater(stroke_update)
		
		self.add(self._arrow, self._circle, self._left_terminal, self._right_terminal, self._gate_terminal)

	def get_left_terminal_coordinates(self):
		return self._left_terminal.get_center()
	def get_right_terminal_coordinates(self):
		return self._right_terminal.get_center()
	def get_gate_terminal_coordinates(self):
		return self._gate_terminal.get_center()

class Capacitor(VMobject):
	HEIGHT_RATIO = 1.5
	def __init__(self, stroke_size=15, color=WHITE, **kwargs):
		VMobject.__init__(self, stroke_width=stroke_size, color=color)

		cornersLeft  = [[-1.5, 0, 0], [-0.5, 0, 0], [-0.5, Capacitor.HEIGHT_RATIO, 0], [-0.5, -Capacitor.HEIGHT_RATIO, 0]]
		cornersRight = [[ 1.5, 0, 0], [ 0.5, 0, 0], [ 0.5, Capacitor.HEIGHT_RATIO, 0], [ 0.5, -Capacitor.HEIGHT_RATIO, 0]]
		
		self._left  = VMobject(stroke_width=stroke_size, color=color, joint_type = LineJointType.ROUND, cap_style = CapStyleType.ROUND)
		self._right = VMobject(stroke_width=stroke_size, color=color, joint_type = LineJointType.ROUND, cap_style = CapStyleType.ROUND)
		self._left.set_points_as_corners(cornersLeft)
		self._right.set_points_as_corners(cornersRight)

		self._left_terminal = Dot(radius=stroke_size/200., color=self.color).set_x(-1.5)
		self._right_terminal = Dot(radius=stroke_size/200., color=self.color).set_x(1.5)

		def stroke_update(capacitor): 
			capacitor.set_stroke_width(100*capacitor._left_terminal.width)
			capacitor._left.set_stroke_width(100*capacitor._left_terminal.width)
			capacitor._right.set_stroke_width(100*capacitor._left_terminal.width)

		self.add_updater(stroke_update)
		
		self.add(self._left, self._right, self._left_terminal, self._right_terminal)

	def get_left_terminal_coordinates(self):
		return self._left_terminal.get_center()
	def get_right_terminal_coordinates(self):
		return self._right_terminal.get_center()


class Resistor(VMobject):
	SPREAD_RATIO = 1.25
	def __init__(self, stroke_size=15, color=WHITE, **kwargs):
		VMobject.__init__(self, stroke_width=stroke_size, color=color, joint_type = LineJointType.ROUND, cap_style = CapStyleType.ROUND)

		corners = [[Resistor.SPREAD_RATIO*(-2),  0, 0]]
		for i in range(-1, 1+1, 1):
			corners.extend([[Resistor.SPREAD_RATIO*(i-0.5),  0, 0],
				   			[Resistor.SPREAD_RATIO*(i-0.25),  1, 0],
							[Resistor.SPREAD_RATIO*(i+0.25), -1, 0],
							[Resistor.SPREAD_RATIO*(i+0.5),  0, 0]])
		corners.append([Resistor.SPREAD_RATIO*(2),  0, 0])
		
		self.set_points_as_corners(corners)

		self._left_terminal = Dot(radius=stroke_size/200., color=self.color).set_x(Resistor.SPREAD_RATIO*(-2))
		self._right_terminal = Dot(radius=stroke_size/200., color=self.color).set_x(Resistor.SPREAD_RATIO*(2))

		self.add_updater(lambda resistor: 
				   resistor.set_stroke_width(100*resistor._left_terminal.width))
		
		self.add(self._left_terminal, self._right_terminal)
	
	def get_left_terminal_coordinates(self):
		return self._left_terminal.get_center()
	def get_right_terminal_coordinates(self):
		return self._right_terminal.get_center()
