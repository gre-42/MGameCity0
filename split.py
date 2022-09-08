import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *
from pathlib import Path

# Disabled decimation because UVs became wrong
# and because it hardly changed the file size.
for decimate in [0]: # , 1]:
    # Delete old objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(confirm=False)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material, do_unlink=True)

    # Load FBX
    # bpy.ops.import_scene.fbx(filepath='/tmp/test.fbx')
    bpy.ops.import_scene.fbx(filepath='source/Buildings.fbx')

    for obj in bpy.context.selected_objects:
        # Skip non-mesh objects
        if obj.type != 'MESH':
            print(f'skipping non-mesh object "{obj.name}"')
            continue
        if obj.parent is not None:
            print(f'skipping child object "{obj.name}" (it should be grass anyway)')
            continue
        print(f'Processing object "{obj.name}"')

        # Select object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Move towards origin
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        # min_x = min(c[0] for c in obj.bound_box)
        # max_x = max(c[0] for c in obj.bound_box)
        # min_y = min(c[1] for c in obj.bound_box)
        min_x = min(v.co.x for v in obj.data.vertices)
        max_x = max(v.co.x for v in obj.data.vertices)
        min_y = min(v.co.y for v in obj.data.vertices)

        obj.location.x -= (max_x + min_x) / 2
        obj.location.y -= min_y

        # Decimate
        if decimate != 0:
            bpy.ops.object.modifier_add(type='DECIMATE')
            # bpy.context.object.modifiers["Decimate"].ratio = 0.5
            bpy.context.object.modifiers["Decimate"].decimate_type = 'DISSOLVE'
            # Apply modifier to triangulation works
            bpy.ops.object.modifier_apply(modifier="Decimate")

        # Convert to quads
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        bpy.ops.mesh.tris_convert_to_quads()
        bpy.ops.object.editmode_toggle()

        # Export to OBJ
        dest_dir = Path('split_%d' % decimate)
        dest_dir.mkdir(exist_ok=True)
        obj_filepath = dest_dir.joinpath(obj.name + '.obj')
        mtl_filepath = dest_dir.joinpath(obj.name + '.mtl')

        bpy.ops.export_scene.obj(
            filepath=str(obj_filepath),
            use_selection=True,
            group_by_material=True)
        
        with open(str(mtl_filepath), 'r') as f:
            s = f.read()
            s = s.replace('source/D:/Modelagem/PBR textures/MyTextures/', '../textures/')
            s = s.replace('.png', '.jpeg')
        with open(str(mtl_filepath), 'w') as f:
            f.write(s)

        # Remove decimate modifier
        bpy.ops.object.modifier_remove(modifier='Decimate')
