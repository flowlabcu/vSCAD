==============================
Demo Nodal Tree
==============================

In this demo, we will create a nodal tree using the ``Tree`` module in vSCAD. 

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

Similar to the binary tree, we create a ``NodalTree`` object that contains ``branches``. However, 
we must provide a list of nodes, or poits, diameters, and a connectivity matrix that
defines how the nodes are connected through branches. We will describe the 
function of each of these components below.

- Connectivity Matrix: A matrix that defines how the nodes (points) are connected. 
The matrix is of the form `[[0, 1], [1, 2], [2, 3]]`, where each row defines a connection between two nodes.
The row index of the connectivity matrix corresponds to the branch index. The elements of the matrix are are 
the node indices. For example, the first row `[0, 1]` defines a connection between nodes 0 and 1.

- Points: A list of points that define the nodes of the tree. Each point is a tuple of the form `(x, y, z)`.

- Diameters: A list of diameters for each branch. The diameter is a scalar value. 

Each of these arrays must be a numpy array before being passed to the ``NodalTree`` object. Here,
we will create a simple nodal tree with 4 nodes and 3 branches.

.. code-block:: python

    # Define the points, diameters, and connectivity of the tree
    points = np.array([[0.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0],
                       [1.0, 2.0, 0.0],
                       [-0.5, 2.0, 0.0]])

    diameters = np.array([0.05, 0.05, 0.05])

    connectivity = np.array([[0, 1],
                             [1, 2],
                             [1, 3]])

We now create a ``NodalTree`` object using the following code:

.. code-block:: python

    nodal_tree = vs.Tree.NodalTree(points=points, 
                                   diameters=diameters, 
                                   connectivity=connectivity,
                                   num_points=5)

We can specify the number of points in each branch by using the `num_points` argument. 

Writing the Vessels 
------------------
vSCAD uses the ``Vessel`` object as the main object for generating 3D models. In order
to create a 3D model of the tree we just generated, we need to convert the tree object
into a vessel object. ``Tree`` objects contain ``branch`` subobjects that contain 
the points and diameters of each branch. We can convert
the ``branch`` subobjects into vessel objects using a for loop:

.. code-block:: python

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

Here, we've given the data within the ``branch`` object to a new ``vessel`` object. We give each 
``vessel`` object a unique name and append it to a list. We then interpolate the paths, 
get the direction vectors, and get the Euler angles used in OpenSCAD.