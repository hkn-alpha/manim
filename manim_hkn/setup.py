from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'HKN Manim wrapper package for animation of ECE Review videos'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="manim_hkn", 
        version=VERSION,
        author="Eta Kappa Nu | Alpha",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=['manim'],

        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)