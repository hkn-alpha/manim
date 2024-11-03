from manim import *

class Terminal(Dot):
	def __init__(self, *args, **kwargs):
		kwargs['stroke_width'] 	= kwargs.get('stroke_width', 0)
		kwargs['fill_opacity'] 	= kwargs.get('fill_opacity', 0)
		Dot.__init__(self, *args, **kwargs)