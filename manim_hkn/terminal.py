import numpy as np
from manim import Dot
from manim.typing import Vector3D, Point3D
from manim.constants import ORIGIN
from manim.utils.color.manim_colors import BLUE
from functools import reduce
import operator as op

class Terminal(Dot):
	def __init__(self, *args, **kwargs):
		kwargs['radius'] 			= kwargs.get('radius', 1) / 30.
		kwargs['stroke_width'] 		= kwargs.get('stroke_width', 0)
		kwargs['fill_opacity'] 		= kwargs.get('fill_opacity', 0)
		kwargs['stroke_opacity'] 	= kwargs.get('stroke_opacity', 0)
		kwargs['color']		 		= kwargs.get('color', BLUE.invert()).invert()

		self._terminal_center:Point3D = ORIGIN

		Dot.__init__(self, *args, **kwargs)
	
	def generate_points(self) -> None:
		super().generate_points()
		self.points = np.concatenate(([self.arc_center for i in range(4)], self.points))
	
	def get_center(self) -> Point3D:
		return self.points[0]
	def get_arc_center(self) -> Point3D:
		return self.points[0]
	def get_center_of_mass(self) -> Point3D:
		return self.points[0]
	
