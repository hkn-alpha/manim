from manim import *
from manim_hkn.utils import *
from manim_hkn import *

def HKN_video_start(scene: Scene) -> None:
	scene.hkn_emblem = ImageMobject("manim_hkn/assets/img/hkn_alpha_emblem.png")
	scene.play(FadeIn(scene.hkn_emblem))
	scene.wait(0.75)
	scene.play(scene.hkn_emblem.animate.scale(0.4).to_corner(UR), run_time = 1.5)
	return scene.hkn_emblem
def HKN_video_end(scene: Scene) -> None:
	scene.play(scene.hkn_emblem.animate.scale(1/0.4).move_to(ORIGIN), run_time = 1.5)
	scene.play(FadeOut(scene.hkn_emblem))
	scene.wait(1)

class test(Scene):
	def construct(self):
		HKN_video_start(self)

		RLC = Text('RLC', font_size = 100).shift(UP)
		self.play(FadeIn(RLC))

		r = Resistor().scale(0.4, about_point=ORIGIN).shift(LEFT*1.5).rotate(-PI/2).update()
		l = Inductor().scale(0.4, about_point=ORIGIN).shift(DOWN * 2).update()
		c = Capacitor().scale(0.4, about_point=ORIGIN).shift(RIGHT*1.5).rotate(PI/2).update()
		v = FunctionGenerator().scale(0.4, about_point=ORIGIN).shift(UP*1.5).update()
		self.wait(0.4)
		self.play(
			Create(v), Create(r), Create(l), Create(c), 
			RLC[0].animate.next_to(r, LEFT), RLC[1].animate.next_to(l, DOWN), RLC[2].animate.next_to(c, RIGHT), run_time = 2)

		wires:list[Wire] = [
			*connect_with_square_wire(c, 'right', v, 'right'),
			*connect_with_square_wire(c, 'left', l, 'right'),
			*connect_with_square_wire(r, 'left', v, 'left'),
			*connect_with_square_wire(r, 'right', l, 'left')
		]
		for wire in wires:
			wire.scale(0.4)
		self.play(FadeIn(*wires))

		vText = Text("V(t)", font_size = 75).next_to(v, UP)
		self.play(Write(vText), run_time = 1)
		self.wait()

		rText = MathTex(r"1\Omega", font_size = 100).next_to(r, LEFT)
		lText = MathTex(r"1H", font_size = 100).next_to(l, DOWN)
		cText = MathTex(r"1F", font_size = 100).next_to(c, RIGHT)
		vTextFunc = MathTex(r"cos(2t)V", font_size = 100).next_to(v, UP)
		self.play([ReplacementTransform(RLC[i], [rText, lText, cText][i]) for i in range(3)], ReplacementTransform(vText, vTextFunc))

		rlc_ciruit = Group(r, l, c, v, rText, lText, cText, vTextFunc, *wires)
		self.wait(0.2)
		self.play(rlc_ciruit.animate.shift(LEFT*5 + DOWN).scale(0.5), run_time = 1.5)

		transform_indicator:Group = Group(Text("Frequency Domain"))
		transform_indicator.add(Arrow(start=LEFT, end=RIGHT).scale_to_fit_width(transform_indicator[0].width).shift(DOWN * 0.5)).shift(r.get_y() - transform_indicator[1].get_y()).set_x(0)
		self.play([Create(elem) for elem in transform_indicator])

		freq_domain_rlc = rlc_ciruit.copy().move_to(rlc_ciruit.get_center() - 2 * rlc_ciruit.get_x() * RIGHT)
		freq_domain_rlc.insert(4, MathTex(r"1\Omega", font_size=50).next_to(freq_domain_rlc[0], LEFT))
		freq_domain_rlc.remove(freq_domain_rlc[5])
		freq_domain_rlc.insert(5, MathTex(r"j2\Omega", font_size=50).next_to(freq_domain_rlc[1], DOWN))
		freq_domain_rlc.remove(freq_domain_rlc[6])
		freq_domain_rlc.insert(6, MathTex(r"\frac{1}{j2}\Omega", font_size=50).next_to(freq_domain_rlc[2], RIGHT))
		freq_domain_rlc.remove(freq_domain_rlc[7])
		freq_domain_rlc.insert(7, MathTex(r"1V", font_size=50).next_to(freq_domain_rlc[3], UP))
		freq_domain_rlc.remove(freq_domain_rlc[8])

		self.play(ReplacementTransform(rlc_ciruit.copy(), freq_domain_rlc), run_time=2)
		self.wait(1)
		self.play(Group(rlc_ciruit, transform_indicator, freq_domain_rlc).animate.shift(rlc_ciruit.get_center() - freq_domain_rlc.get_center()), run_time=2)
		self.remove(rlc_ciruit, transform_indicator)
		self.wait(2)

		re_axis:Line = Line([-2.5,0,0], [2.5,0,0]).add_tip(tip_length=0.2, tip_width=0.2).add_tip(tip_length=0.2, tip_width=0.2, at_start=True)
		im_axis:Line = Line([0,-2.5,0],	[0,2.5,0]).add_tip(tip_length=0.2, tip_width=0.2).add_tip(tip_length=0.2, tip_width=0.2, at_start=True)
		re_labels_and_ticks:list[MathTex | Line] = [mobject for i in range(-2, 3, 4) for mobject in (MathTex(rf'{i}')		.shift(DOWN * 0.35 					+ RIGHT * i).scale(0.75), Line([i, -0.1, 0], [i, 0.1, 0]))]
		im_labels_and_ticks:list[MathTex | Line] = [mobject for i in range(-2, 3, 4) for mobject in (MathTex(rf'{i}j')		.shift(LEFT * 0.15*(len(str(i))+1) 	+ UP 	* i).scale(0.75), Line([-0.1, i, 0], [0.1, i, 0]))]
		re_labels_and_ticks.append(MathTex('Re', font_size=50).next_to(re_axis.get_end(), RIGHT))
		im_labels_and_ticks.append(MathTex('Im', font_size=50).next_to(im_axis.get_end(), UP))
		
		t_axis:Line = Line([0,0,0], 	[3.5,0,0]).add_tip(tip_length=0.2, tip_width=0.2)
		y_axis:Line = Line([0,-2.5,0], 	[0,2.5,0]).add_tip(tip_length=0.2, tip_width=0.2).add_tip(tip_length=0.2, tip_width=0.2, at_start=True)
		t_labels_and_ticks:list[MathTex | Line] = [mobject for i in range(2, 3) 	 for mobject in (MathTex(rf'{i//2}\pi')	.shift(DOWN * 0.35 					+ RIGHT * i).scale(0.75), Line([i, -0.1, 0], [i, 0.1, 0]))]
		y_labels_and_ticks:list[MathTex | Line] = [mobject for i in range(-2, 3, 4)	 for mobject in (MathTex(rf'{i//2}')	.shift(LEFT * 0.35 					+ UP 	* i).scale(0.75), Line([-0.1, i, 0], [0.1, i, 0]))]
		t_labels_and_ticks.append(MathTex('t', font_size=50).next_to(t_axis.get_end(), RIGHT))

		phasor_graph = Group()
		phasor_graph_origin = [0, -1, 0]
		phasor_graph 	= Group(re_axis, *re_labels_and_ticks, im_axis, *im_labels_and_ticks).scale(0.75).shift(phasor_graph_origin - im_axis.get_midpoint())
		td_graph:Group = Group()
		td_graph_origin = [4,-1,0]
		td_graph 		= Group(t_axis,  *t_labels_and_ticks,  y_axis,  *y_labels_and_ticks ).scale(0.75).shift(td_graph_origin - y_axis.get_midpoint())
		
		current_indicator:Group = Group(Arc(radius=0.4, start_angle=PI*0.45, angle=-PI*0.45, arc_center=freq_domain_rlc[8].get_terminal_coord('left')).add_tip(tip_length=0.2, tip_width=0.2)).shift((LEFT+DOWN)*0.1)
		current_indicator.add(Text('I', font_size=30).move_to(current_indicator[0].get_center()).shift((UP+RIGHT) * current_indicator[0].width / 2))

		self.play([Create(component) for group in [td_graph, phasor_graph, current_indicator] for component in group])
		self.wait(1)

		phasors = Group(
			Line(phasor_graph_origin, phasor_graph_origin + RIGHT	* 0.75, stroke_width=10, buff=0, color=BLUE)	.add_tip(tip_length=0.2, tip_width=0.2),
			Line(phasor_graph_origin, phasor_graph_origin + UP*2	* 0.75, stroke_width=10, buff=0, color=RED)		.add_tip(tip_length=0.2, tip_width=0.2),
			Line(phasor_graph_origin, phasor_graph_origin + DOWN/2	* 0.75, stroke_width=10, buff=0, color=GREEN)	.add_tip(tip_length=0.2, tip_width=0.2),
			Line(phasor_graph_origin, phasor_graph_origin + (UP*1.5+RIGHT)	* 0.75, stroke_width=10, buff=0, color=YELLOW)	.add_tip(tip_length=0.2, tip_width=0.2)
			)
		phasors.add(Angle(phasors[0], phasors[3], radius=0.5, other_angle=False))
		for i in range(3):
			self.play(FadeToColor(freq_domain_rlc[i], phasors[i].get_color()), FadeToColor(freq_domain_rlc[i+4], phasors[i].get_color()), FadeIn(phasors[i]), run_time=0.5)
			self.play(Indicate(freq_domain_rlc[i]), Indicate(freq_domain_rlc[i+4]), Indicate(phasors[i]), run_time=2)
		
		t:ValueTracker = ValueTracker(1)
		phi_indicator = Group(	always_redraw(lambda: Angle(phasors[0], phasors[3], radius=0.5, other_angle=False, stroke_opacity=min(PI, 2 - t.get_value() / PI))),
								always_redraw(lambda: MathTex(r"\phi", opacity=min(PI, 2 - t.get_value() / PI), stroke_opacity=min(PI, 2 - t.get_value() / PI), fill_opacity=min(PI, 2 - t.get_value() / PI)).move_to(Angle(phasors[0], phasors[3], radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)))
								)
		eqns = Group(	MathTex(r'\tilde{V} = 1V = \tilde{I} • Z_{tot}').next_to(phasor_graph, UP),
						MathTex(r'Z_{tot} = Z_R + Z_L + Z_C').to_edge(DOWN)).set_color(phasors[3].get_color())
		self.play(FadeIn(eqns), FadeIn(phasors[3], phi_indicator), run_time=0.5)
		self.play(Indicate(eqns), Indicate(phasors[3]), run_time=2)
		
		def update_pos(func: FunctionGraph) -> None:
			try:
				func.shift(td_graph_origin - func.get_start() + UP * 0.75 * func.get_point_from_function(0)[1])
			except Exception:
				pass
		i_func = always_redraw(lambda: FunctionGraph(
            lambda t: 2*np.cos(t*PI - np.arctan(1.5)) * (1/(1 + 1.5j)).real,
			x_range=[0,t.get_value()/PI*2],
            color=PURPLE,
			stroke_opacity=min(PI, 2 - t.get_value() / PI)
        ).scale(0.75)).add_updater(update_pos)
		v_func = always_redraw(lambda: FunctionGraph(
            lambda t: 2*np.cos(t*PI),
			x_range=[0,t.get_value()/PI*2],
			color=YELLOW,
			stroke_opacity=min(PI, 2 - t.get_value() / PI)
        ).scale(0.75)).add_updater(update_pos)
		funcs = Group(i_func, v_func)
		self.add(funcs)
		t.set_value(0)
		
		td_graph.add(
			Text("V(t)", color=YELLOW, font_size=30).next_to(td_graph_origin + UP * 0.75 * v_func.get_point_from_function(0)[1] + LEFT * 0.2, LEFT),
			Text("I(t)", color=PURPLE, font_size=30).next_to(td_graph_origin + UP * 0.75 * i_func.get_point_from_function(0)[1] + LEFT * 0.2, LEFT))
		self.play(FadeIn(td_graph[-2:]), Rotate(phasors, -np.arctan(1.5), about_point=phasor_graph_origin), run_time=1)
		self.wait(0.25)

		phasors.add_updater(lambda mobject, dt: mobject.rotate(dt * 2, about_point=phasor_graph_origin))
		self.play(t.animate(rate_func=linear).set_value(PI), run_time = PI)
		self.play(t.animate(rate_func=linear).set_value(TAU), FadeOut(phasors, freq_domain_rlc, td_graph, phasor_graph, current_indicator, eqns, rate_func=linear), run_time=PI)
		self.remove(phi_indicator, funcs)
		self.wait(1)

		all_elements = VGroup(FunctionGenerator(), Resistor(), Capacitor(), Inductor(), OpAmp(), Battery(), Ground(), BJT_NPN()).arrange_in_grid(rows = 2, cols = 4, buff = -2, cell_alignment=ORIGIN).shift(DOWN)
		
		for elem in all_elements:
			self.play(Create(elem.scale(0.4).update()), run_time = 1)
		self.wait(1)

		final_text = Text("Manim HKN").scale(3)
		self.play(*[ReplacementTransform(all_elements[i // 2 + 4 * (i % 2)], final_text[i]) for i in range(len(all_elements))], run_time = 2)
		self.wait()
		self.play(FadeOut(final_text))

		HKN_video_end(self)

