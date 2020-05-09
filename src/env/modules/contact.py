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

from modules.function import distance
from modules.function import line_func
from modules.function import polar2xy
from modules.function import line_intersection
from modules.function import circle_intersection


class Contact():
    def __init__(self, obj1, obj2, color='red'):
        self.obj1 = obj1
        self.obj2 = obj2
        self.isContact = False
        self.intersection_x = 0
        self.intersection_y = 0
        self.color = color
        
    def set_color(self, color):
        self.color = color
        
    def check_contact(self):
        if self.obj1.type is 'ball' and self.obj2.type is 'ball':
            d = distance(self.obj1.x,self.obj1.y,self.obj2.x,self.obj2.y)
            r1 = self.obj1.r
            r2 = self.obj2.r
            if r1 + r2 < d:
                self.intersection_x, self.intersection_y = circle_intersection(x1=self.obj1.x, y1=self.obj1.y, r1=r1, x2=self.obj2.x, y2=self.obj2.y, r2=r2, d=d)
                self.isContact = True
                return True
            else:
                self.isContact = False
                return False
        
        elif self.obj1.type is 'box' and self.obj2.type is 'box':
            vtx11x, vtx11y = polar2xy(r=self.obj1.w, theta=self.obj1.theta, x=self.obj1.x, y=self.obj1.y)
            vtx12x, vtx12y = polar2xy(r=self.obj1.w, theta=np.pi+self.obj1.theta, x=self.obj1.x, y=self.obj1.y)
            vtx21x, vtx21y = polar2xy(r=self.obj2.w, theta=self.obj2.theta, x=self.obj2.x, y=self.obj2.y)
            vtx22x, vtx22y = polar2xy(r=self.obj2.w, theta=np.pi+self.obj2.theta, x=self.obj2.x, y=self.obj2.y)
            # the centor line of box
            a1, b1, c1, line1 = line_func(vtx11x, vtx11y, vtx12x, vtx12y)
            a2, b2, c2, line2 = line_func(vtx21x, vtx21y, vtx22x, vtx22y)
            if line1(vtx21x, vtx21y) * line1(vtx22x, vtx22y) < 0 and line2(vtx11x, vtx11y) * line2(vtx12x, vtx12y) < 0:
                self.intersection_x, self.intersection_y = line_intersection(a1, b1, c1, a2, b2, c2)
                self.isContact = True
                return True
            else:
                self.isContact = False
                return False
            
        elif self.obj1.type is 'box' and self.obj2.type is 'ball':
            vtx11x, vtx11y = polar2xy(r=self.obj1.w, theta=self.obj1.theta, x=self.obj1.x, y=self.obj1.y)
            vtx12x, vtx12y = polar2xy(r=self.obj1.w, theta=np.pi+self.obj1.theta, x=self.obj1.x, y=self.obj1.y)
            x2 = self.obj2.x
            y2 = self.obj2.y
            a1, b1, c1, line1 = line_func(vtx11x, vtx11y, vtx12x, vtx12y)
            h = line1(x2, y2)/np.sqrt(a1**2+b1**2)
            d1 = distance(vtx11x,vtx11y,x2,y2)
            d2 = distance(vtx12x,vtx12y,x2,y2)
            if np.min([h,d1,d2]) < self.obj2.r:
                if h < np.min(d1,d2):
                    self.intersection_x, self.intersection_y = line_intersection(a1, b1, c1, b1, -a1, -b1*x2+a1*y2)
                elif d1 < d2:
                    self.intersection_x, self.intersection_y = vtx11x, vtx11y
                else:
                    self.intersection_x, self.intersection_y = vtx12x, vtx12y
                self.isContact = True
                return True
            else:
                self.isContact = False
                return False
            
        elif self.obj1.type is 'ball' and self.obj2.type is 'box':
            vtx21x, vtx21y = polar2xy(r=self.obj2.w, theta=self.obj2.theta, x=self.obj2.x, y=self.obj2.y)
            vtx22x, vtx22y = polar2xy(r=self.obj2.w, theta=np.pi+self.obj2.theta, x=self.obj2.x, y=self.obj2.y)
            x1 = self.obj1.x
            y1 = self.obj1.y
            a2, b2, c2, line2 = line_func(vtx21x, vtx21y, vtx22x, vtx22y)
            h = line2(x1, y1)/np.sqrt(a2**2+b2**2)
            d1 = distance(vtx21x,vtx21y,x1,y1)
            d2 = distance(vtx22x,vtx22y,x1,y1)
            if np.min([h,d1,d2]) < self.obj1.r:
                if h < np.min(d1,d2):
                    self.intersection_x, self.intersection_y = line_intersection(a2, b2, c2, b2, -a2, -b2*x1+a2*y1)
                elif d1 < d2:
                    self.intersection_x, self.intersection_y = vtx21x, vtx21y
                else:
                    self.intersection_x, self.intersection_y = vtx22x, vtx22y
                self.isContact = True
                return True
            else:
                self.isContact = False
                return False
            
    def step(self):
        self.check_contact()


class Contact_Penalty(Contact):
    def __init__(self, obj1, obj2, k=0, c=10, color='red'):
        super().__init__(obj1=obj1, obj2=obj2, color=color)
        self.k = k
        self.c = c
    
    def add_force(self, obj):
        if obj.type is 'ball':
            d = distance(obj.x,obj.y,self.intersection_x,self.intersection_y)
            Fx = self.k*(obj.r-d)*(obj.x-self.intersection_x)/d
            Fx = self.k*(obj.r-d)*(obj.y-self.intersection_y)/d
            obj.add_force(Fx, Fy, 0)
    
    def step(self):
        if self.check_contact():
            self.add_force(self.obj1)
            self.add_force(self.obj2)






