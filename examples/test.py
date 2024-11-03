from manim import *
from manim_hkn.utils import *
from manim_hkn import *

class test(Scene):
	def construct(self):
		self.wait(0.1)

		r1 = Resistor()
		r2 = Resistor()
		c = Capacitor()
		bjt_npn = BJT_NPN()


		bjt_npn.shift(UP*2).scale(0.5)
		r1.shift(DOWN*2).rotate(PI).scale(0.5)
		r2.shift(LEFT*3).rotate(PI/2).scale(0.5)
		c.shift(RIGHT*3).rotate(-PI/2).scale(0.5)

		hw1,vw1=connect_with_square_wire(c, 'left', bjt_npn, 'collector', 'y')
		hw2,vw2=connect_with_square_wire(c, 'right', r1, 'left', 'x')
		hw3,vw3=connect_with_square_wire(r2, 'left', r1, 'right', 'y')
		hw4,vw4=connect_with_square_wire(r2, 'right', bjt_npn, 'emitter', 'x')
		cElems = [bjt_npn,hw1,vw1,c,vw2,hw2,r1,hw3,vw3,r2,vw4,hw4]

		for cElem in cElems:
			cElem.update()


		for wire in [hw1, vw1, hw2, vw2, hw3, vw3, hw4, vw4]:
			wire.scale(0.5)
			wire.update()

			
		hw0, hw1 = split_wire(hw1, 0.2)
		hw0.bind_terminal('right', bjt_npn, 'collector', Y_AXIS)
		hw1.bind_terminal('left', bjt_npn, 'collector', Y_AXIS)

		r3 = Resistor()
		r3.rotate(-PI/2).scale(0.5).shift([hw0.get_terminal_coord('right')[0] - r3.get_terminal_coord('left')[0], 0, 0])
		w0 = connect_with_straight_wire(hw0, 'right', r3, 'left')
		w1 = Wire()
		w0=w0.scale(0.5)
		w1=w1.scale(0.5)
		w1.set_terminal_coordinate('left', r3.get_terminal_coord('right'))
		w1.set_terminal_coordinate('right', [r3.get_terminal_coord('right')[0], r1.get_center()[1], r3.get_terminal_coord('right')[2]])

		cElems = [bjt_npn,hw0,hw1,vw1,c,vw2,hw2,r1,hw3,vw3,r2,vw4,hw4, w0,r3,w1]
		for cElem in cElems:
			cElem.update()
			self.play(Create(cElem))

		self.play(bjt_npn.animate.shift(DOWN*0.5+LEFT),
			c.animate.shift(RIGHT),
			r2.animate.shift(DOWN),
			r1.animate.shift(DOWN+LEFT),
			r3.animate.shift(DOWN),
			w1.animate.shift(DOWN))
		
		self.wait(0.1)
