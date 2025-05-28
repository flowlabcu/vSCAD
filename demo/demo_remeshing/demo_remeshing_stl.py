import vSCAD as vs

# ---- Import OpenSCAD-Generated STL ---- #
stl_path = 'scad-stl/vessel.stl'

remesh = vs.Remesh(stl_path)

# ---- Set remeshing parameters ---- #
# 0.60% of the bounding box diagonal - coarser values result in fewer mesh errors
remesh.set_initial_target_length_percentage(0.6) 

# 0.10% of the bounding box diagonal 
remesh.set_final_target_length_percentage(0.1)

# 0.10% of the bounding box diagonal
# We remesh the model starting with a target length of 0.6% of the bounding box diagonal,
# and we reduce the target length by 0.1% of the bounding box diagonal at each remeshing step
remesh.set_target_length_reduction_step_size(0.1)

# Number of isotropic remeshing iterations
remesh.set_isotropic_remeshing_iterations(3)

# Number of recursive smoothing iterations
remesh.set_recursive_smoothing_iterations(10)

# Number of final smoothing iterations
remesh.set_final_smoothing_iterations(30)

# Save the mesh every 10 steps
remesh.set_saveout_period(10)

# ---- Remesh the STL file ---- #
# The original STL mesh is copied to 'scad-stl/original-mesh.stl'
# The final STL mesh is saved to the same name as the original STL file
remesh.remesh_stl()
