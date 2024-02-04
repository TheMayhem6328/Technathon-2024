from setuptools import setup
from Cython.Build import cythonize

setup(
    name="Technathon 2024",
    version="1.0",
    author="Zahiruzzaman Chowdhury",
    author_email="2013060031@scholastica.online",
    packages=["pytrends", "pyarrow", "cython"],
    ext_modules = cythonize("Q1.pyx")
)

"python setup.py build_ext --inplace"