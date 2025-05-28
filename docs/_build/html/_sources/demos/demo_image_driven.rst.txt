=========================
Demo Image Driven
=========================

This is a demo of the vSCAD package. It will show you how to use the package to generate a 3D model from a set of points and diameters.

Creating a project
-------------------
vSCAD uses a preset file structure to organize projects. After installing the package, you can create a new project by running the following command:

.. code-block:: console

    $ python3 ~/path/to/vSCAD/src/vSCAD/io/new_project.py

This will create a new project in the current directory. The project directory will contain:
1. `vscad.py`: The main script for generating the 3D model.
2. `image_data/`: A directory for storing the point and diameter data.
3. `scad/`: A directory for storing the OpenSCAD files.
4. `scad-stl/`: A directory for storing the generated 3D models generated from OpenSCAD.


Writing the script
------------------

We will now begin editing the `vscad.py` script to generate the 3D model. vSCAD provides 
a method to load points and diameters from a csv file generated from ImageJ. 
To import from an ImageJ csv file, use the following:

.. code-block:: python

    Reader = ImageJReader
    # ---- Read data for main vessel ---- #
    main_path_csv = 'image_data/main.pth'
    main_diam_csv = 'image_data/main.diam'
    points = Reader.get_path(main_path_csv)
    diameters = Reader.get_diam(main_diam_csv)

Next we create a vessel object. The vessel object is the main object in vSCAD. It contains the points and diameters, 
and has methods for smoothing the geometry using cubic spline interpolation. 

.. code-block:: python

    # Make main vessel object
    main_vessel = vs.Vessel(name='main_vessel')
    main_vessel.set_scale_factor(scale_factor=1.0)
    main_vessel.set_path(points)
    main_vessel.set_diameters(diameters)

We have the option of scaling our point data by using the `set_scale_factor` method. This is useful when the point and diameter
data are in pixels and need to be scaled to a physical unit. `set_scale_factor` is 1 by default.

In this example, we will generate a mesh from a simple bifurcation. The bifurcation is defined by two paths, `main` and `side`. We will make a second
vessel object for the side path.    

.. code-block:: python

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

If we want to smooth the geometry beyond what our point and diameter data provides, we can use the `interpolate_paths` method. This method
belongs to the vessel object and will smooth the geometry using cubic spline interpolation. We specify the number of points to interpolate.

.. code-block:: python

    # ---- Interpolate paths ---- #
    main_vessel.interpolate_path(n=3)
    side_vessel.interpolate_path(n=3)

Next, we prepare the vessel objects for OpenSCAD. When OpenSCAD generates a cylinder at each point, it assumes the cylinder is oriented along the z-axis.
To smoothly connect each point, we need to provide euler angles to rotate each cylinder. We do this by finding the tangent vector between each point and 
rotating the cylinder to align with the tangent vector.

.. code-block:: python

    # ---- Prepare vessels for OpenSCAD ---- #
    main_vessel.get_direction_vectors()
    main_vessel.get_euler_angles()

    side_vessel.get_direction_vectors()
    side_vessel.get_euler_angles()

Finally, we generate the 3D model using OpenSCAD. We prepare the OpenSCAD file for writting by creating a `SCADFile` object.  

.. code-block:: python

    scad_file = vs.SCADFile('vessel.scad')

Next, import the point and angle data that we have already prepared.

.. code-block:: python

    # ---- Import vessel data ---- #
    scad_file.import_vessel(main_vessel)
    scad_file.import_vessel(side_vessel)


We then import OpenSCAD modules necessary to generate the 3D model. We will call these modules later.  

.. code-block:: python

    # ---- Import OpenSCAD functions ---- #
    scad_file.modules.import_circle_at()
    scad_file.modules.import_loft_path()

`import_circle_at` is a function that draws a cylinder with a small height at a specified point, diameter, and rotation. OpenSCAD does 
not loft 2D objects, so we use cylinders with small heights to represent circles.

`import_loft_path` is a function that generates a 3D model by hulling the cylinders. Since OpenSCAD does not have a built-in loft function,
we use the hull function to connect our nearly-2D cylinders into a 3D model.

After importing the necessary functions, we write the OpenSCAD code to generate the 3D model. In our bifurcation example, we want each vessel to 
be part of one final body. To do this we use `start_union()` and `end_union()` functions to group the cylinders together. Between the union 
markers, we loft each vessel.

.. code-block:: python

    # ---- Write OpenSCAD code ---- #
    scad_file.start_union()
    
    scad_file.modules.function_loft_path(main_vessel)
    scad_file.modules.function_loft_path(side_vessel)

    scad_file.end_union()

Notice that OpenSCAD modules that were imported earlier using the `import` prefix are called using the `function` prefix.

Finally, we can run the OpenSCAD code and generate the 3D model. This is the only step that requires OpenSCAD to be installed on your system.

.. code-block:: python

    scad_file.write_stl('vessel.stl')

The full script
-----------------

.. code-block:: python

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


