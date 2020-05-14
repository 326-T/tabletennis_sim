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


class Obj():
    def __init__(self, x=0, y=0, theta=0, M=1, I=1, fix=False, color='black'):
        # position
        self.x = x
        self.y = y
        self.theta = theta
        # fixed object or not
        self.fix = fix
        # velocity
        self.v_x = 0
        self.v_y = 0
        self.v_theta = 0
        # acceleration
        self.a_x = 0
        self.a_y = 0
        self.a_theta = 0
        # mass, inertial mass
        self.M = M
        self.I = 0
        # color for plot
        self.color=color
        self.img = None
        
    def set_position(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        
    def set_velocity(self, v_x, v_y, v_theta):
        self.v_x = v_x
        self.v_y = v_y
        self.v_theta = v_theta
        
    def set_acceleration(self, a_x, a_y, a_theta):
        self.a_x = a_x
        self.a_y = a_y
        self.a_theta = a_theta
    
    def set_mass(self, M, I=None):
        self.M = M
        if I is not None:
            self.I = I
        
    def set_color(self, color):
        self.color = color
        
    def set_img(self, img):
        self.img, = img
        
    def set_fix(self, fix):
        self.fix = fix
    
    def add_force(self, F_x, F_y, Torque):
        self.a_x = self.a_x + F_x / self.M
        self.a_y = self.a_y + F_y / self.M
        self.a_theta = self.a_theta + Torque / self.I
        
    def step(self, dt):
        if self.fix is False:
            # update position
            self.x = self.x + self.v_x * dt
            self.y = self.y + self.v_y * dt
            self.theta = self.theta + self.v_theta * dt
            # update velocity
            self.v_x = self.v_x + self.a_x * dt
            self.v_y = self.v_y + self.a_y * dt
            self.v_theta = self.v_theta + self.a_theta * dt
            # reset acceleration
            self.a_x = 0
            self.a_y = 0
            self.a_theta = 0


# +
class Ball(Obj):
    def __init__(self, r, x=0, y=0, theta=0, M=1, I=1, fix=False, color='black'):
        super().__init__(x=x, y=y, theta=theta, M=M, I=I, fix=fix, color=color)
        self.r = r
        self.I = 2.0/3.0*self.M*self.r**2
        self.type = 'ball'
        
    def set_mass(self, M, I=None):
        super().__init__(M, I)
        if I is None:
            self.I = 2.0/3.0*M*self.r**2
        
class Box(Obj):
    def __init__(self, w, h=0, x=0, y=0, theta=0, M=1, I=1, fix=False, color='black'):
        super().__init__(x=x, y=y, theta=theta, M=M, I=I, fix=fix, color=color)
        self.w = w
        self.h = h
        self.I = 1.0/12.0*M*(self.w**2+self.h**2)
        self.type = 'box'
        
    def set_mass(self, M, I=None):
        super().__init__(M, I)
        if I is None:
            self.I = 1.0/12.0*M*(self.w**2+self.h**2)
            
    def plot(self):
        vtx3x = - self.w/2*np.cos(self.theta) + self.h/2*np.sin(self.theta) + self.x
        vtx3y = - self.w/2*np.sin(self.theta) - self.h/2*np.cos(self.theta) + self.y
        return (vtx3x, vtx3y)
            
# -


