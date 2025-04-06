"""
Specialized VMobjects for Circuit Elements, abbreviated as cElems.
Custom VMobjects are all built entirely natively using VMobject Cubic Bezier Rendering
"""

from manim import VMobject
from manim.animation.animation import override_animation
from manim.animation.creation import Create, ShowPartial
from manim.constants import LineJointType, CapStyleType, ORIGIN, PI, TAU, RIGHT, UP, LEFT, DOWN
from manim.utils.color.manim_colors import WHITE
from manim.typing import Vector3D
from manim_hkn.terminal import Terminal
import numpy as np

# Template class for all Cubic-Bezier Vectorized Circuit Elements
class _CircuitElementTemplate(VMobject):
	def __init__(self: "_CircuitElementTemplate",
			  terminalCoords: dict[str, list[float]],
			  reverse_points: bool = False,
			  **kwargs) -> None:
		kwargs['stroke_width'] 	= kwargs.get('stroke_width', 	15)
		kwargs['color'] 		= kwargs.get('color', 			WHITE)
		kwargs['joint_type'] 	= kwargs.get('joint_type', 		LineJointType.ROUND)
		kwargs['cap_style'] 	= kwargs.get('cap_style', 		CapStyleType.ROUND)	
		
		self._terminal_scale_factor:float = 0.5
		self._terminals:dict[str, Terminal] = {
			terminal_name:Terminal(radius = kwargs['stroke_width'] * self._terminal_scale_factor, point = terminalCoords[terminal_name])
			
			for terminal_name in terminalCoords
		}

		self._reverse_points = reverse_points

		VMobject.__init__(self,	**kwargs)
		
		self.add(*self._terminals.values())

		def _update_width(self:"_CircuitElementTemplate"):
			VMobject.set_stroke(self, width=100.*list(self._terminals.values())[0].width / self._terminal_scale_factor)
		self.add_updater(_update_width)
	def generate_points(self:"_CircuitElementTemplate") -> None:
		if self._reverse_points:
			self.points = self.points[::-1]

	# Set stroke override. With this, and the updater added to circuit elements in __init__, we enable scaling of an element to also scale the width accordingly, while also enabling scaling width in isolation.
	def set_stroke(self:"_CircuitElementTemplate", *args, width:float = None, **kwargs) -> "_CircuitElementTemplate":
		if width is not None and width != 0.:
			self._terminal_scale_factor = list(self._terminals.values())[0].width / (width/100.)
		return VMobject.set_stroke(self, *args, **kwargs)

	# Helper methods which generate and add the necessary bezier curves to define some common geometries. These become extremely useful when generating complex geometries.
	def _add_geom_arc(	self:"_CircuitElementTemplate",
				   		start_angle:float	= 0,
				   		angle:float 		= PI / 2,
						center:list[float]	= ORIGIN,
						radius:float = 1) -> None:
		self._close_last_curve()
		
		num_components:int = int(9 * abs(start_angle - angle) / TAU) + 1
		d_theta:float = angle / (num_components - 1.0)

		anchors:list[list[float]] = np.array(
        	radius * np.array([
                np.cos(a) * RIGHT + np.sin(a) * UP
                for a in np.linspace(
                    start_angle,
                    start_angle + angle,
                    num_components,
                )
            ])
        )
		tangent_vectors:list[list[float]] = np.zeros(anchors.shape)
		tangent_vectors[:, 1] = anchors[:, 0]
		tangent_vectors[:, 0] = -anchors[:, 1]

		anchors:list[list[float]] = [anchor + center for anchor in anchors]
		handles1:list[list[float]] = anchors[:-1] + (d_theta / 3) * tangent_vectors[:-1]
		handles2:list[list[float]] = anchors[1:] - (d_theta / 3) * tangent_vectors[1:]

		arrays:list[list[list[float]]] = np.array([anchors[:-1], handles1, handles2, anchors[1:]])

		for i in range(arrays.shape[1]):
			self.add_cubic_bezier_curve(
				arrays[0][i],
				arrays[1][i],
				arrays[2][i],
				arrays[3][i]
			)
	def _add_geom_circle(	self:"_CircuitElementTemplate",
							start_angle:float	= 0,
							center:list[float]	= ORIGIN,
							radius:float = 1) -> None:
		self._add_geom_arc(start_angle, TAU, center, radius)
	def _add_geom_elliptical_arc(	self:"_CircuitElementTemplate",
									start_angle:float	= 0,
									angle:float 		= PI / 2,
									center:list[float]	= ORIGIN,
									width:float = 2,
									height:float = 1) -> None:
		arc_start_index = len(self.points)
		self._add_geom_arc(start_angle, angle, ORIGIN, radius = 0.5)
		for i in range(arc_start_index, len(self.points)):
			self.points[i][0] *= width
			self.points[i][1] *= height
			self.points[i] += center
	def _add_geom_ellipse(	self:"_CircuitElementTemplate",
							start_angle:float	= 0,
							center:list[float]	= ORIGIN,
							width:float = 2,
							height:float = 1) -> None:
		self._add_geom_elliptical_arc(start_angle, TAU, center, width, height)
	def _add_geom_linear_path(	self:"_CircuitElementTemplate",
						   		vertices:list[list[float]]) -> None:
		self.start_new_path(np.array(vertices[0]))
		self.add_points_as_corners([np.array(vertex) for vertex in vertices[1:]])
	def _add_geom_polygram(	self:"_CircuitElementTemplate",
							*vertex_groups:list[list[float]]) -> None:
		for vertex_group in vertex_groups:
			self._add_geom_linear_path(vertex_group)
	def _add_geom_pointer(
			self:"_CircuitElementTemplate",
			tip_coord:list[float]=ORIGIN,
			target_coord:list[float]=ORIGIN,
			width:float=0.5,
			length:float=0.7,
			pointer_notch_depth_ratio:float=0.3) -> None:
		triangle_direction_vector:list[float] = (np.array(target_coord)-np.array(tip_coord)) / np.linalg.norm(np.array(target_coord)-np.array(tip_coord))
		triangle_orthogonal_vector:list[float] = np.array([triangle_direction_vector[1], -triangle_direction_vector[0], 0])
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
	def _close_last_curve(self:"_CircuitElementTemplate") -> None:
		if len(self.points) % 4 != 0:
			last_anchor = self.get_start_anchors()[-1]
			for _ in range(4 - (len(self.points) % 4)):
				self.append_points([last_anchor])

	# Returns the coordinate of the specified terminal
	def get_terminal_coord(self:"_CircuitElementTemplate", terminal_name: str) -> list[float]:
		return self._terminals[terminal_name].get_center()
	
	"""
	Returns a shift transformation that shifts two circuit elements such that the specified terminals are "connected"
	ex: capacitor.connect_terminals('left', resistor, 'right'))
		will shift the capacitor over to the location such that the left terminal of the capacitor and right terminal of the resistor to overlap and appear connected
	"""
	def connect_terminals(
			self,
			source_terminal_name: str,
			dest: "_CircuitElementTemplate",
			dest_terminal_name: str
			) -> "_CircuitElementTemplate":
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

class CurrentSource(_CircuitElementTemplate):
	def __init__(self:"CurrentSource", **kwargs) -> None:
		
		kwargs['stroke_width'] = kwargs.get('stroke_width', 3) 
		
		self._circle_radius: float = 0.5
		self._arrow_length: float = 0.35
		self._arrow_head_length: float = 0.25
		self._arrow_head_width: float = 0.15
		
		terminal_wire_length = kwargs.pop('terminal_wire_length', 0.25)
		self._terminal_wire_length: float = terminal_wire_length
		
		terminal_coords = {
			'top': [0, self._circle_radius + self._terminal_wire_length, 0],
			'bottom': [0, -self._circle_radius - self._terminal_wire_length, 0]
		}
	
		super().__init__(
			terminalCoords=terminal_coords,
			**kwargs
		)
	
	def generate_points(self:"CurrentSource") -> None:
		# Draw the circle
		self._add_geom_circle(
			radius=self._circle_radius,
			center=ORIGIN
		)
		
		# Arrow shaft
		self._add_geom_linear_path([
			[0, -self._arrow_length, 0],
			[0, self._arrow_length - self._arrow_head_length, 0]  # Stop before the arrow head
		])
		
		# Arrow head
		self._add_geom_pointer(
			tip_coord=[0, self._arrow_length, 0],
			target_coord=[0, self._arrow_length + self._arrow_head_length, 0],
			width=self._arrow_head_width,
			length=self._arrow_head_length,
			pointer_notch_depth_ratio=0
		)
		
		# Terminal wires
		self._add_geom_linear_path([
			[0, self._circle_radius, 0],
			[0, self._circle_radius + self._terminal_wire_length, 0]
		])
		self._add_geom_linear_path([
			[0, -self._circle_radius, 0],
			[0, -self._circle_radius - self._terminal_wire_length, 0]
		])
		
		super().generate_points()


class OpAmp(_CircuitElementTemplate):
	def __init__(self:"OpAmp", non_inverting_terminal_on_top:bool = True, include_bias_terminals:bool = False, **kwargs) -> None:
		triangle_width:float = 3.5 / np.sqrt(3)
		self._polygram:list[list[list[float]]] = [
			# input terminals
			[[-1.75, 1,0],[-2.75, 1, 0]],
			[[-1.75,-1,0],[-2.75,-1, 0]],
			# output terminal
			[[ 1.75, 0,0],[ 2.75, 0, 0]],
			# symbols
			[[-1.25, -1.25 + 2.00 * non_inverting_terminal_on_top, 0], [-1.25, -0.75 + 2.00 * non_inverting_terminal_on_top, 0]],
			[[-1.50, -1.00 + 2.00 * non_inverting_terminal_on_top, 0], [-1.00, -1.00 + 2.00 * non_inverting_terminal_on_top, 0]],
			[[-1.50,  1.00 - 2.00 * non_inverting_terminal_on_top, 0], [-1.00,  1.00 - 2.00 * non_inverting_terminal_on_top, 0]],
		]
		# bias terminals
		if include_bias_terminals:
			self._polygram[3:3] = [
				[[0, triangle_width/2, 0],[0, triangle_width/2 + 1, 0]],
				[[0,-triangle_width/2, 0],[0, -triangle_width/2 - 1, 0]]
			]

		super().__init__(
			terminalCoords={
				'non-inverting input'	: self._polygram[0][1],
				'inverting input'		: self._polygram[1][1],
				'output'				: self._polygram[2][1]
			} | ({
				'V+'					: self._polygram[3][1],
				'V-'					: self._polygram[4][1]
			} if include_bias_terminals else {}),
			**kwargs
		)

	def generate_points(self:"OpAmp") -> None:
		self._add_geom_pointer(
			tip_coord	 = self._polygram[2][0],
			target_coord = self._polygram[2][1],
			width  = (self._polygram[2][0][0] - self._polygram[0][0][0]) * 2 / np.sqrt(3),
			length =  self._polygram[2][0][0] - self._polygram[0][0][0],
			pointer_notch_depth_ratio = 0
		)
		self._add_geom_polygram(*self._polygram)
		super().generate_points()

class BJT_NPN(_CircuitElementTemplate):
	# Defines how far down the emmitter trace on the diagram the arrow tip is located
	_ARROW_DIST_RATIO:float = 0.7
	# Defines the width of the arrow (not including its stroke thickness) relative to the stroke width of the BJT
	_ARROW_WIDTH_RATIO:float = 2.6
	# Defines the length of the arrow (not including its stroke thickness) relative to the stroke width of the BJT
	# Defined in terms of _ARROW_WIDTH_RATIO to make scaling easier
	_ARROW_LENGTH_RATIO:float = 1.1 * _ARROW_WIDTH_RATIO

	def __init__(self:"BJT_NPN", **kwargs) -> None:
		kwargs['joint_type'] 	= kwargs.get('joint_type', LineJointType.MITER)

		# we split up each line segment into seperate disconnected segments, in order to round edges (using round cap styles) while maintaining the MITER joint type which is necessary for the sharp triangle.
		self._polygram:list[list[list[float]]] = [
			[[	-1.2,	0.8,	0], [	1.2,	0.8,	0]],
			[[	0,		0.8,	0], [	0,		2.3,	0]],
			[[	-0.8,	0.8,	0], [	-1.3,	-1,		0]],
			[[	0.8,	0.8,	0], [	1.3,	-1,		0]],
			[[	-1.3,	-1,		0], [	-2.5,	-1,		0]],
			[[	1.3,	-1,		0], [	2.5,	-1,		0]]
		]

		super().__init__(
			terminalCoords={
				'collector'	: self._polygram[-1][1],
				'emitter'	: self._polygram[-2][1],
				'gate'		: self._polygram[1][1]
			},
			**kwargs
		)
	
	def generate_points(self:"BJT_NPN") -> None:
		# Main BJT Circle
		self._add_geom_circle(radius=2)
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
		super().generate_points()

class Capacitor(_CircuitElementTemplate):
	# This ratio is used for the following geometric equality: <Capacitor Height> = 2/3 * HEIGHT_RATIO * <Capacitor Width>
	HEIGHT_RATIO:float = 1.5

	def __init__(self:"Capacitor", **kwargs) -> None:
		# Define polygram for Capacitor shape
		self._polygram:list[list[list[float]]]  = [
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
		
		super().__init__(
			terminalCoords={
				'left'	: self._polygram[0][0],
				'right'	: self._polygram[1][0]
			},
			**kwargs
		)
		
	def generate_points(self:"Capacitor") -> None:
		self._add_geom_polygram(*self._polygram)
		super().generate_points()

class Inductor(_CircuitElementTemplate):
	# This ratio is used for the following geometric equality: <Inductor Width> = 2 * SPREAD_RATIO * <Inductor Height>
	# In other words, this is defined by SPREAD_RATIO = 0.5 * <Inductor Width> / <Inductor Height
	SPREAD_RATIO:float = 1.6
	# Width of the ellipses forming the upper half of the inductor
	UPPER_ELLIPSE_SPREAD:float = 1.75
	def __init__(self:"Inductor", **kwargs) -> None:
		# Generating vertices for Resistor
		self._polygram:list[list[list[float]]] = [
			[[ -2 * Inductor.SPREAD_RATIO,  0, 0],[-1.5 * Inductor.SPREAD_RATIO,  0, 0]],
			[[1.5 * Inductor.SPREAD_RATIO,  0, 0],[   2 * Inductor.SPREAD_RATIO,  0, 0]]
		]
		super().__init__(
			terminalCoords={
				'left'	: self._polygram[0][0],
				'right'	: self._polygram[1][1]
			},
			**kwargs
		)
	
	def generate_points(self:"Inductor") -> None:
		self._add_geom_linear_path(self._polygram[0])

		loop_width:float = (self._polygram[1][0][0] - self._polygram[0][1][0] - Inductor.UPPER_ELLIPSE_SPREAD) / 3

		for i in range(-1,1+1,1):
			self._add_geom_elliptical_arc(start_angle=PI, angle=-PI, center=RIGHT * (i - 0.5) * loop_width, width=Inductor.UPPER_ELLIPSE_SPREAD, height=2)
			self._add_geom_elliptical_arc(start_angle=0, angle=-PI, center=RIGHT * (i - 0.0) * loop_width, width=Inductor.UPPER_ELLIPSE_SPREAD - loop_width, height=1.4)

		self._add_geom_elliptical_arc(start_angle=PI, angle=-PI, center=RIGHT * 1.5 * loop_width, width=Inductor.UPPER_ELLIPSE_SPREAD, height=2)
		self._add_geom_linear_path(self._polygram[1])
		super().generate_points()

class FunctionGenerator(_CircuitElementTemplate):
	def __init__(self:"FunctionGenerator", **kwargs) -> None:
		self._polygram = [
			[[-2,0,0], [-1.5,0,0]],
			[[ 1.5,0,0], [ 2,0,0]]
		]
		super().__init__(
			terminalCoords={
				'left'	: self._polygram[0][0],
				'right'	: self._polygram[1][1]
			},
			**kwargs
		)

	def generate_points(self:"FunctionGenerator"):
		self._add_geom_linear_path(self._polygram[0])
		self._add_geom_circle(radius=1.5, start_angle=-PI)
		self._add_geom_elliptical_arc(start_angle=3*PI/4, angle=-PI/2, center=[-0.75/np.sqrt(2),-2.5/np.sqrt(2),0], width = 1.5, height = 5)
		self._add_geom_elliptical_arc(start_angle=-3*PI/4, angle=PI/2, center=[0.75/np.sqrt(2),2.5/np.sqrt(2),0], width = 1.5, height = 5)
		self._add_geom_linear_path(self._polygram[1])

class Battery(_CircuitElementTemplate):
	def __init__(self:"Battery", **kwargs) -> None:
		self._polygram:list[list[list[float]]] = [
			[
				[-2,0,0],
				[-0.5,0,0],
				[-0.5,1,0],
				[-0.5,-1,0]
			],[
				[2,0,0],
				[0.5,0,0],
				[0.5,2,0],
				[0.5,-2,0]
			]
		]
		super().__init__(
			terminalCoords={
				'positive'	: self._polygram[1][0],
				'negative'	: self._polygram[0][0]
			},
			**kwargs
		)
		
	def generate_points(self) -> None:
		self._add_geom_polygram(*self._polygram)
		super().generate_points()


class Ground(_CircuitElementTemplate):
	def __init__(self:"Battery", **kwargs) -> None:
		self._polygram:list[list[list[float]]] = [
			[
				[0,0,0],
				[ 0,-0.5,0],
				[-1,-0.5,0],
				[+1,-0.5,0],
			],[
				[-0.66,-0.9,0],
				[+0.66,-0.9,0],
			],[
				[-0.33,-1.3,0],
				[+0.33,-1.3,0],
			]
		]
		super().__init__(
			terminalCoords={
				'ground'	: self._polygram[1][0]
			},
			**kwargs
		)
		
	def generate_points(self) -> None:
		self._add_geom_polygram(*self._polygram)
		super().generate_points()

class Resistor(_CircuitElementTemplate):
	# This ratio is used for the following geometric equality: <Resistor Width> = 2 * SPREAD_RATIO * <Resistor Height>
	# In other words, this is defined by SPREAD_RATIO = 0.5 * <Resistor Width> / <Resistor Height
	SPREAD_RATIO:float = 1.25

	def __init__(self:"Resistor", **kwargs) -> None:
		# Generating vertices for Resistor
		self._vertices:list[list[float]] = [[Resistor.SPREAD_RATIO*(-2),  0, 0]]
		for i in range(-1, 1+1, 1):
			self._vertices.extend([ [Resistor.SPREAD_RATIO*(i-0.5),  0, 0],
									[Resistor.SPREAD_RATIO*(i-0.25),  1, 0],
									[Resistor.SPREAD_RATIO*(i+0.25), -1, 0],
									[Resistor.SPREAD_RATIO*(i+0.5),  0, 0]])
		self._vertices.append(		[Resistor.SPREAD_RATIO*(2),  0, 0])

		super().__init__(
			terminalCoords={
				'left'	: self._vertices[0],
				'right'	: self._vertices[-1]
			},
			**kwargs
		)
	
	def generate_points(self:"Resistor") -> None:
		self._add_geom_linear_path(self._vertices)
		super().generate_points()

class Wire(_CircuitElementTemplate):
	def __init__(self:"Wire", **kwargs) -> None:
		self._target_coordinates:dict[str, list[float]] = {
				'left'  : [-1, 0, 0],
				'right' : [ 1, 0, 0]
			}
		
		super().__init__(
			terminalCoords=self._target_coordinates,
			**kwargs
		)

		self._terminal_bindings:dict[str, list[ Terminal]] = {
			key : [None, None, None] for key in self._terminals.keys()
		}

		self.add_updater(Wire._update_shape, call_updater=True)

	def _update_shape(self:"Wire") -> None:
		self._target_coordinates = {
				key : np.array([(self._terminal_bindings[key][i] or self._terminals[key]).get_center()[i]
				for i in range(3)])
				for key in self._terminals.keys()}
		for key in self._terminals.keys():
			self._terminals[key].move_to(self._target_coordinates[key]) 
		self.generate_points()

	def bind_terminal(
			self:"Wire", 
			source_terminal:str, 
			dest:_CircuitElementTemplate,
			dest_terminal:str,
			bind_axes=Vector3D) -> None:
		if source_terminal not in self._terminal_bindings:
			raise ValueError(f'Invalid Source Terminal: {source_terminal}.')
		
		for i in range(3):
			if bind_axes[i] != 0:
				if bind_axes[i] != 1:
					raise ValueError(f'Invalid Axis: {bind_axes}, each element of the axis must be either 0 or 1.')
				self._terminal_bindings[source_terminal][i] = dest._terminals[dest_terminal]

		self._update_shape()

	def generate_points(self:"Wire") -> None:
		self.clear_points()
		self._add_geom_linear_path([self._target_coordinates[key] for key in self._terminals.keys()])
		super().generate_points()

	def set_terminal_coordinate(self:"Wire", key:str, coord:list[float]) -> "Wire":
		self._target_coordinates[key] = coord
		self._terminals[key].shift(
			self._target_coordinates[key] - 
			self._terminals[key].get_center())
		self._update_shape()