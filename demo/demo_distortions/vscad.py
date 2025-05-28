import numpy as np
import vSCAD as vs
import matplotlib.pyplot as plt

# ---- Create vessel ---- #
points = np.array([[0, 0, 0], [0, 20, 0]])
diameters = np.array([1, 1])
vessel = vs.Vessel(name='vessel_1')
vessel.set_path(points)
vessel.set_diameters(diameters)
vessel.interpolate_paths(n=20)

# ---- Create distortion ---- #
distortion = vs.Geometry.Distortions

distortion.add_path_noise(vessel, noise_level=0.02, noise_type='xz', hold=6)


# ---- Prepare vessels for OpenSCAD ---- #
vessel.interpolate_paths(n=10)
vessel.get_direction_vectors()
vessel.get_euler_angles()


# ---- Prepare OpenSCAD file ---- #
scad_file = vs.SCADFile('vessel.scad')
scad_file.import_vessel(vessel)


scad_file.modules.import_circle_at()
scad_file.modules.import_loft_path()

scad_file.modules.start_union()
scad_file.modules.function_loft_path(vessel)
scad_file.modules.end_union()

scad_file.write_stl('vessel.stl')









