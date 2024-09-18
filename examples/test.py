from manim import *
from manim_hkn.cElements import Resistor

class test(Scene):
	def construct(self):

		self.camera.background_color = BLACK

		r = Resistor()
		self.add(r)

		self.play(r.animate.scale(2))
		self.play(r.animate.set_color(GREEN))


		self.wait(1)



		self.play(r.animate.shift(RIGHT))

		# # r.remove()

		self.wait()