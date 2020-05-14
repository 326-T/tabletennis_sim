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


class Air_resistance_ball:
    def __init__(self, obj, Cd=0.54, Cm=0.069, po=1.184):
        self.obj = obj
        self.Cd = Cd
        self.Cm = Cm
        self.po = po
        self.A = np.pi*self.obj.r**2
        self.coef = 1.0/2.0*self.Cd*self.po*self.A
        self.drag = 4.0/3.0*self.Cm*np.pi*self.po*self.obj.r**3
        
    def step(self):
        v = np.sqrt(self.obj.v_x**2+self.obj.v_y**2)
        Rx = -self.coef*v*self.obj.v_x-self.drag*self.obj.v_theta*self.obj.v_y
        Ry = -self.coef*v*self.obj.v_y+self.drag*self.obj.v_theta*self.obj.v_x
        self.obj.add_force(Rx, Ry, 0)
