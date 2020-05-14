# -*- coding: utf-8 -*-
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
    b = -x1+x2
    c = -(y1-y2)*x1+(x1-x2)*y1
    def func(x,y):
        return a*x+b*y+c
    return a, b, c, func


def line_intersection(a1, b1, c1, a2, b2, c2):
    x = (-b2*c1+b1*c2)/(a1*b2-a2*b1)
    y = (a2*c1-a1*c2)/(a1*b2-a2*b1)
    return x, y


def circle_intersection(x1,y1,r1,x2,y2,r2,d):
    k = (r1**2-r2**2+d**2)/(2*d)
    x = x1+(x2-x1)*k/d
    y = y1+(y2-y1)*k/d
    return x, y


def polar2xy(r, theta, x=0, y=0):
    return r*np.cos(theta)+x, r*np.sin(theta)+y


def get_vertex(x, y, theta, w, h):
    vtx1x = w/2*np.cos(theta) - h/2*np.sin(theta) + x
    vtx1y = w/2*np.sin(theta) + h/2*np.cos(theta) + y
    vtx2x = - w/2*np.cos(theta) - h/2*np.sin(theta) + x
    vtx2y = - w/2*np.sin(theta) + h/2*np.cos(theta) + y
    vtx3x = - w/2*np.cos(theta) + h/2*np.sin(theta) + x
    vtx3y = - w/2*np.sin(theta) - h/2*np.cos(theta) + y
    vtx4x = w/2*np.cos(theta) + h/2*np.sin(theta) + x
    vtx4y = w/2*np.sin(theta) - h/2*np.cos(theta) + y
    return [[vtx1x,vtx1y], [vtx2x,vtx2y], [vtx3x,vtx3y], [vtx4x,vtx4y]]


def get_outside_boxes(x, y, theta, w, h, r):
    # 外接する長方形
    vtx11x = w/2*np.cos(theta) - h/2*np.sin(theta) + x
    vtx11y = w/2*np.sin(theta) + h/2*np.cos(theta) + y
    vtx12x = - w/2*np.cos(theta) - h/2*np.sin(theta) + x
    vtx12y = - w/2*np.sin(theta) + h/2*np.cos(theta) + y
    
    vtx13x = - w/2*np.cos(theta) - (h/2+r)*np.sin(theta) + x
    vtx13y = - w/2*np.sin(theta) + (h/2+r)*np.cos(theta) + y
    vtx14x = w/2*np.cos(theta) - (h/2+r)*np.sin(theta) + x
    vtx14y = w/2*np.sin(theta) + (h/2+r)*np.cos(theta) + y
    
    
    vtx21x = - w/2*np.cos(theta) - h/2*np.sin(theta) + x
    vtx21y = - w/2*np.sin(theta) + h/2*np.cos(theta) + y
    vtx22x = - w/2*np.cos(theta) + h/2*np.sin(theta) + x
    vtx22y = - w/2*np.sin(theta) - h/2*np.cos(theta) + y
    
    vtx23x = - (w/2+r)*np.cos(theta) + h/2*np.sin(theta) + x
    vtx23y = - (w/2+r)*np.sin(theta) - h/2*np.cos(theta) + y
    vtx24x = - (w/2+r)*np.cos(theta) - h/2*np.sin(theta) + x
    vtx24y = - (w/2+r)*np.sin(theta) + h/2*np.cos(theta) + y
    
    
    vtx31x = - w/2*np.cos(theta) + h/2*np.sin(theta) + x
    vtx31y = - w/2*np.sin(theta) - h/2*np.cos(theta) + y
    vtx32x = w/2*np.cos(theta) + h/2*np.sin(theta) + x
    vtx32y = w/2*np.sin(theta) - h/2*np.cos(theta) + y
    
    vtx33x = w/2*np.cos(theta) + (h/2+r)*np.sin(theta) + x
    vtx33y = w/2*np.sin(theta) - (h/2+r)*np.cos(theta) + y
    vtx34x = - w/2*np.cos(theta) + (h/2+r)*np.sin(theta) + x
    vtx34y = - w/2*np.sin(theta) - (h/2+r)*np.cos(theta) + y
    
    
    vtx41x = w/2*np.cos(theta) + h/2*np.sin(theta) + x
    vtx41y = w/2*np.sin(theta) - h/2*np.cos(theta) + y
    vtx42x = w/2*np.cos(theta) - h/2*np.sin(theta) + x
    vtx42y = w/2*np.sin(theta) + h/2*np.cos(theta) + y
    
    vtx43x = (w/2+r)*np.cos(theta) - h/2*np.sin(theta) + x
    vtx43y = (w/2+r)*np.sin(theta) + h/2*np.cos(theta) + y
    vtx44x = (w/2+r)*np.cos(theta) + h/2*np.sin(theta) + x
    vtx44y = (w/2+r)*np.sin(theta) - h/2*np.cos(theta) + y
    
    return get_vertex(x,y,theta,w,h), [[[vtx11x,vtx11y], [vtx12x,vtx12y], [vtx13x,vtx13y], [vtx14x,vtx14y]],
                                       [[vtx21x,vtx21y], [vtx22x,vtx22y], [vtx23x,vtx23y], [vtx24x,vtx24y]],
                                       [[vtx31x,vtx31y], [vtx32x,vtx32y], [vtx33x,vtx33y], [vtx34x,vtx34y]],
                                       [[vtx41x,vtx41y], [vtx42x,vtx42y], [vtx43x,vtx43y], [vtx44x,vtx44y]]]


def is_in_box(x, y, box_vertex):
    a1, b1, c1, line1 = line_func(box_vertex[0][0],box_vertex[0][1],box_vertex[1][0],box_vertex[1][1])
    a2, b2, c2, line2 = line_func(box_vertex[1][0],box_vertex[1][1],box_vertex[2][0],box_vertex[2][1])
    a3, b3, c3, line3 = line_func(box_vertex[2][0],box_vertex[2][1],box_vertex[3][0],box_vertex[3][1])
    a4, b4, c4, line4 = line_func(box_vertex[3][0],box_vertex[3][1],box_vertex[0][0],box_vertex[0][1])
    a = [a1, a2, a3, a4]
    b = [b1, b2, b3, b4]
    c = [c1, c2, c3, c4]
    line = [line1, line2, line3, line4]
    if line1(x,y)*line3(x,y) > 0 and line2(x,y)*line4(x,y) > 0:
        return True
    else:
        return False


box=[[2,2],[-2,1],[-1,-3],[3,-2]]
is_in_box(-1,-2,box)

line_intersection(1,-1,-1,1,2,-4)

line_intersection(1,2,-4,1,-1,-1)

a1=1
b1=-1
c1=-1
x2=2
y2=2
line_intersection(a1, b1, c1, b1, -a1, -b1*x2+a1*y2)

a1=0
b1=1
c1=0
x2=2
y2=2
line_intersection(a1, b1, c1, b1, -a1, -b1*x2+a1*y2)

_,_,_,a=line_func(1,-1,2,2)

a(1,-1)

get_vertex(2,2,np.pi/4,2,2)

get_outside_boxes(0,0,0,4,2,1)


