from manim import *
from manim_hkn.cElements import Wire, _CircuitElementTemplate

def connect_with_straight_wire(left_cElem:_CircuitElementTemplate, left_terminal:Dot, right_cElem:_CircuitElementTemplate, right_terminal:Dot):
	wire = Wire()
	if left_cElem is not None and left_terminal is not None:
		wire.bind_terminal('left',  left_cElem,  left_terminal,  X_AXIS+Y_AXIS+Z_AXIS)
	if right_cElem is not None and right_terminal is not None:
		wire.bind_terminal('right', right_cElem, right_terminal, X_AXIS+Y_AXIS+Z_AXIS)
	return wire
def connect_with_square_wire(x_cElem:_CircuitElementTemplate, x_terminal:Dot, y_cElem:_CircuitElementTemplate, y_terminal:Dot, animation_start:str = 'x'):
	if animation_start != 'x' and animation_start != 'y':
		raise ValueError('Animation start must be either \'x\' or \'y\', corresponding to which terminal to start geometry generation at so that the user can specify create animation behaviors.')

	hWire = Wire()
	vWire = Wire()

	vWire.bind_terminal('left' if animation_start == 'x' else 'right', x_cElem, x_terminal, X_AXIS+Y_AXIS+Z_AXIS)
	hWire.bind_terminal('left' if animation_start == 'y' else 'right', y_cElem, y_terminal, X_AXIS+Y_AXIS+Z_AXIS)

	vWire.bind_terminal('right' if animation_start == 'x' else 'left', x_cElem, x_terminal, X_AXIS)
	vWire.bind_terminal('right' if animation_start == 'x' else 'left', y_cElem, y_terminal, Y_AXIS)
	hWire.bind_terminal('right' if animation_start == 'y' else 'left', x_cElem, x_terminal, X_AXIS)
	hWire.bind_terminal('right' if animation_start == 'y' else 'left', y_cElem, y_terminal, Y_AXIS)

	return hWire, vWire
def split_wire(wire:Wire, split_point:float = 0.5):
	if split_point <= 0 or split_point >= 1:
		raise ValueError('split_point must be between 0 and 1 (exclusive), to determine the location on the wire to split it into 2 wires.')
	lWire = wire.copy()
	rWire = wire.copy()
	
	lWire._terminal_bindings['left']  = wire._terminal_bindings['left']
	lWire._terminal_bindings['right'] = [None, None, None]
	rWire._terminal_bindings['left'] = [None, None, None]
	rWire._terminal_bindings['right'] = wire._terminal_bindings['right']

	lCoord = wire.get_terminal_coord('left')
	rCoord = wire.get_terminal_coord('right')

	lWire.set_terminal_coordinate('left', lCoord)
	lWire.set_terminal_coordinate('right', lCoord + (rCoord - lCoord) * split_point)
	rWire.set_terminal_coordinate('left', lWire.get_terminal_coord('right'))
	rWire.set_terminal_coordinate('right', rCoord)

	return lWire, rWire
