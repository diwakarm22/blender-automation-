
import os
import os.path
import sys
from time import *
import runpy
import bpy
import json
from mathutils import *
from math import *
from mathutils import Vector
import shutil

configuration_dict = {}
cwd = os.getcwd()



def read_json_config_file():
	global configuration_dict
	fd =  open("D:\Conti_Blender\Conti_Blender\Projects\Working_scripts\configuration_AU416.json")
	configuration_dict = json.loads(fd.read())

def move_files(src_folder, dest_folder, update_file_name):
	if os.listdir(src_folder) == os.listdir(dest_folder):
		return
	for i in os.listdir(src_folder):
		if i.endswith(".json"):
			temp = update_file_name + "_camera_positions.json"
		else:
			temp = update_file_name + "." + i.split(".")[-1]

		#shutil.copyfile(src_folder+i, dest_folder+temp)
	print("Copy File completed")

def move_files_rename_them():
	global configuration_dict

	# /home/uif34373/Conti_Blender/Projects/Fov_Studies
	folder_name = f"{configuration_dict['date_string']}_{configuration_dict['model_string']}"
	folder_path = f"{configuration_dict['brand_path']}{folder_name}"
	folder_path = f"../../Projects/{folder_path}/"
	if os.path.exists(folder_path):
		move_files(configuration_dict['model_path'], folder_path, folder_name)
	else:
		os.makedirs(folder_path)
		move_files(configuration_dict['model_path'], folder_path, folder_name)



try:
	read_json_config_file()
	basePath = configuration_dict['script_path']
	move_files_rename_them()


	fileGlobals = runpy.run_path(basePath + "0_setup_RK.py")
	globals().update(fileGlobals)

	# read variables from setup file
	# exec( open( "/home/test/Projects/03_Scripts/0_setup_RK.py").read(), globals())

		
	loggen( LogDat, screen_echo, "")
	loggen( LogDat, screen_echo, strftime( "Start posCam Step 1 %d.%m.%y %H:%M:%S", localtime()))
	loggen( LogDat, screen_echo, "")

	bpy.context.scene.cursor.location = ( 0, 0, 0)

	# delete initial objects in the new file
	# bpy.ops.object.select_all( action = "DESELECT")
	# bpy.ops.object.select_all( action = "TOGGLE")
	# bpy.ops.object.delete( use_global = False)

	# import car model
	loggen( LogDat, screen_echo, "import vehicle model " + model_path + model_stl)
	bpy.ops.import_mesh.stl(
			filepath	= model_path + model_stl,
			files		= [ { "name": model_stl}],
			directory	= model_path
		)


	# load car center from camera_positions.json
	# moved to setup
	loggen( LogDat, screen_echo, "read " + cam_pos_json)
	cam_pos_file	= open( cam_pos_json, "r")
	cam_pos			= json.load( cam_pos_file)
	cam_pos_file.close()

	loggen( LogDat, screen_echo, "set vehicle origo")
	try:
		loc_car_center = Vector( cam_pos[ "G1"]) / 1000 
		loggen( LogDat, screen_echo, "loc_car_center from " + cam_pos_json)
	except:
		loggen( LogDat, screen_echo, "loc_car_center from setup.py")
		
	loggen( LogDat, screen_echo, "{}".format( loc_car_center))

	# set vehicle model origin
	bpy.context.scene.cursor.location = loc_car_center
	bpy.ops.object.select_all( action = "DESELECT")
	D.objects[ model_name.replace( "_", " ")].select_set(True)
	bpy.ops.object.origin_set( type= "ORIGIN_CURSOR")
	bpy.context.scene.cursor.location = (0, 0, 0)
	D.objects[ model_name.replace( "_", " ")].location =  ( 0, 0, 0)

	# import camera model
	if os.path.exists( model_path + cam_stl):
		loggen( LogDat, screen_echo, "import camera model " + cam_stl)
		bpy.ops.import_mesh.stl(
				filepath	= model_path + cam_stl,
				files		= [ { "name": cam_stl}],
				directory	= model_path
			)

		# set vehicle model origin
		loggen( LogDat, screen_echo, "set camera model origo")
		bpy.context.scene.cursor.location = loc_car_center
		bpy.ops.object.select_all( action = "DESELECT")
		D.objects[ model_name.replace( "_", " ") + " cameras"].select = True
		bpy.ops.object.origin_set( type= "ORIGIN_CURSOR")
		bpy.context.scene.cursor.location = (0, 0, 0)
		D.objects[ model_name.replace( "_", " ") + " cameras"].location =  (0, 0, 0)


	loggen( LogDat, screen_echo, strftime( "Ende posCam Step 1 %d.%m.%y %H:%M:%S", localtime()) + " ( " + Laufzeit( StartZeit) + ")")
	loggen( LogDat, screen_echo, "")

	if not ( "run_both" in locals() or "run_both" in globals()):
		LogZu( LogDat, log_file, model_path, model_name)
		del setup_RK


	os.chdir(cwd)
	## STEP 1 ## 
	############

	StartZeit2 = localtime()

	loggen( LogDat, screen_echo, "")
	loggen( LogDat, screen_echo, strftime( "Start posCam Step 2 %d.%m.%y %H:%M:%S", StartZeit2))

	# append virtual cameras
	loggen( LogDat, screen_echo, "")

	if os.path.exists( cam_blend):
		loggen( LogDat, screen_echo, "append virtual camera from " + cam_blend)
		bpy.ops.wm.append(
				filepath	= cam_blend,
				directory	= cam_blend_dir,
				files		= [
							{ "name":"Car Center"},
							{ "name":"Front"},
							{ "name":"Left"},
							{ "name":"Rear"},
							{ "name":"Right"}
						]
			)
	else:
		loggen( LogDat, screen_echo, "virtual cameras model " + cam_blend + " not found!")

	car_center = D.objects[ "Car Center"]
	#car_center.location = Vector( loc_car_center)
 
	ground = D.objects[ "FMVSS"]
	# ground.location = Vector( ground) #+ Vector((5,0,0))
	# print("***********************")
	# print(ground.location)
	# print("***********************")
 
 
 
	loggen( LogDat, screen_echo, "")
	loggen( LogDat, screen_echo, "car_center.location = "	+ format( Vector( loc_car_center), ""))

	# define camera collection
	cam_objects = [
			D.objects[ "Front"],
			D.objects[ "Left"],
			D.objects[ "Rear"],
			D.objects[ "Right"]
		]
 
	# cam_objects = [D.objects[ "Rear"]]

	for cam in cam_objects:
		cam.parent			= None
		cam.location		= Vector( (0, 0, 0))
		cam.rotation_euler	= Euler( [ 0, 0 , 0])

	if os.path.exists( cam_pos_json):

		bpy.ops.object.select_all( action = "DESELECT")

		for cam in cam_objects:
			cam_position		= cam_pos[ "camera" + cam.name.lower()][ "position"]
			cam.location		= Vector( ( cam_position[ 0], cam_position[ 1], cam_position[ 2])) / 1000

			cam_rotation		= cam_pos[ "camera" + cam.name.lower()][ "rotation"]

			# normalize camera rotation if necessary
			if ( cam_rotation[ 0] < 0):
				cam_rotation[ 0] = - cam_rotation[ 0]
				if ( cam_rotation[ 1] > 0):
					cam_rotation[ 1] = cam_rotation[ 1] - 180
				else:
					cam_rotation[ 1] = cam_rotation[ 1] + 180
				if ( cam_rotation[ 2] > 0):
					cam_rotation[ 2] = cam_rotation[ 2] - 180
				else:
					cam_rotation[ 2] = cam_rotation[ 2] + 180
			
			cam.select_set(True)
			#bpy.ops.transform.rotate( value = radians( cam_rotation[ 2]), axis = Vector(( 0, 0, 1)))	# z2 um Z
			#bpy.ops.transform.rotate( value = radians( cam_rotation[ 0]), axis = Vector(( 1, 0, 0)))	# x  um X
			#bpy.ops.transform.rotate( value = radians( cam_rotation[ 1]), axis = Vector(( 0, 0, 1)))    # z1 um Z

			bpy.ops.transform.rotate(value=radians(cam_rotation[2]), orient_axis='Z')
			# Rotate around X-axis (cam_rotation[0])
			bpy.ops.transform.rotate(value=radians(cam_rotation[0]), orient_axis='X')
			# Rotate around Y-axis (cam_rotation[1])
			bpy.ops.transform.rotate(value=radians(cam_rotation[1]), orient_axis='Z')



			cam.select_set(False)

			loggen( LogDat, screen_echo, "camera" + cam.name.lower())
			loggen( LogDat, screen_echo, "  position : " + format( cam_position))
			loggen( LogDat, screen_echo, "  rotation : " + format( cam_rotation))
			loggen( LogDat, screen_echo, format( cam, ""))
			loggen( LogDat, screen_echo, "  position : " + format( cam.location, ""))
			loggen( LogDat, screen_echo, "  rotation : " + format( cam.rotation_euler, ""))
			loggen( LogDat, screen_echo, "         x : " + "{0:7.2f}".format( degrees( cam.rotation_euler.x)) + "°")
			loggen( LogDat, screen_echo, "         y : " + "{0:7.2f}".format( degrees( cam.rotation_euler.y)) + "°")
			loggen( LogDat, screen_echo, "         z : " + "{0:7.2f}".format( degrees( cam.rotation_euler.z)) + "°")
			loggen( LogDat, screen_echo, "")

	else:
		loggen( LogDat, screen_echo, "camera_position.json " + cam_pos_json + " not found!")

	# nudge the cameras a bit
	for cam in cam_objects:
		vec = Vector( ( 0.0, 0.0, ( nudge_cams + nudge_cams_img) * cam.scale[ 2]))
		inv = cam.matrix_world.copy()
		inv.invert()
			#vec aligned to local axis
		vec_rot = vec @ inv
		cam.location = cam.location + vec_rot

	# "Car Center" as parent for cameras
	bpy.ops.object.select_all( action = "DESELECT")
	bpy.ops.object.select_all( action = "TOGGLE")
	obj = bpy.data.objects["Car Center"]
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.parent_set( type = "OBJECT", keep_transform = True)

	car_center.location = Vector( (0, 0, 0)) # cam + vehicle
	ground.location = Vector( (4.466+2.57, 0, 0.23)) # cam + vehicle
	# ground
    
	print(car_center.location)
	loggen( LogDat, screen_echo, "car_center.location = "	+ format( car_center.location, ""))

	# set camera intrinsics
	for cam in cam_objects:
		cam.cycles.panorama_type = 'CONTI_SV'
		cam.cycles.svcam_fisheyeAmt_1	=  100.0341 
		cam.cycles.svcam_fisheyeAmt_2	=  -10.4642 
		cam.cycles.svcam_fisheyeAmt_3	=  57.2134 
		cam.cycles.svcam_fisheyeAmt_4	=  -82.7111 
		cam.cycles.svcam_fisheyeAmt_5=59.000
		cam.cycles.svcam_fisheyeAmt_6	=  -16.000
		cam.cycles.svcam_cam_aspect	=  0.9986

	# save blend
	loggen( LogDat, screen_echo, "save " + model_blend)
	bpy.ops.wm.save_mainfile(
			filepath		= model_blend,
			compress		= True,
			relative_remap	= True
		)

	if os.path.exists( model_blend):
		loggen( LogDat, screen_echo, "size: " + "{:,}".format( os.path.getsize( model_blend), ""))
	else:
		loggen( LogDat, screen_echo, model_blend + " not saved!")

	loggen( LogDat, screen_echo, "")
	loggen( LogDat, screen_echo, strftime( "Ende posCam Step 2 %d.%m.%y %H:%M:%S", localtime()) + " ( " + Laufzeit( StartZeit2) + ")")
	if ("StartZeit" in locals() or "StartZeit" in globals()):
		loggen( LogDat, screen_echo, "Gesamt: " + Laufzeit( StartZeit))
		del StartZeit

	LogZu( LogDat, log_file, model_path, model_name)

	del StartZeit2
	os.chdir(cwd)

except Exception as e:
	os.chdir(cwd)
	raise e
	

