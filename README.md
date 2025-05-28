# vSCAD
## 1. About
`vSCAD` or the **Vascular Systems Computer Aided Design Software Toolkit** is a toolkit designed for creating parametrized surface meshes for vascular networks that are CFD simulation-ready as well as 3D print-ready. `vSCAD` was developed with a focus on microcirculatory vascular systems and microcirculatory network modeling. However, `vSCAD` is capable of developing any geometric model relevant for internal flows across and around complex networks.

The toolkit is built in `Python` based on the open-source software, [OpenSCAD](https://openscad.org/index.html/) , and leverages custom OpenSCAD modules to loft vessel paths and diameters into complex tree structures. vSCAD is best suited to take small-vessel and microfluidic geometries from 2D image data to a 3D domain for CFD and printing. This library has been developed based on research and development needs at [FLOWLab](https://www.flowphysicslab.com/), an interdisciplinary research group focusing on flow physics and transport phenomena in biofluid systems at the *University of Colorado, Boulder*. 

## 2. Features
vSCAD is a collection of geometric tools designed to break complex vascular networks into vessel objects that are merged in OpenSCAD. These vessels can be created to:

- Create 3D geometries from 2D image data from basic path and diameter analysis using a tool such as ImageJ.

- Import vascular tree data in the form of connectivity, node, and diameter arrays to generate custom vascular tree geometries.

- Smooth OpenSCAD's STL outputs with degenerate traingles to generate isotrpoic triangle surface meshes. For use in CFD simulations or for 3D printing.

## 3. Installation
vSCAD is easily installed with:

        $ pip install vSCAD

All dependencies are found in ``requirements.txt``.

In addition to the vSCAD Python library, OpenSCAD is required to create the geometries. OpenSCAD can be installed [here](https://openscad.org/downloads.html).

## 4. Demos
For those looking to get started with using vSCAD, we have provided a collection of well documented demos along with the library.

## 5. Modules
Module documentation is available in the vSCAD documentation page at the following link: Modules (NEED LINK). Comments and feedback on module documentation can be shared by opening an Issue on the GitHub page, or by emailing the contributors directly below.
