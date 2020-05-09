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

class Obj():
    def __init__(self, x=0, y=0, theta=0, M=1, I=1):
        # position
        self.x = x
        self.y = y
        self.theta = theta
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
    
    def set_mass(self, M, I):
        self.M = M
        self.I = I
        
    def add_force(self, F_x, F_y, Torque):
        self.a_x = self.a_x + F_x / M
        self.a_y = self.a_y + F_y / M
        self.a_theta = self.a_theta + Torque / I
        
    def move(self, dt):
        # update position
        self.x = self.x + self.v_x * dt
        self.y = self.y + self.v_y * dt
        self.theta = self.theta + self.v_theta * dt
        # update velocity
        self.v_x = self.v_x + self.a_x * dt
        self.v_y = self.v_y + self.a_y * dt
        self.v_theta = self.v_theta + self.a_theta * dt


# +
class ball(Obj):
    def __init__(self, r, x=0, y=0, theta=0, M=1, I=1):
        super.__init__(self, x=0, y=0, theta=0, M=1, I=1)
        self.r = r
        self.type = 'ball'
        
class box(Obj):
    def __init__(self, w, h=0, x=0, y=0, theta=0, M=1, I=1):
        super.__init__(self, x=0, y=0, theta=0, M=1, I=1)
        self.w = w
        self.h = h
        self.type = 'box'
        
