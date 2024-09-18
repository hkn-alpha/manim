from manim import *
from manim_hkn.resistor import Resistor

class test(Scene):
	def construct(self):

		self.camera.background_color = BLACK

		r = Resistor(self, 10)
		r.add()

		self.wait(12)

		r.remove()

		self.wait()