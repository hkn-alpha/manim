from manim import *
from manim_hkn.utils import *
from manim_hkn import *

class test(Scene):
	def construct(self):
		L = Text('L', font_size = 100).shift(UP)
		R = Text('R', font_size = 100).next_to(L, LEFT)
		C = Text('C', font_size = 100).next_to(L, RIGHT)

		self.play(FadeIn(R, L, C))

		r = Resistor().scale(0.5).shift(DOWN + LEFT*3)
		l = Resistor().scale(0.5).shift(DOWN)
		c = Capacitor().scale(0.5).shift(DOWN + RIGHT*3)

		self.wait(0.5)
		self.play(Transform(R, r))
		self.wait(0.5)
		self.play(Transform(L, l))
		self.wait(0.5)
		self.play(Transform(C, c))
