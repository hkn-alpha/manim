from manim import *
from manim_hkn.cElements import Resistor, Capacitor, BJT_NPN
from manim_hkn.circuit import Circuit
from manim_hkn.util import get_terminal_connect_animation

class test(Scene):
	def construct(self):

		self.camera.background_color = BLACK

		r = Resistor()
		c = Capacitor()
		bjt_npn = BJT_NPN()

		self.wait(0.1)

		self.play(Create(bjt_npn))

		self.play(bjt_npn.animate.scale(0.6).shift(3 * DOWN + LEFT))

		self.play(Create(r))
		self.play(r.animate.scale(0.6))
		self.play(r.animate.shift(3 * LEFT + 2 * UP))

		self.wait()

		self.play(Create(c))
		self.play(c.animate.scale(0.6).rotate(-PI/2))

		a = get_terminal_connect_animation(c, c.get_left_terminal_coordinates(), r.get_right_terminal_coordinates())
		self.play(a)

		a = get_terminal_connect_animation(bjt_npn, bjt_npn.get_gate_terminal_coordinates(), c.get_right_terminal_coordinates())
		self.play(a)

		self.wait()
