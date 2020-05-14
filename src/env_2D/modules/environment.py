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
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as pat


# +
# without rendering
class Environment_without_rendering():
    def __init__(self):
        self.obj = []
        self.contact = []
        self.air_resistance = []
        self.g_x = 0
        self.g_y = - 9.8
    
    def set_gravity(self, g_x, g_y):
        self.g_x = g_x
        self.g_y = g_y
    
    def add_obj(self, new_obj):
        self.obj.append(new_obj)
        
    def add_contact(self, new_contact):
        self.contact.append(new_contact)
        
    def add_air_resistance(self, new_air_resistance):
        self.air_resistance.append(new_air_resistance)
        
    def step(self, dt):
        # calcurate contact
        for contact in self.contact:
            contact.step()
        # add gravity
        for obj in self.obj:
            obj.add_force(obj.M*self.g_x, obj.M*self.g_y, 0)
        # add air resistance
        for air_res in self.air_resistance:
            air_res.step()
        # move
        for obj in self.obj:
            obj.step(dt)
            
class Environment(Environment_without_rendering):

    def __init__(self, ax, dt=0.00001, fps = 1000):
        super().__init__()
        self.images = []
        self.ax = ax
        self.dt = dt
        self.fps = fps

    def render(self, i):
        for i in range(int(1/self.dt/self.fps)):
            self.step(self.dt)
        # rendering
        plt.cla()
        self.ax.set_xlim(-2,2)
        self.ax.set_ylim(-0.5,2)
        for obj in self.obj:
            if obj.type is 'box':
                self.ax.add_patch(pat.Rectangle(xy=obj.plot(), width=obj.w, height=obj.h, angle=obj.theta/np.pi*180, color=obj.color, alpha=0.5))
            if obj.type is 'ball':
                self.ax.add_patch(pat.Circle(xy=(obj.x,obj.y), radius=obj.r*2, color=obj.color, alpha=0.5))
                self.ax.scatter(obj.x+obj.r*np.cos(obj.theta), obj.y+obj.r*np.sin(obj.theta), color = 'black', s=5)
        for contact in self.contact:
            if contact.isContact is True:
                self.ax.scatter(contact.intersection_x, contact.intersection_y, color=contact.color, s=5)







# -

