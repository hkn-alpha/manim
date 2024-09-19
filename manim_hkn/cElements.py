from manim import *

class Capacitor(VMobject):
	HEIGHT_RATIO = 1.5
	def __init__(self, resistance='1Ω', stroke_size=15, color=WHITE, **kwargs):

		self.resistance = resistance

		cornersLeft  = [[-1.5, 0, 0], [-0.5, 0, 0], [-0.5, Capacitor.HEIGHT_RATIO, 0], [-0.5, -Capacitor.HEIGHT_RATIO, 0]]
		cornersRight = [[ 0.5, -Capacitor.HEIGHT_RATIO, 0], [ 0.5, Capacitor.HEIGHT_RATIO, 0], [ 0.5, 0, 0], [ 1.5, 0, 0]]
		
		VMobject.__init__(self, stroke_width=stroke_size, color=color)
		
		self.left = VMobject(stroke_width=stroke_size, color=color)
		self.right = VMobject(stroke_width=stroke_size, color=color)
		self.left.set_points_as_corners(cornersLeft)
		self.right.set_points_as_corners(cornersRight)
		self.add(self.left, self.right)
		self.joint_type=LineJointType.ROUND
		self.cap_style=CapStyleType.ROUND

		self.left_terminal = Dot(radius=stroke_size/200., color=self.color).set_x(-1.5)
		self.right_terminal = Dot(radius=stroke_size/200., color=self.color).set_x(1.5)

		def stroke_update(capacitor): 
			capacitor.set_stroke_width(100*capacitor.left_terminal.width)
			capacitor.left.set_stroke_width(100*capacitor.left_terminal.width)
			capacitor.right.set_stroke_width(100*capacitor.left_terminal.width)

		self.add_updater(stroke_update)
		self.add_updater(lambda capacitor: capacitor.left.next_to(capacitor.left_terminal, RIGHT, buff = -capacitor.left_terminal.width/2))
		
		self.add(self.left_terminal)
		self.add(self.right_terminal)


class Resistor(VMobject):
	SPREAD_RATIO = 1.25
	def __init__(self, resistance='1Ω', stroke_size=15, color=WHITE, **kwargs):
		self.resistance = resistance

		corners = [[Resistor.SPREAD_RATIO*(-2),  0, 0]]
		for i in range(-1, 1+1, 1):
			corners.extend([[Resistor.SPREAD_RATIO*(i-0.5),  0, 0],
				   			[Resistor.SPREAD_RATIO*(i-0.25),  1, 0],
							[Resistor.SPREAD_RATIO*(i+0.25), -1, 0],
							[Resistor.SPREAD_RATIO*(i+0.5),  0, 0]])
		corners.append([Resistor.SPREAD_RATIO*(2),  0, 0])
		
		VMobject.__init__(self, stroke_width=stroke_size, color=color)
		self.set_points_as_corners(corners)
		self.joint_type=LineJointType.ROUND
		self.cap_style=CapStyleType.ROUND

		self.left_terminal = Dot(radius=stroke_size/200., color=self.color).set_x(Resistor.SPREAD_RATIO*(-2))
		self.right_terminal = Dot(radius=stroke_size/200., color=self.color).set_x(Resistor.SPREAD_RATIO*(2))

		self.add_updater(lambda resistor: 
				   resistor.set_stroke_width(100*resistor.left_terminal.width))
		
		self.add(self.left_terminal)
		self.add(self.right_terminal)
