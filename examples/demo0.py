import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from manim import *
from manim_hkn.utils import *
from manim_hkn import *

class test(Scene):
    def construct(self):
        self.wait(0.1)

        b = Battery()
        r1 = Resistor()
        r2 = Resistor(reverse_points=True)
        r3 = Resistor(reverse_points=True)
        r4 = Resistor(reverse_points=True)
        #r5 = Resistor()

        b.shift(LEFT*2.5).rotate(PI/2).scale(0.5)
        r1.shift(UP*2).rotate(0).scale(0.5)
        r2.shift(RIGHT*2.5).rotate(PI/2).scale(0.5)
        r3.shift(DOWN*2).rotate(0).scale(0.5)
        r4.shift(RIGHT*5).rotate(PI/2).scale(0.5)
        #r5.shift(DOWN*4).rotate(0).scale(0.5)

        hw1,vw1=connect_with_square_wire(b, 'positive', r1, 'left')
        hw2,vw2=connect_with_square_wire(r2, 'right', r1, 'right', 'y')
        hw3,vw3=connect_with_square_wire(r4, 'right', r1, 'right', 'y')
        hw4,vw4=connect_with_square_wire(r2, 'left', r3, 'right')
        hw5,vw5=connect_with_square_wire(r4, 'left', r3, 'right')
        hw6,vw6=connect_with_square_wire(b, 'negative', r3, 'left', 'y')
        
        
        

        cElems = [b,vw1,hw1,r1,hw2,vw2,hw3,vw3,r2,vw4,r4,vw5,hw5,r3,hw6,vw6]   

        for cElem in cElems:
            cElem.update()


        for wire in [hw1, vw1, hw2, vw2, hw3, vw3, hw4, vw4, hw5, vw5, hw6, vw6]:
            wire.scale(0.5)
            wire.update()


        #hw0, hw1 = split_wire(hw1, 0.2)
        #hw0.bind_terminal('right', bjt_npn, 'collector', Y_AXIS)
        #hw1.bind_terminal('left', bjt_npn, 'collector', Y_AXIS)

        #r3 = Resistor()
        #r3.rotate(-PI/2).scale(0.5).shift([hw0.get_terminal_coord('right')[0] - r3.get_terminal_coord('left')[0], 0, 0])
        #w0 = connect_with_straight_wire(hw0, 'right', r3, 'left')
        #w1 = Wire()
        #w0=w0.scale(0.5)
        #w1=w1.scale(0.5)
        #w1.set_terminal_coordinate('left', r3.get_terminal_coord('right'))
        #w1.set_terminal_coordinate('right', [r3.get_terminal_coord('right')[0], r1.get_center()[1], r3.get_terminal_coord('right')[2]])

        #cElems = [bjt_npn,hw0,hw1,vw1,c,vw2,hw2,r1,hw3,vw3,r2,vw4,hw4, w0,r3,w1]
        for cElem in cElems:
            cElem.update()
            self.play(Create(cElem))

        self.play(
            b.animate,
            r1.animate,
            r2.animate,
            r3.animate,
            r4.animate
            #r3.animate.shift(DOWN),
            #w1.animate.shift(DOWN)
        )

        #g = Group(*cElems)
        #self.play(g.animate.scale(0.4).shift(LEFT+DOWN))
        #self.play(g.animate.scale(2).shift(LEFT+UP))
        #self.play(c.animate.shift(RIGHT))

        self.wait(0.1)