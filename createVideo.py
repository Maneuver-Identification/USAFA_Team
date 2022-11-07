#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bpy,sys
from pathlib import Path
from math import radians

#obtains command line arguments
for i in range(len(sys.argv)):
    arg = sys.argv[i]
    if arg == "--":
        args = sys.argv[i+1:]

#clears plane animation
plane = bpy.data.objects["Plane"]
plane.animation_data_clear()

#Open Flight Path
tsv  = open(args[0], "r")
tsv  = open(args[0], "r")

#Reads first line of file
A = tsv.readline()
B = [float(x) for x in A.split('\t') if x.strip()]

#tracks the frame and time segments added
frame_num = 1
prev_time = 0

#sets the inital location of the plane and camera, and sets a keyframe for both
plane.location = (0,0,0)
plane.rotation_euler = (radians(B[10]+90), radians(-B[9]), radians(-B[8] + 90))
plane.location  = (B[2], B[3], B[4])
plane.keyframe_insert(data_path = "location", frame = frame_num)
plane.keyframe_insert(data_path = "rotation_euler", frame = frame_num)

for line in tsv:
    B = [float(x) for x in line.split('\t') if x.strip()]
    if not int(B[1]) == prev_time:
        #Update time
        frame_num = int(B[1]) * 24
        prev_time = int(B[1])
        
        #Move to origin, apply rotation, and move to desired point
        plane.location = (0,0,0)
        plane.rotation_euler = (radians((B[10] + 90)), radians((-B[9])), radians((-B[8] + 90)))
        plane.location  = (B[2], B[3], B[4])
        plane.keyframe_insert(data_path = "location", frame = frame_num)
        plane.keyframe_insert(data_path = "rotation_euler", frame = frame_num)
        
tsv.close()

#set camera
bpy.data.scenes["Scene"].camera = bpy.data.objects[args[2]]
bpy.data.scenes["Scene"].render.filepath = args[1] + args[0].split("/")[-1].split(".")[0] +args[2] + ".avi"


for area in bpy.context.screen.areas: 
    if area.type == 'VIEW_3D':
        for space in area.spaces: 
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'
bpy.ops.render.opengl(animation=True)
bpy.ops.wm.quit_blender()


# In[ ]:




