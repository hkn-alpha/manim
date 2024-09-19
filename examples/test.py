from manim import *
from manim_hkn.cElements import Resistor, Capacitor
from manim_hkn.circuit import Circuit

class test(Scene):
	def construct(self):

		self.camera.background_color = BLACK

		r = Resistor()
		c = Capacitor()

		self.wait(0.2)

		self.play(Create(r))
		self.play(r.animate.scale(0.6))
		self.play(r.animate.shift(0.6*LEFT*Resistor.SPREAD_RATIO*2+UP))

		self.wait()

		self.play(Create(c))
		self.play(c.animate.scale(0.6))
		self.play(c.animate.shift(0.6*1.5*RIGHT+UP))

		self.wait()
