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

from environment import Environment, Environment_without_rendering
from obj import Ball, Box
from contact import Contact, Contact_Penalty, Contact_ball_table, Contact_ball_racket
from air_resistance import Air_resistance_ball

# +
fig = plt.figure()
ax = fig.add_subplot(111)
tabletennis = Environment(ax=ax)
#tabletennis = Environment_without_rendering()

ball = Ball(r=0.02, M=0.0027, color='orange')
table = Box(w=2.74, h=0.20, x=0, y=-0.10, fix=True, color='blue')
net = Box(w=0.15, h=0.01, x=0, y=0.075, theta=np.pi/2, fix=True, color='gray')
racket = Box(w=0.2, h=0.01, x=1.5, y=0.20, theta=np.pi/2, color='red', fix=True)

ball.set_position(-1.5,0.3,0)
ball.set_velocity(10.0, 1.0, -50*np.pi)

tabletennis.add_obj(table)
tabletennis.add_obj(net)
tabletennis.add_obj(ball)
tabletennis.add_obj(racket)

tabletennis.add_contact(Contact_Penalty(net,ball))
tabletennis.add_contact(Contact_ball_table(ball,table))
tabletennis.add_contact(Contact_ball_racket(ball,racket))

tabletennis.add_air_resistance(Air_resistance_ball(ball))

ani = animation.FuncAnimation(fig, tabletennis.render, interval=1, frames=1000)
plt.show()
# -

ani.save("topspin.mp4", writer="ffmpeg", fps=100)
