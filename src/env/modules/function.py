# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import numpy as np
import math


def distance(x1, y1, x2, y2):
    return np.sqrt((x1-x2)**2+(y1-y2)**2)


def line_func(x1, y1, x2, y2):
    a = y1-y2
    b = x1-x2
    c = -(y1-y2)*x1+(x1-x2)*y1
    def func(x,y):
        return a*x+b*y+c
    return a, b, c, func


def line_intersection(a1, b1, c1, a2, b2, c2):
    x = (b2*c1-b1*c2)/(a1*b2-a2*b1)
    y = (-a2*c1+a1*c2)/(a1*b2-a2*b1)
    return x, y


def circle_intersection(x1,y1,r1,x2,y2,r2,d):
    k = (r1**2-r2**2+d**2)/(2*d)
    x = x1+(x2-x1)*k/d
    y = y1+(y2-y1)*k/d
    return x, y


def polar2xy(r, theta, x=0, y=0):
    return r*np.sin(theta)+x, r*np.cos(theta)+y


def plot_rectangular(x, y, theta, w, h):
    vtx1x = w/2*np.cos(theta) - h/2*np.sin(theta) + x
    vtx1y = w/2*np.sin(theta) + h/2*np.cos(theta) + y
    vtx2x = - w/2*np.cos(theta) - h/2*np.sin(theta) + x
    vtx2y = - w/2*np.sin(theta) + h/2*np.cos(theta) + y
    vtx3x = - w/2*np.cos(theta) + h/2*np.sin(theta) + x
    vtx3y = - w/2*np.sin(theta) - h/2*np.cos(theta) + y
    vtx4x = w/2*np.cos(theta) + h/2*np.sin(theta) + x
    vtx4y = w/2*np.sin(theta) - h/2*np.cos(theta) + y
    return [[vtx1x,vtx2x,vtx3x,vtx4x], [vtx1y,vtx2y,vtx3y,vtx4y]]


def plot_circle(x, y, r, division=12):
    x = [x]
    y = [y]
    for i in range(division):
        x.append(x+r*np.cos(2*np.pi*i/division))
        y.append(y+r*np.sin(2*np.pi*i/division))
    return [x, y]


