import numpy as np, scipy as sp, itertools as it
from pulp import *
import pandas as pd
import os, sys, csv, time
from scipy import optimize as spo
import multiprocessing as mp
import latexSetup

WListRaw = "WList.csv"
LocRaw = "LocList.csv"
