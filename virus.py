import numpy as np
from pylab import *
import copy as cp
import random
import math
from PIL import Image, ImageDraw
import os


N_total = 500			#total number of persons
N_sick = 2 			#initial number of infected
infect_radius = 0.0001		#maximum distance at which virus is transmitted
m = 0.01 			#distance moved during iteration 
soc_dist = 0.5 			#ratio of people obeying social distancing, 0 = none and at 1 all are static
virus_deathrate = 0.1		#probability of death once infected
iterations = 500		#simulation iterations
movement_fact = 9		#iterations in a day
frame_dur = 0.05		#duration of one frame of the final .gif

class person:
	pass
	
def initialize():
	global population
	population = []

	for i in range(N_total):
		per = person()
		per.id = i
		per.timer = 0 	#used to track the time after infenction
		per.update = '' #indicates the status update for the next iteration
		
		per.day_h = movement_fact * max(10, math.trunc(random.gauss(11, 5))) #if agent gets infected, gives the day at which he recovers
		per.day_x = 0
		
		if random.random() <= virus_deathrate: #based on the given deathrate, decides if agent will die or not
			per.day_x =  movement_fact * max(4, math.trunc(random.gauss(10, 4))) #decides on which day the agent will die
		
		per.angle = 2*math.pi * random.random() #initial spacial orientation of the agent, in radians
		
		if i < (N_total - N_sick):
			per.stat = 'healthy'  #the inital healthy agents
		else: 
			per.stat = 'sick' #the initial sick agents

		if i >= (N_total * soc_dist):  #decides if the agent is obeying social distancing or not
			per.social = 1 #socializing
		else:
			per.social = 0 #stays home

		per.x = random.random() #random seed for agent on x space
		per.y = random.random()	#random seed for agent on y space
		population.append(per)  #creating the agent space

def observe():
	#subplot(1, 2, 1)
	cla()
	for per in population:
		if per.stat == 'sick':
			if (per.day_x > 0) and (per.timer == per.day_x): #if person sick and will die, this keeps track of the day of death
				per.stat = 'dead'
				per.social = 0
			elif (per.day_x == 0) and (per.timer == per.day_h):	#if person sick and will recover, this keeps track of the day of recovering
				per.stat = 'recovered'
			per.timer += 1 #time tracker

		if per.update != '': #checks if person was infected in last step
			per.stat = per.update
			per.update = ''
			
	x_healthy = [per.x for per in population if per.stat == 'healthy']
	y_healthy = [per.y for per in population if per.stat == 'healthy']

	x_sick = [per.x for per in population if per.stat == 'sick']
	y_sick = [per.y for per in population if per.stat == 'sick']

	x_dead = [per.x for per in population if per.stat == 'dead']
	y_dead = [per.y for per in population if per.stat == 'dead']

	x_recovered = [per.x for per in population if per.stat == 'recovered']
	y_recovered = [per.y for per in population if per.stat == 'recovered']

	plot(x_healthy, y_healthy, 'go')
	plot(x_dead, y_dead, 'kx')
	plot(x_sick, y_sick, 'ro')
	plot(x_recovered, y_recovered, 'bo')
	print(len(x_healthy), len(x_sick), len(x_recovered), len(x_dead))

	axis('image')
	axis([0, 1, 0, 1])
	#subplot(1, 2, 2)
	#cla()
	#plot(len(population), label='population')
	title('interval ' + str(t))
	savefig('interval ' + str(t) + '.png')

def update():
	for per in population:
		if per.stat == 'healthy':
			proximity = [nb for nb in population if ((per.x - nb.x)**2 + (per.y - nb.y)**2 < infect_radius) and (nb.stat == 'sick')]
			if len(proximity) > 0:
				per.update = 'sick'
	for per in population:
		if (per.social == 1):
			per.x += m*math.cos(per.angle)
			per.y += m*math.sin(per.angle)
		if (per.x >= 1) or (per.x <= 0):
			per.angle = math.pi - per.angle
		elif (per.y >= 1) or (per.y <= 0):
			per.angle = -1 * per.angle


t = 0
initialize()
observe()

for t in range(1, iterations):
    update()
    observe()

frames = []
for i in range(iterations):
	img = Image.open('interval '+str(i)+'.png')
	frames.append(img)
frames[0].save('simulation.gif', format='GIF', append_images=frames[1:], save_all=True, duration=frame_dur, loop=0)
for i in range(iterations):
	os.remove('interval '+str(i)+'.png') 
