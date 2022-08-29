import numpy as np, scipy as sp, itertools as it
from pulp import *
import pandas as pd
import os, sys, csv, time
from scipy import optimize as spo
import multiprocessing as mp


def title(fl, t, au="", d=""):
	"""
	Standard latex title format

	TODO: finish docstring, change function name

	:param fl: _description_
	:type fl: _type_
	:param t: _description_
	:type t: _type_
	:param au: _description_
	:type au: _type_
	:param d: _description_, defaults to ""
	:type d: str, optional
	"""

	fl.write("\\title{"+ t + "}\n")
	fl.write("\\author{"+ au + "}\n")
	fl.write("\\date{"+ d + "}\r\n")


def package(fl, p, set=None):
	"""
	Standard format to include latex packages

	TODO: finish docstring, change function name

	:param fl: _description_
	:type fl: _type_
	:param p: _description_
	:type p: _type_
	:param set: _description_, defaults to None
	:type set: _type_, optional
	"""

	towrite = "\\usepackage"

	if(set != None):
		towrite = towrite + "[" + set + "]"
	towrite = towrite + "{" + p + "}\n"
	fl.write(towrite)


def stdSetup(fl, set=None):
	"""
	TODO: Add method description

	TODO: finish docstring, change function name

	:param fl: _description_
	:type fl: _type_
	:param set: _description_, defaults to None
	:type set: _type_, optional
	"""
	
	towrite = "\\documentclass"
	
	if(set != None):
		towrite = towrite + "[" + set + "]"
	
	towrite = towrite + "{article}\r\n"
	fl.write(towrite)
	
	package(fl,"inputenc",set="utf8")
	package(fl,"graphicx")
	package(fl,"physics")
	package(fl,"mathtools")
	package(fl,"amsmath")
	package(fl,"bbold")
	package(fl,"geometry")
	package(fl,"hyperref",set="pdftex,colorlinks=true")
