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

from function import distance
from function import line_func
from function import polar2xy
from function import line_intersection
from function import circle_intersection
from function import get_outside_boxes
from function import is_in_box


class Contact():
    def __init__(self, obj1, obj2, color='red'):
        self.obj1 = obj1
        self.obj2 = obj2
        self.isContact = False
        self.intersection_x = 0
        self.intersection_y = 0
        self.color = color
        self.refractory_period = 5
        self.counter = 0
        
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
            
        else:
            if self.obj1.type is 'box' and self.obj2.type is 'ball':
                x = self.obj1.x
                y = self.obj1.y
                theta = self.obj1.theta
                w = self.obj1.w
                h = self.obj1.h
                c_x = self.obj2.x
                c_y = self.obj2.y
                r = self.obj2.r
            elif self.obj1.type is 'ball' and self.obj2.type is 'box':
                x = self.obj2.x
                y = self.obj2.y
                theta = self.obj2.theta
                w = self.obj2.w
                h = self.obj2.h
                c_x = self.obj1.x
                c_y = self.obj1.y
                r = self.obj1.r
                
            box, out_boxes = get_outside_boxes(x,y,theta,w,h,r)
            
            if is_in_box(c_x, c_y, box):
                a1, b1, c1, line1 = line_func(box[0][0],box[0][1],box[1][0],box[1][1])
                a2, b2, c2, line2 = line_func(box[1][0],box[1][1],box[2][0],box[2][1])
                a3, b3, c3, line3 = line_func(box[2][0],box[2][1],box[3][0],box[3][1])
                a4, b4, c4, line4 = line_func(box[3][0],box[3][1],box[0][0],box[0][1])
                a = [a1, a2, a3, a4]
                b = [b1, b2, b3, b4]
                c = [c1, c2, c3, c4]
                line = [line1, line2, line3, line4]
                d = []
                for i in range(4):
                    d.append(np.abs(line[i](c_x, c_y))/np.sqrt(a[i]**2+b[i]**2))
                idx = np.argmin(d)
                self.intersection_x, self.intersection_y = line_intersection(a[idx], b[idx], c[idx], b[idx], -a[idx], -b[idx]*c_x+a[idx]*c_y)
                self.isContact = True
                return True
            
            else:
                for out_box in out_boxes:
                    if is_in_box(c_x, c_y, out_box):
                        a, b, c, line = line_func(out_box[0][0],out_box[0][1],out_box[1][0],out_box[1][1])
                        self.intersection_x, self.intersection_y = line_intersection(a, b, c, b, -a, -b*c_x+a*c_y)
                        self.isContact = True
                        return True
                    
                for vtx in box:
                    if distance(c_x, c_y, vtx[0], vtx[1]) < r:
                        self.intersection_x, self.intersection_y = vtx[0], vtx[1]
                        self.isContact = True
                        return True
               
                self.isContact = False
                return False
            
    def step(self):
        self.check_contact()


class Contact_Penalty(Contact):
    def __init__(self, obj1, obj2, k=10, c=1, color='red'):
        super().__init__(obj1=obj1, obj2=obj2, color=color)
        self.k = k
        self.c = c
    
    def add_force(self, obj):
        if obj.type is 'ball':
            d = distance(obj.x,obj.y,self.intersection_x,self.intersection_y)
            Fx = self.k*(obj.r-d)*(obj.x-self.intersection_x)/d
            Fy = self.k*(obj.r-d)*(obj.y-self.intersection_y)/d
            obj.add_force(Fx, Fy, 0)
    
    def step(self):
        self.counter += 1
        if self.counter > self.refractory_period:
            if self.check_contact():
                self.add_force(self.obj1)
                self.add_force(self.obj2)
                self.counter = 0


class Contact_ball_table(Contact):
    def __init__(self, obj1, obj2, et=0.93, u=0.25, color='red'):
        super().__init__(obj1=obj1, obj2=obj2, color=color)
        self.et = et
        self.u = u
    def step(self):
        self.counter += 1
        if self.counter > self.refractory_period:
            if self.check_contact():
                # obj1 should be a ball
                vbt = self.obj1.v_x + self.obj1.r * self.obj1.v_theta
                print(vbt)
                vs = 1 - 2.0/5.0 * self.u *(1+self.et)*abs(self.obj1.v_y/(vbt+1e-7))
                if vs > 0:
                    alpha = self.u*(1*self.et)*abs(self.obj1.v_y/(vbt+1e-7))
                else:
                    alpha = 2.0/5.0
                self.obj1.v_x = (1-alpha)*self.obj1.v_x-alpha*self.obj1.r*self.obj1.v_theta
                self.obj1.v_y = - self.et*self.obj1.v_y
                self.obj1.v_theta = -3.0/2.0*alpha/self.obj1.r*self.obj1.v_x+(1-3.0/2.0*alpha)*self.obj1.v_theta
                self.counter = 0


class Contact_ball_racket(Contact):
    def __init__(self, obj1, obj2, er=0.81, kp=0.0019, color='red'):
        super().__init__(obj1=obj1, obj2=obj2, color=color)
        self.er = er
        self.kp = kp
        self.kv = self.kp/self.obj1.M
        self.kw = self.kp/self.obj1.I
    def step(self):
        self.counter += 1
        if self.counter > self.refractory_period:
            if self.check_contact():
                # rotate
                vr_x = np.cos(self.obj2.theta)*self.obj1.v_x+np.sin(self.obj2.theta)*self.obj1.v_y
                vr_y = -np.sin(self.obj2.theta)*self.obj1.v_x+np.cos(self.obj2.theta)*self.obj1.v_y
                # reflect
                self.obj1.v_theta = -self.kw*self.obj1.r*vr_x*(1-self.kw*self.obj1.r**2)*self.obj1.v_theta
                vr_x = (1-self.kv)*vr_x-self.kv*self.obj1.r*self.obj1.v_theta
                vr_y = -self.er*vr_y
                # rotate
                self.obj1.v_x = np.cos(self.obj2.theta)*vr_x-np.sin(self.obj2.theta)*vr_y
                self.obj1.v_y = np.sin(self.obj2.theta)*vr_x+np.cos(self.obj2.theta)*vr_y
                self.counter = 0
