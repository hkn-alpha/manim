from manim import *
from manim_hkn.cElements import Resistor, Capacitor, BJT_NPN

class test(Scene):
	def construct(self):
		r = Resistor()
		c = Capacitor()
		bjt_npn = BJT_NPN(color = GREEN)

		self.wait(0.1)

		self.play(Create(bjt_npn, run_time=2))
		self.play(bjt_npn.animate.
			scale(0.6).
			shift(2.5 * DOWN + LEFT))

		self.play(Create(r))
		self.play(r.animate.
			scale(0.6).
			shift(3 * LEFT + 2 * UP))

		self.play(Create(c))
		self.play(c.animate.
			scale(0.6).
			rotate(-PI/4))
		self.play(c.animate.
			connect_terminals('left', r, 'right'))

		self.play(bjt_npn.animate.
			set_color(WHITE).
			connect_terminals('gate', c, 'right'))

		g = Group(r, c, bjt_npn)

		self.play(g.animate.shift(DOWN + RIGHT))

		self.wait()
