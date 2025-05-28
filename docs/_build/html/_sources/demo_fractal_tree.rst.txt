==============================
Demo Fractal Tree
==============================

In this demo, we will create a binray tree using the ``Tree`` module in vSCAD. 

Creating a project
-------------------
vSCAD uses a preset file structure to organize projects. After installing the package, you can create a new project by running the following command:

.. code-block:: console

    $ python3 ~/path/to/vSCAD/src/vSCAD/io/new_project.py

This will create a new project in the current directory. The project directory will contain:
1. `vscad.py`: The main script for generating the 3D model.
2. `image_data/`: A directory for storing the point and diameter data.
3. `scad/`: A directory for storing the OpenSCAD files.
4. `scad-stl/`: A directory for storing the generated 3D models generated from OpenSCAD

In this demo, we will not use the ``image_data`` directory. 

Writing the Tree
------------------

We will now begin editing the `vscad.py` script to generate the 3D model. Creating a 
binray tree is simple with the ``Tree`` module. We create the tree object using 
the following code:

.. code-block:: python

    fractal_tree = vs.Tree.BinaryTree(start_point=(0, 0, 0), 
                                      length=10, 
                                      angle=np.pi/6, 
                                      depth=4, 
                                      diameter=1, 
                                      num_points_base=10)

The `BinaryTree` method creates a binary tree object. The arguments are as follows:
- `start_point`: The starting point of the tree. This is a tuple of the form `(x, y, z)`.
- `length`: The length of the base tree.
- `angle`: The angle between the branches.
- `depth`: The depth of the tree.
- `diameter`: The diameter of the tree.
- `num_points_base`: The number of points in the base of the tree.

By default, each child branch will be 0.7 times the length of the parent branch. We can change by 
using the following code:

.. code-block:: python

    fractal_tree.set_branch_length_reduction(alpha)

where `alpha` is the reduction factor.

The child branch diameter will additionally be calculated using Murray's law with and 
exponent of 3.0. We can change the exponent by using the following code:

.. code-block:: python

    fractal_tree.set_murray_exponent(beta)

where `beta` is the exponent.

Writing the Vessels 
------------------------
vSCAD uses the ``Vessel`` object as the main object for generating 3D models. In order
to create a 3D model of the tree we just generated, we need to convert the tree object
into a vessel object. ``Tree`` objects contain ``branch`` subobjects that contain 
the points and diameters of each branch. We can convert
the ``branch`` subobjects into vessel objects using a for loop:

.. code-block:: python

    branches = fractal_tree.draw_tree()

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

Here, we've given the data within the ``branch`` object to a new ``vessel`` object. We give each 
``vessel`` object a unique name and append it to a list. We then interpolate the paths, 
get the direction vectors, and get the Euler angles used in OpenSCAD.

Writing the OpenSCAD file
-------------------------
We can now write the OpenSCAD file. We will import the ``Vessel`` objects we created to the
OpenSCAD file. We will also import lofting modules:

.. code-block:: python

    scad_file = vs.SCADFile('vessel.scad')

    scad_file.modules.import_circle_at()
    scad_file.modules.import_loft_path()

    for object in vessel_object:
        scad_file.import_vessel(object)

Next, we need to loft each vessel and merge their geometries:

.. code-block:: python

    scad_file.modules.start_union()
    
    for object in vessel_object:
        scad_file.loft_path(object)

    scad_file.modules.end_union()

Finally, we call OpenSCAD to write the STL mesh:

.. code-block:: python

    scad_file.write_scad_file('binray_tree.scad')

The full script is shown below:
---------------------------------

.. code-block:: python 

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


Writing the OpenSCAD file
-------------------------
We can now write the OpenSCAD file. We will import the ``Vessel`` objects we created to the
OpenSCAD file. We will also import lofting modules:

.. code-block:: python

    scad_file = vs.SCADFile('vessel.scad')

    scad_file.modules.import_circle_at()
    scad_file.modules.import_loft_path()

    for object in vessel_object:
        scad_file.import_vessel(object)

Next, we need to loft each vessel and merge their geometries:

.. code-block:: python

    scad_file.modules.start_union()
    
    for object in vessel_object:
        scad_file.loft_path(object)

    scad_file.modules.end_union()

Finally, we call OpenSCAD to write the STL mesh:

.. code-block:: python

    scad_file.write_scad_file('nodal_tree.scad')

The full script is shown below:
---------------------------------

.. code-block:: python

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

    diameters = np.array([0.05, 0.05, 0.05])

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

