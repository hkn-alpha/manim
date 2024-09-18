from manim import *

class Resistor(VGroup):
	def __init__(self, resistance='1Ω', stroke_size=15, color=WHITE, **kwargs):
		self.resistance = resistance

		RESISTOR_RATIO = 1

		RESISTOR_VERTICES = (Dot(radius=stroke_size/200.0).set_x(-2),
					   		 Dot(radius=stroke_size/200.0).set_x(-1.5),
					   		 Dot(radius=stroke_size/200.0).set_x(1.5),
					   		 Dot(radius=stroke_size/200.0).set_x(2),)
		RESISTOR_POLYGRAM_SHAPE = (Line(start=[-1.5, 0, 0], end=[-2, 0, 0]).set_stroke(width=stroke_size).add_updater(lambda mobject: mobject.set_stroke_width(100*RESISTOR_VERTICES[0].width)),
								   Line(start=[ 1.5, 0, 0], end=[ 2, 0 ,0]).set_stroke(width=stroke_size).add_updater(lambda mobject: mobject.set_stroke_width(100*RESISTOR_VERTICES[0].width)))
		for i in range(-1, 1+1, 1):
			RESISTOR_VERTICES += (Dot(point=[RESISTOR_RATIO*(i-0.25),   1, 0], radius=stroke_size/200.0),
						 		  Dot(point=[RESISTOR_RATIO*(i+0.25),  -1, 0], radius=stroke_size/200.0), )
			RESISTOR_POLYGRAM_SHAPE += (Line(start=[RESISTOR_RATIO*(i-0.5),  0, 0], end=[RESISTOR_RATIO*(i-0.25),  1, 0]).set_stroke(width=stroke_size).add_updater(lambda mobject: mobject.set_stroke_width(100*RESISTOR_VERTICES[0].width)),
										Line(start=[RESISTOR_RATIO*(i-0.25), 1, 0], end=[RESISTOR_RATIO*(i+0.25), -1, 0]).set_stroke(width=stroke_size).add_updater(lambda mobject: mobject.set_stroke_width(100*RESISTOR_VERTICES[0].width)),
										Line(start=[RESISTOR_RATIO*(i+0.5),  0, 0], end=[RESISTOR_RATIO*(i+0.25), -1, 0]).set_stroke(width=stroke_size).add_updater(lambda mobject: mobject.set_stroke_width(100*RESISTOR_VERTICES[0].width)),)

		l=Group(*RESISTOR_VERTICES, *RESISTOR_POLYGRAM_SHAPE)

		VGroup.__init__(self, *RESISTOR_VERTICES, *RESISTOR_POLYGRAM_SHAPE)
		
