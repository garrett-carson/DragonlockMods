import bpy
import mathutils
import reset
import ntpath

class dlmutils:
	@staticmethod
	def makeof(importpath):
		reset.reset.reset()
		dlmutils.importfdg(importpath)
		name = ntpath.basename(importpath).replace("_", " ").replace(".stl", "")
		fdg = bpy.data.objects[name]
		#cleanup()
		dlmutils.cutbottom(fdg)
		dlmutils.scale(fdg)
		dlmutils.addbase(fdg)
		dlmutils.exportfdg(importpath)
		print('Done!')
	
	@staticmethod
	def importfdg(importpath):
		print('Import')
		bpy.ops.import_mesh.stl(filepath=importpath)
	
	# def cleanup(fdg):
		# print('Clean up')
		# bpy.context.scene.objects.active = fdg
		# bpy.ops.object.editmode_toggle()
		# bpy.ops.mesh.select_all(action='SELECT')
		# bpy.ops.mesh.remove_doubles()
		# bpy.ops.mesh.normals_make_consistent()
		# bpy.ops.object.editmode_toggle()
	
	@staticmethod
	def cutbottom(fdg):
		print('Cut bottom')
		verts = [
			(-30,-30,-1),
			(-30,30,-1),
			(30,30,-1),
			(30,-30,-1),
			(-30,-30,5),
			(-30,30,5),
			(30,30,5),
			(30,-30,5)]
		faces = [
			(0,1,2,3),
			(4,5,6,7),
			(0,4,5,1),
			(1,5,6,2),
			(2,6,7,3),
			(3,7,4,0)]
		mesh_data = bpy.data.meshes.new("cube_mesh_data")
		mesh_data.from_pydata(verts, [], faces)
		mesh_data.update(calc_edges=True)
		
		cube = bpy.data.objects.new("Cube", mesh_data)
		
		scene = bpy.context.scene
		scene.objects.link(cube)
		cube.select = True
		boo = fdg.modifiers.new('BDiff', 'BOOLEAN')
		boo.object = cube
		boo.operation = 'DIFFERENCE'
		scene.objects.active = fdg
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="BDiff")
		bpy.data.objects.remove(cube, do_unlink=True)
	
	@staticmethod
	def scale(fdg):
		print('Scale')
		minz = 100
		minx = 100
		maxx = 0
		miny = 100
		maxy = 0
		mesh = fdg.data
		for vert in mesh.vertices:
			if vert.co.z < minz:
				minz = vert.co.z
				maxx = vert.co.x
				maxy = vert.co.z
			elif vert.co.z == minz or abs(vert.co.z - minz) < .1:
				if vert.co.x > maxx:
					maxx = vert.co.x
				if vert.co.x < minx:
					minx = vert.co.x
				if vert.co.y > maxy:
					maxy = vert.co.y
				if vert.co.y < miny:
					miny = vert.co.y
		
		print('minx: %f miny: %f minz: %f' % (minx, miny, minz))
		print('maxx: %f maxy: %f height: %f' % (maxx, maxy, fdg.dimensions[2]))
		
		otherx = float(abs(minx-maxx))
		scalex = 100
		if otherx > 50.0:
			scalex = 50.0 / otherx
		else:
			scalex = otherx / 50.0
		
		othery = float(abs(miny-maxy))
		scaley = 100
		if othery > 50.0:
			scaley = 50.0 / othery
		else:
			scaley = othery / 50.0
		
		height = fdg.dimensions[2]
		
		scalez = 1
		if height > 43.5:
			scalez = 43.5/fdg.dimensions[2]
		
		print('Scaling to %f, %f, %f' % (scalex, scaley, scalez))
		
		fdg.scale = (scalex, scaley, scalez)
		fdg.location += mathutils.Vector((0,0,-3.2))
	
	@staticmethod
	def addbase(fdg):
		print('Add base')
		verts = [
			(-25.001,-25.001,0),
			(-25.001,25.001,0),
			(25.001,25.001,0),
			(25.001,-25.001,0),
			(-25.001,-25.001,2.8),
			(-25.001,25.001,2.8),
			(25.001,25.001,2.8),
			(25.001,-25.001,2.8)]
		faces = [
			(0,1,2,3),
			(4,5,6,7),
			(0,4,5,1),
			(1,5,6,2),
			(2,6,7,3),
			(3,7,4,0)]
		mesh_data = bpy.data.meshes.new("cube_mesh_data")
		mesh_data.from_pydata(verts, [], faces)
		mesh_data.update(calc_edges=True)
		
		cube = bpy.data.objects.new("Cube", mesh_data)
		
		scene = bpy.context.scene
		scene.objects.link(cube)
		cube.select = True
		
		boo = fdg.modifiers.new('BUnion', 'BOOLEAN')
		boo.object = cube
		boo.operation = 'UNION'
		scene.objects.active = fdg
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="BUnion")
		bpy.data.objects.remove(cube, do_unlink=True)
	
	@staticmethod
	def exportfdg(importpath):
		print('Export')
		bpy.ops.export_mesh.stl(filepath=importpath.replace(".stl", "_BPY.stl"))