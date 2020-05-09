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

# %matplotlib nbagg

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as pat

from modules.environment import Environment
from modules.obj import Ball, Box
from modules.contact import Contact, Contact_Penalty

fig = plt.figure()
ax = fig.add_subplot(111)

tabletennis = Environment(ax=ax)
ball = Ball(r=0.20, M=0.0027, color='orange')
table = Box(w=2.74, h=0.01, x=0, y=0, fix=True, color='blue')
net = Box(w=0.15, h=0.01, x=0, y=0.075, theta=np.pi/2, fix=True, color='gray')

ball.set_position(0,1,0)

tabletennis.add_obj(table)

tabletennis.add_obj(net)

tabletennis.add_obj(ball)

#tabletennis.add_contact(Contact(net,ball))
tabletennis.add_contact(Contact_Penalty(table,ball))

ani = animation.FuncAnimation(fig, tabletennis.step, interval=10, frames=3000, repeat=True)
plt.show()

np.pi

np.cos(np.pi)


