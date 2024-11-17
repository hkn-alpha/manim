from manim import *
from manim_hkn.utils import *
from manim_hkn import *

class test(Scene):
	def construct(self):

		hkn_emblem = ImageMobject("manim_hkn/assets/img/hkn_alpha_emblem.png")
		self.play(FadeIn(hkn_emblem))
		self.wait(0.75)
		self.play(hkn_emblem.animate.scale(0.3).to_corner(UR), run_time = 1.5)

		RLC = Text('RLC', font_size = 100).shift(UP)
		self.play(FadeIn(RLC))

		r = Resistor().scale(0.4, about_point=ORIGIN).shift(LEFT*1.5).rotate(-PI/2).update()
		l = Inductor().scale(0.4, about_point=ORIGIN).shift(DOWN * 2).update()
		c = Capacitor().scale(0.4, about_point=ORIGIN).shift(RIGHT*1.5).rotate(PI/2).update()
		v = FunctionGenerator().scale(0.4, about_point=ORIGIN).shift(UP*2).update()

		self.wait(0.4)
		self.play(Create(v), Transform(RLC[0], r), Transform(RLC[1], l), Transform(RLC[2], c), run_time = 2)
		self.remove(RLC)
		self.add(r, l, c)

		wires:list[Wire] = [
			*connect_with_square_wire(c, 'right', v, 'right'),
			*connect_with_square_wire(c, 'left', l, 'right'),
			*connect_with_square_wire(r, 'left', v, 'left'),
			*connect_with_square_wire(r, 'right', l, 'left')
		]

		for wire in wires:
			wire.scale(0.4)

		self.play(FadeIn(*wires))

		VIN = Text("V(t)", font_size = 75).next_to(v, UP)
		RLC = Text("RLC", font_size = 75).next_to(r, RIGHT)
		RLC[0].next_to(r, LEFT)
		RLC[1].next_to(l, DOWN)
		RLC[2].next_to(c, RIGHT)
		rText = Text("1Ω", font_size = 75).next_to(r, RIGHT)
		rText = Text("1Ω", font_size = 75).next_to(r, RIGHT)
		self.play(Write(VIN), Write(RLC), run_time = 1.4)

		rlc_ciruit = Group(r, l, c, RLC, v, VIN, *wires)
		self.wait(0.2)
		self.play(rlc_ciruit.animate.shift(LEFT*4).scale(0.5), run_time = 1.5)

		plane1 = NumberPlane(
			x_range=[0,20],
			y_range=[-6,6],
			axis_config = {
				'font_size' : 3000
			}
		)
		graph = ImplicitFunction(
			lambda x, y: y - 5*np.cos(x/2),
			x_range=[0, 20],
			y_range=[-6, 6],
			color=YELLOW
		).shift(LEFT*10)
		v_graph = Group(plane1, graph, plane1.get_x_axis_label('t')).scale(0.25).shift(RIGHT*3)
		self.play(FadeIn(v_graph))
		
