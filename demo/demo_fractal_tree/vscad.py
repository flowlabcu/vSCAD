import numpy as np
import vSCAD as vs

# ---- Draw a fractal tree with 4 levels of recursion ---- #
fractal_tree = vs.Tree.BinaryTree(start_point=(0, 0, 0), length=10, angle=np.pi/6, depth=4, diameter=1, num_points_base=10)

# ---- Get the branches of the tree ---- # 
branches = fractal_tree.draw_tree()

# ---- Create a vessel object for each branch ---- #
vessel_object = []
for branch in branches:
    vessel_name = f'branch_{branches.index(branch)}'
    vessel = vs.Vessel(name=vessel_name)
    vessel.set_scale_factor(scale_factor=1.0)
    vessel.set_path(branch.points)
    vessel.set_diameters(branch.diameters)
    vessel.interpolate_paths(n=3) 
    vessel.get_direction_vectors()
    vessel.get_euler_angles()
    vessel_object.append(vessel)

# ---- Prepare OpenSCAD file ---- #
scad_file = vs.SCADFile('vessel.scad')

# ---- Import OpenSCAD functions ---- #
scad_file.modules.import_circle_at()
scad_file.modules.import_loft_path()

# ---- Import vessel data ---- #
for object in vessel_object:
    scad_file.import_vessel(object)

# ---- Write OpenSCAD code ---- #    
scad_file.modules.start_union()

for object in vessel_object: 
    scad_file.modules.function_loft_path(object)

scad_file.modules.end_union()

scad_file.write_stl('binary_tree.stl')