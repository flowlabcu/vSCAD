Welcome to vSCAD's documentation!
======================================

About
-----------------
vSCAD (Vascular Solid Computer Aided Design) is a tool designed for creating CFD/3dPrinting - ready STLs of vascular networks. 
The toolkit is based on the open-source software, OpenSCAD, and leverages custom OpenSCAD modules to loft vessel paths and 
diameters into complex tree structures.

Features
-----------------
vSCAD is a collection of geometric tools designed to break complex vascular networks into vessel objects that are merged in OpenSCAD. These vessels can be created to:

- Create 3D geometries from 2D image data from basic path and diameter analysis using a tool such as ImageJ.

- Import vascular tree data in the form of connectivity, node, and diameter arrays to generate custom vascular tree geometries.

- Smooth OpenSCAD's STL outputs with degenerate traingles to generate isotrpoic triangle surface meshes. For use in CFD simulations or for 3D printing.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   toc_demo
   toc_modules


Indices and tables
-------------------
* :ref:`genindex`
* :ref:`modindex`

