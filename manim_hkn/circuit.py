from manim import *

class Circuit(VGroup):
	def __init__(self, *dots, **kwargs):
		VGroup.__init__(self, *dots, **kwargs)
		self.cNodes
		for node in self.cNodes:
			if node != self.cNodes[0]:
				node.add_updater(lambda mobject: mobject.set_stroke_width(100*self.cNodes[0].width))
		
