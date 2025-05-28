import numpy as np
import vSCAD as vs

scad_file = 'demo_nodal_tree.scad'
# Scad file written at scad/demo_nodal_tree.scad

# ---- Draw a nodal tree with 4 levels of recursion ---- #
# Define the points, diameters, and connectivity of the tree
points = np.array([[0.0, 0.0, 0.0],
                   [0.0, 1.0, 0.0],
                   [1.0, 2.0, 0.0],
                   [-0.5, 2.0, 0.0]])

# include end diameter of final branch
diameters = np.array([0.05, 0.05, 0.05, 0.05])

connectivity = np.array([[0, 1],
                         [1, 2],
                         [1, 3]])

# ---- Create the NodeTree object ---- #
tree = vs.NodalTree(connectivity, points, diameters, num_points=5)
branches = tree.draw_tree()

# Create a vessel object for each branch
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

scad_file.write_stl('nodal_tree.stl')

