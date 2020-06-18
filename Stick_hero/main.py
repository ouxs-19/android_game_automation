#!/usr/bin/python3

from ppadb.client import Client as adb_client
import numpy
from PIL import Image 
from time import sleep
client=adb_client(host='127.0.0.1',port=5037)
devices=client.devices()

if len(devices)==0:
	print("No device found")
	exit()
my_device=devices[0]
count = 1 
eat_fruit = False #set this to True if you want to eat frui but it doesn't work well yet
while True : 
	situaton=result = my_device.screencap()
	start_check=False
	edge_check=False
	end_point_check=False
	start_point=0


	with open("screen.png", "wb") as fp:
	    fp.write(situaton)

	img=Image.open("screen.png")
	data=numpy.array(img)
	screen_pixels= [px[:3] for px in data[int(len(data)*0.8)]]

	for  ind , px in enumerate(screen_pixels):
		if sum(px)+start_point==0:
			start_check=True

		if start_check and sum(px)!=0:
			start_point=ind
			start_check=False


		if start_point!=0 and sum(px)==0 and not edge_check:
			edge=ind
			edge_check=True
			end_point_check=True
		if end_point_check and sum(px)!=0:
			end_point=ind
			break
	half_edge=(end_point-edge)/2
	jump_dist=int(((edge-start_point)+half_edge*0.97))
	
	print("Jump number : {} and about to jump {} m ".format(count,jump_dist))
	count+=1

	my_device.shell('input touchscreen swipe 500 500 500 500 {}'.format(jump_dist))
	if jump_dist > 570 and eat_fruit:		
		pass
		sleep(jump_dist/1500)
		my_device.shell('input tap 500 500')
		time_to_sleep=((jump_dist/1000)-0.04-(half_edge/1000))*0.965
		sleep(time_to_sleep)
		my_device.shell('input tap 500 500')

	sleep(2.5)