# vSCAD

## 1. About

`vSCAD` or the **Vascular Systems Computer Aided Design Software Toolkit** is a toolkit designed for creating parametrized surface meshes for vascular networks that are CFD simulation-ready as well as 3D print-ready. `vSCAD` was developed with a focus on microcirculatory vascular systems and microcirculatory network modeling. However, `vSCAD` is capable of developing any geometric model relevant for internal flows across and around complex networks. The complete documentation for `vSCAD` toolkit can be found [here](https://vscad.readthedocs.io/en/latest/index.html).

The toolkit is built in `Python` based on the open-source software, [OpenSCAD](https://openscad.org/index.html/) , and leverages custom `OpenSCAD` modules to loft vessel paths, diameters, and other morphological features into complex tree or network structures. `vSCAD` is best suited to take small-vessel, microcirculatory, and micro/milli-fluidic geometries from 2D/3D image data to a 3D domain for CFD and 3D printing.

## 2. Features

`vSCAD` is a collection of geometric tools designed to break complex vascular networks into vessel objects that are merged in OpenSCAD. These vessels can be created to:

- Create 3D geometries from 2D image data from basic path and diameter analysis (*such as those obtained using standard image-processing tools such as ImageJ*).

- Import vascular tree data in the form of connectivity, node, and diameter arrays to generate custom vascular tree geometries.

- Smooth `OpenSCAD`'s STL outputs with degenerate triangles to generate isotropic triangle surface meshes, for use in CFD simulations or for 3D printing.

## 3. Installation

`vSCAD` can be easily installed with:

```bash
pip install vSCAD
```

All dependencies are found in `requirements.txt`. In addition to the vSCAD Python library, OpenSCAD is required to create the geometries. OpenSCAD can be installed [here](https://openscad.org/downloads.html).

## 4. Demos

For those looking to get started with using `vSCAD`, we have provided a collection of well documented demos along with the library. These demos can all be accessed [here](https://vscad.readthedocs.io/en/latest/toc_demo.html).

## 5. Modules

Module documentation is available in the `vSCAD` documentation page [here](https://vscad.readthedocs.io/en/latest/toc_modules.html). Comments and feedback on module documentation can be shared by opening an Issue on the GitHub page, or by emailing the contributors directly below.

## 6. How to cite our code?

While `vSCAD` is released as an open-source toolkit, there is currently not a single linking article that you can cite to acknowledge the use of `vSCAD` in your work. Hence, the best way to cite our tool directly is to link to our GitHub repository.

## 7. Questions and issues

For questions and issues, please feel free to directly reach out to the contributors below, report an `Issue` on our GitHub page, or email us at *FLOWLab* through our contacts page linked [here](https://www.flowphysicslab.com/contact.html).

## 8. License

`vSCAD` is released under the **GNU LGPL License**.

## 9. Contributors

`vSCAD` has been developed based on research and development needs at [FLOWLab](https://www.flowphysicslab.com/), an interdisciplinary research group focusing on flow physics and transport phenomena in biofluid systems led by **Prof. Debanjan Mukherjee** (email: debanjan@Colorado.Edu) at the *University of Colorado, Boulder*. The lead developer and researcher for `vSCAD` software toolkit project is doctoral student **Nick Rovito** (email: nick.rovito@Colorado.Edu).
