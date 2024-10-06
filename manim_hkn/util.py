from manim import *

def get_terminal_connect_animation(cElem, sourceTerminal, destTerminal, rotation_angle = 0):
	return MoveAlongPath(cElem, Line(cElem.get_center(), destTerminal + cElem.get_center() - sourceTerminal))