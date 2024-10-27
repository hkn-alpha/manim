"""
Specialized VMobjects for Circuit Elements, abbreviated as cElems.
Custom VMobjects are all built entirely natively using VMobject Cubic Bezier Rendering
"""

from manim import VMobject
from manim.mobject.geometry.arc import Dot
from manim.animation.animation import override_animation
from manim.animation.creation import Create, ShowPartial
from manim.constants import *
from manim.utils.color.manim_colors import WHITE
import numpy as np

# Template class for all Cubic-Bezier Vectorized Circuit Elements
class _CircuitElementTemplate(VMobject):
	def __init__(self,
			  terminalCoords: dict[str, list[float]],
			  **kwargs):
		kwargs['stroke_width'] 	= kwargs.get('stroke_width', 15)
		kwargs['color'] 		= kwargs.get('color', WHITE)
		kwargs['joint_type'] 	= kwargs.get('joint_type', LineJointType.ROUND)
		kwargs['cap_style'] 	= kwargs.get('cap_style', CapStyleType.ROUND)	

		self._terminal_scale_factor = 0.5

		self._terminals:dict[str, Dot] = {
			terminal_name:
				Dot(
					radius			= self._terminal_scale_factor * kwargs['stroke_width']/200.,
					color			= kwargs['color'].invert(),
					fill_opacity	= 0)
				.shift(terminalCoords[terminal_name])
			for terminal_name in terminalCoords
		}
		for dot in self._terminals.values():
			dot.set_stroke(opacity=0)

		VMobject.__init__(self,	**kwargs)
		
		self.add(*self._terminals.values())

		def _update_width(self):
			VMobject.set_stroke(self, width=100.*list(self._terminals.values())[0].width / self._terminal_scale_factor)
		self.add_updater(_update_width)

	# Set stroke override. With this, and the updater added to circuit elements in __init__, we enable scaling of an element to also scale the width accordingly, while also enabling scaling width in isolation.
	def set_stroke(self, *args, width:float = None, **kwargs):
		if width is not None and width != 0.:
			self._terminal_scale_factor = list(self._terminals.values())[0].width / (width/100.)
		VMobject.set_stroke(self, *args, **kwargs)

	# Helper methods which generate and add the necessary bezier curves to define some common geometries. These become extremely useful when generating complex geometries.
	def _add_geom_arc(	self,
				   		start_angle:float	= 0,
				   		angle:float 		= PI / 2,
						center:list[float]	= ORIGIN,
						radius:float = 1):
		self._close_last_curve()
		
		num_components = 9
		d_theta = angle / (num_components - 1.0)

		anchors = np.array(
        	radius * np.array([
                np.cos(a) * RIGHT + np.sin(a) * UP
                for a in np.linspace(
                    start_angle,
                    start_angle + angle,
                    num_components,
                )
            ])
        )
		tangent_vectors = np.zeros(anchors.shape)
		tangent_vectors[:, 1] = anchors[:, 0]
		tangent_vectors[:, 0] = -anchors[:, 1]

		anchors = [anchor + center for anchor in anchors]
		handles1 = anchors[:-1] + (d_theta / 3) * tangent_vectors[:-1]
		handles2 = anchors[1:] - (d_theta / 3) * tangent_vectors[1:]

		if len(self.points) % 4 != 0:
			last_anchor = self.get_start_anchors()[-1]
			for _ in range(4 - (len(self.points) % 4)):
				self.append_points([last_anchor])

		arrays = np.array([anchors[:-1], handles1, handles2, anchors[1:]])
		for i in range(arrays.shape[1]):
			self.add_cubic_bezier_curve(
				arrays[0][i],
				arrays[1][i],
				arrays[2][i],
				arrays[3][i]
			)
	def _add_geom_circle(	self,
							center:list[float]	= ORIGIN,
							radius:float = 1):
		self._add_geom_arc(radius=radius, center=center, angle=TAU)
	def _add_geom_linear_path(	self,
						   		vertices:list[list[float]]):
		self.start_new_path(np.array(vertices[0]))
		self.add_points_as_corners([np.array(vertex) for vertex in vertices[1:]])
	def _add_geom_polygram(	self,
							*vertex_groups:list[list[float]]):
		for vertex_group in vertex_groups:
			self._add_geom_linear_path(vertex_group)
	def _add_geom_pointer(
			self,
			tip_coord:list[float]=ORIGIN,
			target_coord:list[float]=ORIGIN,
			width:float=0.5,
			length:float=0.7,
			pointer_notch_depth_ratio:float=0.3):
		triangle_direction_vector = (np.array(target_coord)-np.array(tip_coord)) / np.linalg.norm(np.array(target_coord)-np.array(tip_coord))
		triangle_orthogonal_vector = np.array([triangle_direction_vector[1], -triangle_direction_vector[0], 0])
		self._add_geom_linear_path([
			tip_coord,
			tip_coord
				- triangle_direction_vector  * length
				+ triangle_orthogonal_vector * width / 2,
			tip_coord
				- triangle_direction_vector  * length * (1 - pointer_notch_depth_ratio),
			tip_coord
				- triangle_direction_vector  * length
				- triangle_orthogonal_vector * width / 2,
			tip_coord
		])

	# When adding bezier curves and defining the geometry of a circuit element, this is a useful method to close any unclosed bezier curves in the internal points list.
	def _close_last_curve(self):
		if len(self.points) % 4 != 0:
			last_anchor = self.get_start_anchors()[-1]
			for _ in range(4 - (len(self.points) % 4)):
				self.append_points([last_anchor])

	# Returns the coordinate of the specified terminal
	def get_terminal_coord(self, terminal_name: str) -> list[float]:
		return self._terminals[terminal_name].get_center()
	# Returns a shift transformation that shifts two circuit elements such that the specified terminals are "connected"
	# ex: 	capacitor.connect_terminals('left', resistor, 'right'))
	#		will shift the capacitor over to the location such that the left terminal of the capacitor and right terminal of the resistor to overlap and appear connected
	def connect_terminals(
			self,
			source_terminal_name: str,
			dest: "_CircuitElementTemplate",
			dest_terminal_name: str
			):
		return self.shift(dest.get_terminal_coord(dest_terminal_name) - self.get_terminal_coord(source_terminal_name))

	# Override the Create animation such that Terminals do not consume runtime. Not including this override causes a significant portion of the create animation runtime to be spent waiting, with no change on the screen due to invisible terminals
	@override_animation(Create)
	def create(self, lag_ratio:float = 0, *args, **kwargs) -> ShowPartial:
		return type('_Create_No_Lag', (ShowPartial,),{
			'_get_bounds': lambda self, alpha: (0, alpha)
		})(
			self,
			lag_ratio=lag_ratio,
			introducer=True,
			*args, **kwargs
		)

class BJT_NPN(_CircuitElementTemplate):
	# Defines how far down the emmitter trace on the diagram the arrow tip is located
	_ARROW_DIST_RATIO = 0.7
	# Defines the width of the arrow (not including its stroke thickness) relative to the stroke width of the BJT
	_ARROW_WIDTH_RATIO = 2.6
	# Defines the length of the arrow (not including its stroke thickness) relative to the stroke width of the BJT
	# Defined in terms of _ARROW_WIDTH_RATIO to make scaling easier
	_ARROW_LENGTH_RATIO = 1.1 * _ARROW_WIDTH_RATIO

	def __init__(self, **kwargs):
		kwargs['joint_type'] 	= kwargs.get('joint_type', LineJointType.MITER)

		# we split up each line segment into seperate disconnected segments, in order to round edges (using round cap styles) while maintaining the MITER joint type which is necessary for the sharp triangle.
		self._polygram = [
			[[	-1.2,	0.8,	0], [	1.2,	0.8,	0]],
			[[	0,		0.8,	0], [	0,		2.3,	0]],
			[[	-0.8,	0.8,	0], [	-1.3,	-1,		0]],
			[[	0.8,	0.8,	0], [	1.3,	-1,		0]],
			[[	-1.3,	-1,		0], [	-2.5,	-1,		0]],
			[[	1.3,	-1,		0], [	2.5,	-1,		0]]
		]

		_CircuitElementTemplate.__init__(
			self,  
			terminalCoords={
				'collector'	: self._polygram[-1][1],
				'emitter'	: self._polygram[-2][1],
				'gate'		: self._polygram[1][1]
			},
			**kwargs
		)
	
	def generate_points(self) -> None:
		# Main BJT Circle
		self._add_geom_circle(radius=self.stroke_width / 8.)
		# Main BJT Gate, Collector, Emitter geometry
		self._add_geom_polygram(*self._polygram)
		# Arrow indicating NPN BJT
		self._add_geom_pointer(
			tip_coord = (np.array(self._polygram[2][1])-np.array(self._polygram[2][0])) * BJT_NPN._ARROW_DIST_RATIO + self._polygram[2][0],
			target_coord = self._polygram[2][1],
			width = BJT_NPN._ARROW_WIDTH_RATIO * self.stroke_width / 100,
			length = BJT_NPN._ARROW_LENGTH_RATIO * self.stroke_width / 100,
			pointer_notch_depth_ratio = 0
		)
		
class Capacitor(_CircuitElementTemplate):
	# This ratio is used for the following geometric equality: <Capacitor Height> = 2/3 * HEIGHT_RATIO * <Capacitor Width>
	HEIGHT_RATIO = 1.5

	def __init__(self, **kwargs):
		# Define polygram for Capacitor shape
		self._polygram  = [
			[
				[-1.5, 0, 0],
				[-0.5, 0, 0],
				[-0.5, Capacitor.HEIGHT_RATIO, 0],
				[-0.5, -Capacitor.HEIGHT_RATIO, 0]
			],
			[
				[ 1.5, 0, 0],
				[ 0.5, 0, 0],
				[ 0.5, Capacitor.HEIGHT_RATIO, 0],
				[ 0.5, -Capacitor.HEIGHT_RATIO, 0]
			]
		]
		
		_CircuitElementTemplate.__init__(
			self,  
			terminalCoords={
				'left'	: self._polygram[0][0],
				'right'	: self._polygram[1][0]
			},
			**kwargs
		)
		
	def generate_points(self) -> None:
		self._add_geom_polygram(*self._polygram)

class Resistor(_CircuitElementTemplate):
	# This ratio is used for the following geometric equality: <Resistor Width> = 2 * SPREAD_RATIO * <Resistor Height>
	# In other words, this is defined by SPREAD_RATIO = 0.5 * <Resistor Width> / <Resistor Height
	SPREAD_RATIO = 1.25

	def __init__(self, **kwargs):
		# Generating vertices for Resistor
		self._vertices = [[Resistor.SPREAD_RATIO*(-2),  0, 0]]
		for i in range(-1, 1+1, 1):
			self._vertices.extend([[Resistor.SPREAD_RATIO*(i-0.5),  0, 0],
				   			[Resistor.SPREAD_RATIO*(i-0.25),  1, 0],
							[Resistor.SPREAD_RATIO*(i+0.25), -1, 0],
							[Resistor.SPREAD_RATIO*(i+0.5),  0, 0]])
		self._vertices.append([Resistor.SPREAD_RATIO*(2),  0, 0])

		_CircuitElementTemplate.__init__(
			self, 
			terminalCoords={
				'left'	: self._vertices[0],
				'right'	: self._vertices[-1]
			},
			**kwargs
		)
	
	def generate_points(self) -> None:
		self._add_geom_linear_path(self._vertices)

class Wire(_CircuitElementTemplate):
	def __init__(self, **kwargs):
		_CircuitElementTemplate.__init__(
			self, 
			terminalCoords={},
			**kwargs
		)
	def generate_points(self) -> None:
		# self._add_geom_linear_path(self._vertices)
		None