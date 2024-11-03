For HKN Backend Package Developers
==================================
General Development Guide for contributors.
# Overview
This Development Guide contains the general guidelines for an HKN Member contributing to the backend of the manim_hkn package, which serves as a wrapper for the manim community version, specially equipped for HKN Alpha video animations. More details can be found in the [repository README](https://github.com/hkn-alpha/manim/blob/main/README.md). This Development Guide is for developers adding new circuit elements and functionality to the package.
## Prerequisites
In order to make meaningful contributions to this package, first you must learn the fundamentals of manim from the community [Tutorials & Guides](https://docs.manim.community/en/stable/tutorials_guides.html) page. This may seem tedious, but is a crucial step in being able to make efficient contributions to this package, and will help you save many hours of incredibly difficult debugging down the line.
## Manim Documentation
https://docs.manim.community/en/stable/index.html
# Circuit Element Guidelines
The bare minimum requirements for a class definition of any circuit element:
- Must be a subclass of `_CircuitElementTemplate`
- The `__init__` method must be properly defined, and must correctly call the parent class `__init__` method
- Definition of the element's geometries within the `generate_points` method
## `_CircuitElementTemplate` parent class
This template class serves as an abstract class which all Circuit Elements must inherit from. It inherits from `VMobject` defined by manim, and defines some basic functionality for package users, assisting in the streamlined development of circuit animations, such as the `connect_terminals` functionality. It overrides certain methods of the native `VMobject` type, in order to behave as one would typically desire for a majority of circuit animations, such as scaling stroke width relative to object size, and preventing the unwanted animation of `Terminal`s.
### Terminals
Each `_CircuitElementTemplate` subclass will have a `_terminals` property, which is a dictionary of `Terminal` objects, which are all subclasses of `Dot` as values, each of which represents one "Terminal" of the circuit element. These are "points" on the element which wires and other circuit elements can connect to. For example, a resistor and capacitor will each have `2` terminals, an NPN BJT will have `3`, and an n-input NOR gate will have `n+1` terminals. We access these terminals with string keys, which are defined in the constructor of the `_CircuitElementTemplate` subclass.
### Subclass `__init__` definition
In the definition of `__init__` in any `_CircuitElementTemplate` subclass, a few guidelines need to be carefully followed. The `__init__` method **SHOULD NOT** add any geometries to the object, all geometry definitions should be made in the `generate_points` method. One can define the necessary points and geometries in the constructor, however they certainly should not be added to the VMobject in the constructor. This means no calls to any of the `_add_geom_` methods should be made in the constructor. One option, if the geometries must be defined in the constructor (usually needed for terminal coordinates), is to define the geometries and store them as properties of `self`, and add these geometries to `self` using the appropriate methods in `generate_points`.

Additionally, within this definition the `_CircuitElementTemplate.__init__` method must be called, and must be passed `self` as a parameter, as well as a dictionary of string keys, each indexing the coordinate of its respective Terminal, relative to the definition of the circuit element. For example, for the `Resistor` circuit element, it has a terminal labeled `'left'` located on the left-most vertex of the resistor geometry definition, and another terminal labeled `'right'` located on the right-most vertex of the resistor geometry definition. 

One final important note, is to include `**kwargs` in the parameter list for `__init__` and pass it through to the `_CircuitElementTemplate.__init__` call.
### Subclass `generate_points` definition
Any subclass of `_CircuitElementTemplate` must override the `generate_points` method of VMobject, in which one adds the geometries of the circuit element to the VMobject so that manim can render the object using a vectorized Bezier curve definition. To understand more details about how this works and how one can add geometries to a VMobject, refer to the community [Tutorials & Guides](https://docs.manim.community/en/stable/tutorials_guides.html) page, and carefully study the [VMobject](https://docs.manim.community/en/stable/reference/manim.mobject.types.vectorized_mobject.VMobject.html#manim.mobject.types.vectorized_mobject.VMobject) documentation. Writing this method effectively can be very technically challenging, it may even be useful to dive into the source code of VMobjects to get a lower level understanding of the system.
## Miscellaneous Circuit Element Guidelines
1) If you are adding a Circuit Element which has a common, or abstractable geometry, add an `_add_geom_` method to the `_CircuitElementTemplate` definition to generalize the geometry and make it reusable for future elements. This is especially important for complex geometries that may be difficult to replicate or approximate with Bezier curves. Before adding a geometry to a new circuit element or defining a new `_add_geom_` method, check the current methods to see if your new abstraction is very similar to, or easily replicated by a pre-existing `_add_geom_` method. If so, attempt to define the same geometry using the pre-existing methods, but if an abstraction seems simple, useful, and scalable, then you may consider adding it.
2) All circuit elements should be built such that their default geometries (meaning no transformations or additional formatting is applied) appear visually reasonable in terms of their relative scale. The default geometries should be able to construct a circuit which looks reasonably sized when connected, without any elements looking out of place or unnatural. There is no objective way to measure this, so use best judgement and reasonable critical thinking.