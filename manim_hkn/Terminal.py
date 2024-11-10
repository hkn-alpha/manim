from manim import *
from manim.typing import Vector3D, Point3D
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
	
	def shift(self, *vectors: Vector3D) -> "Terminal":
		"""Shift by the given vectors.

		Parameters
		----------
		vectors
			Vectors to shift by. If multiple vectors are given, they are added
			together.

		Returns
		-------
		:class:`Mobject`
			``self``

		See also
		--------
		:meth:`move_to`
		"""

		total_vector = reduce(op.add, vectors)
		for mob in self.family_members_with_points():
			mob.points = mob.points.astype("float")
			mob.points += total_vector

		return self
	
	def generate_points(self) -> None:
		super().generate_points()
		self.points = np.concatenate(([self.arc_center for i in range(4)], self.points))
	
	def get_center(self) -> Point3D:
		return self.points[0]
	def get_arc_center(self) -> Point3D:
		return self.points[0]
	def get_center_of_mass(self) -> Point3D:
		return self.points[0]
	