import bpy
import mathutils

context = bpy.context 
scene = context.scene
object = context.object

def reset_blend():
    #bpy.ops.wm.read_factory_settings()

    for scene in bpy.data.scenes:
        for obj in scene.objects:
            scene.objects.unlink(obj)

    for bpy_data_iter in (
            bpy.data.objects,
            bpy.data.meshes,
            bpy.data.lamps,
            bpy.data.cameras,
            ):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)

reset_blend()

print('Import')
bpy.ops.import_mesh.stl(filepath="D://3d//FDG0160U_DLUDungeonStarterSet_03012017//FDG0160U_DLU_Wall1.stl")
fdg = bpy.data.objects["FDG0160U DLU Wall1"]

# clean up
#bpy.context.scene.objects.active = fdg
#bpy.ops.object.editmode_toggle()
#bpy.ops.mesh.select_all(action='SELECT')
#bpy.ops.mesh.remove_doubles()
#bpy.ops.mesh.normals_make_consistent()
#bpy.ops.object.editmode_toggle()

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

scene.objects.link(cube)
cube.select = True
boo = fdg.modifiers.new('BDiff', 'BOOLEAN')
boo.object = cube
boo.operation = 'DIFFERENCE'
scene.objects.active = fdg
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="BDiff")
bpy.data.objects.remove(cube, do_unlink=True)

print('Scale')
minz = 100
minx = 100
maxx = 0
miny = 100
maxy = 0
for vert in fdg.data.vertices:
    if vert.co.z < minz:
        minz = vert.co.z
        maxx = vert.co.x
        maxy = vert.co.z
    elif vert.co.z == minz:
        if vert.co.x > maxx:
            maxx = vert.co.x
        if vert.co.x < minx:
            minx = vert.co.x
        if vert.co.y > maxy:
            maxy = vert.co.y
        if vert.co.y < miny:
            miny = vert.co.y

scalex = 50.0/abs(minx-maxx)
scaley = 50.0/abs(miny-maxy)
scalez = 43.5/fdg.dimensions[2]
#print('Scaling to %f, %f, %f' % (scalex, scaley, scalez))

fdg.scale = (scalex, scaley, scalez)
fdg.location += mathutils.Vector((0,0,-3.2))

print('Add base')
verts = [
(-25.001,-25,0),
(-25.001,25,0),
(25,25,0),
(25,-25,0),
(-25.001,-25,2.8),
(-25.001,25,2.8),
(25,25,2.8),
(25,-25,2.8)]
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

scene.objects.link(cube)
cube.select = True

boo = fdg.modifiers.new('BUnion', 'BOOLEAN')
boo.object = cube
boo.operation = 'UNION'
scene.objects.active = fdg
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="BUnion")
bpy.data.objects.remove(cube, do_unlink=True)

print('Export')
bpy.ops.export_mesh.stl(filepath="D://3d//FDG0160U_DLUDungeonStarterSet_03012017//FDG0160U_DLU_Wall1_BPY.stl", )
#bpy.ops.object.mode_set(mode = 'OBJECT')

print('Done!\n')