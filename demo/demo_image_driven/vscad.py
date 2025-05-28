import numpy as np
import vSCAD as vs

Reader = vs.ImageJReader
# ---- Read data for main vessel ---- #
main_path_csv = 'image_data/main.pth'
main_diam_csv = 'image_data/main.diam'
points = Reader.get_path(main_path_csv)
diameters = Reader.get_diam(main_diam_csv)

# Make main vessel object
main_vessel = vs.Vessel(name='main_vessel')
main_vessel.set_scale_factor(scale_factor=1.0)
main_vessel.set_path(points)
main_vessel.set_diameters(diameters)

# ---- Read data for side vessel ---- #
side_path_csv = 'image_data/side.pth'
side_diam_csv = 'image_data/side.diam'
points = Reader.get_path(side_path_csv)
diameters = Reader.get_diam(side_diam_csv)

# Make side vessel object
side_vessel = vs.Vessel(name='side_vessel')
side_vessel.set_scale_factor(scale_factor=1.0)
side_vessel.set_path(points)
side_vessel.set_diameters(diameters)

# ---- Interpolate paths ---- #
main_vessel.interpolate_paths(n=3)
side_vessel.interpolate_paths(n=3)

# ---- Prepare vessels for OpenSCAD ---- #
main_vessel.get_direction_vectors()
main_vessel.get_euler_angles()

side_vessel.get_direction_vectors()
side_vessel.get_euler_angles()

# ---- Prepare OpenSCAD file ---- #
scad_file = vs.SCADFile('vessel.scad')

# ---- Import vessel data ---- #
scad_file.import_vessel(main_vessel)
scad_file.import_vessel(side_vessel)

# ---- Import OpenSCAD functions ---- #
scad_file.modules.import_circle_at()
scad_file.modules.import_loft_path()

# ---- Write OpenSCAD code ---- #
scad_file.modules.start_union()

scad_file.modules.function_loft_path(main_vessel)
scad_file.modules.function_loft_path(side_vessel)

scad_file.modules.end_union()

# ---- Write stl ---- #
scad_file.write_stl('vessel.stl')