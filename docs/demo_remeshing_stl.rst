==================
Remeshing an stl
==================

OpenSCAD, like most CAD programs, does not generate nice surface meshes for use in CFD. The surface mesh is often very coarse and not isotropic. This can lead to poor quality simulations. 
To improve the mesh quality, we can use the `pyMeshLab` package to remesh the stl file.

Here, we demonstrate a `pyMeshLab` wrapper function that can be used to remesh the stl file. 

This script demonstrates the remeshing of an STL file using the vSCAD library.


Import the OpenSCAD-generated STL file.
---------------------------------------
First, we import the OpenSCAD-generated STL file that we want to remesh. We pass 
the path to the STL file to the `Remesh` class.

.. code-block:: python

    import vSCAD as vs

    stl_path = 'scad-stl/vessel.stl'

    remesh = vs.Remesh(stl_path)

Next, we set the remeshing parameters. We first set the coursest isotropic cell diameter to use:

.. code-block:: python

    remesh.set_initial_target_length_percentage(0.6) 

This sets the initial target length as a percentage (0.6%) of the bounding box diagonal. 

We also set the final target length:

.. code-block:: python

    remesh.set_final_target_length_percentage(0.1)

We will then set the target length reduction step size: 
Here we set it to 0.1% of the bounding box diagonal.

.. code-block:: python

    remesh.set_target_length_reduction_step_size(0.1)

This will recursively remesh the geometry until the target length is reached.

We can additionally set the number of isotropic remeshing iterations and smoothing 
iterations for each recursive remeshing step:

.. code-block:: python

    remesh.set_isotropic_remeshing_iterations(3)
    remesh.set_recursive_smoothing_iterations(10)

Finally, we set the final smoothing iterations:

.. code-block:: python

    remesh.set_final_smoothing_iterations(10)

We also can save the mesh at a specified interval during the remeshing process.

.. code-block:: python

    remesh.set_saveout_period(10)

Finally, with these parameters set, we can perform the remeshing process and save 
the final STL file:

.. code-block:: python

    remesh.remesh_stl()

The full script is shown below:

.. code-block:: python

    import vSCAD as vs

    stl_path = 'scad-stl/vessel.stl'

    remesh = vs.Remesh(stl_path)

    remesh.set_initial_target_length_percentage(0.6) 
    remesh.set_final_target_length_percentage(0.1)
    remesh.set_target_length_reduction_step_size(0.1)
    remesh.set_isotropic_remeshing_iterations(3)
    remesh.set_recursive_smoothing_iterations(10)
    remesh.set_final_smoothing_iterations(10)
    remesh.set_saveout_period(10)

    remesh.remesh_stl()

