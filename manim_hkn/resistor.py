from manim import *

class Resistor:
	def __init__(self, scene, resistance):
		self.resistance = resistance
		self.scene = scene

		self.img = SVGMobject("manim_hkn/assets/svg/resistor_img.svg")
		self.img.color = WHITE

	def add(self):
		self.scene.add(self.img)

	def setSize(self, w):
		self.img.set(width=w)

	def move(self, x, y):
		self.img.set(width=w)

	def remove(self):
		self.scene.remove(self.img)