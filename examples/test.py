from manim import *
from manim_hkn.utils import *
from manim_hkn import *

class test(Scene):
	def construct(self):
		L = Text('L', font_size = 100).shift(UP)
		R = Text('R', font_size = 100).next_to(L, LEFT)
		C = Text('C', font_size = 100).next_to(L, RIGHT)

		self.play(FadeIn(R, L, C))

		r = Resistor().scale(0.4, about_point=ORIGIN).shift(LEFT*3).rotate(-PI/2).update()
		l = Inductor().scale(0.4, about_point=ORIGIN).shift(DOWN * 1.5).update()
		c = Capacitor().scale(0.4, about_point=ORIGIN).shift(RIGHT*3).rotate(PI/2).update()

		self.wait(0.4)
		self.play(Transform(R, r))
		self.wait(0.4)
		self.play(Transform(L, l))
		self.wait(0.4)
		self.play(Transform(C, c))

		b = FunctionGenerator().scale(0.4, about_point=ORIGIN).shift(UP*1.5).update()
		hw1,vw1 = connect_with_square_wire(c, 'right', b, 'right')
		hw2,vw2 = connect_with_square_wire(c, 'left', l, 'right')
		hw3,vw3 = connect_with_square_wire(r, 'left', b, 'left')
		hw4,vw4 = connect_with_square_wire(r, 'right', l, 'left')

		wires = [hw1, vw1, hw2, vw2, hw3, vw3, hw4, vw4]
		for wire in wires:
			wire.scale(0.4)
		
		elems = [r, l, c, *wires]

		self.play(Create(b))
		self.play(FadeIn(*elems))

		vin = Text("V(t)", font_size = 75).next_to(b, UP)
		R = Text("R", font_size = 75).next_to(r, LEFT)
		L = Text("L", font_size = 75).next_to(l, DOWN)
		C = Text("C", font_size = 75).next_to(c, RIGHT)
		self.play(Write(vin), Write(R), Write(L), Write(C))
