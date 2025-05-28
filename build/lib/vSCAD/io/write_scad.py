import numpy 
import os
import subprocess 
import sys 

class SCADFile():
    def __init__(self, file_name):
        self.file_name = file_name
        self.path = 'scad/' + self.file_name
        self.create_file()
        self.modules = OpenSCADFunctions(self.path)
        
    def create_file(self):
        '''
        Create a new SCAD file.
        '''
        with open(self.path, 'w') as f:
            f.write(f'// OpenSCAD file\n')
            f.write(f'// Created with vSCAD\n\n')
            f.write(f'// ------------------------------------\n')

        return
    
    def import_vessel(self, vessel):
        '''
        Import a vessel data into the SCAD file.

        Parameters: 
        - vessel: Vessel object
        '''
        with open(self.path, 'a') as f:
            f.write(f'// Import vessel\n')
            f.write(f'// {vessel.name} path\n')
            f.write(f'{vessel.name}_path = [\n')
            for point in vessel.path:
                f.write(f'    [{point[0]}, {point[1]}, {point[2]}],\n')
            f.write(f'];\n\n')
            
            f.write(f'// {vessel.name} diameters\n')
            f.write(f'{vessel.name}_diameters = [\n')
            for diam in vessel.diameters:
                f.write(f'    {diam},\n')
            f.write(f'];\n\n')
            
            
            f.write(f'// {vessel.name} euler angles\n')
            f.write(f'{vessel.name}_euler_angles = [\n')
            for angle in vessel.euler_angles:
                f.write(f'    [{angle[0]}, {angle[1]}, {angle[2]}],\n')
            f.write(f'];\n\n')
            
            f.write(f'// ------------------------------------\n')

    def write_stl(self, custom_name=None):
        '''
        Write the SCAD file to an STL file.

        Parameters: 
        - custom_name: str, optional
            Custom name for the STL file. If not provided, the STL file will be named after the SCAD file.
        '''
        if custom_name:
            self.stl_path = f'scad-stl/{custom_name}'

        else:
            self.stl_path = f'scad-stl/{self.file_name}.stl'
        
        try:
            result = subprocess.run(['mkdir', '-p', 'scad-stl'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e.stderr.decode('utf-8')}")

        print('Writing stl file. This may take some time...')
        subprocess.run(['openscad', '-o', self.stl_path, self.path], check=True)
        print(f'SCAD file written to {self.stl_path}')
        return 

class OpenSCADFunctions():
    def __init__(self, path):
        self.path = path
        self.fragments = 25
        self.thickness = 0.01

    def set_thickness(self, thickness):
        '''
        Set the thickness of the lofted circle.
        '''
        self.thickness = thickness
        
    def set_fragments(self, fragments):
        '''
        Set the number of fragments for OpenSCAD to draw circles.
        '''
        self.fragments = fragments

    def import_circle_at(self):
        '''
        Import the circle_at module into the SCAD file.
        
        The circle at function creates a cylinder with a given diameter and angle.
        OpenSCAD cannot loft (hold()) circles (or other 2D objects), so we 
        create a cylinder with a small height (0.01) to represent the lofted circle. 
        '''
        with open(self.path, 'a') as f:
            f.write(f'// Circle at\n')
            f.write(f'module circle_at(position, diameter, angle) {{ \n')
            f.write(f'    translate(position) {{\n')
            f.write(f'        rotate(angle) {{\n')
            f.write(f'            cylinder({self.thickness}, d = diameter, $fn={self.fragments});\n')
            f.write(f'        }}\n')
            f.write(f'    }}\n')
            f.write(f'}}\n\n')
            f.write(f'// ------------------------------------\n')

    def import_loft_path(self):
        '''
        Import the loft_path module into the SCAD file.
        '''
        with open(self.path, 'a') as f:
            f.write(f'// Loft path\n')
            f.write(f'module loft_path(path, diameters, euler_angles) {{\n')
            f.write(f'    for (i = [0 : len(path) - 2]) {{\n')
            f.write(f'        hull() {{\n')
            f.write(f'            circle_at(path[i], diameters[i], euler_angles[i]);\n')
            f.write(f'            circle_at(path[i + 1], diameters[i + 1], euler_angles[i + 1]);\n')
            f.write(f'        }}\n')
            f.write(f'    }}\n')
            f.write(f'}}\n\n')
            f.write(f'// ------------------------------------\n')
        
    def function_loft_path(self, vessel):
        '''
        Create a loft path function in OpenSCAD for a given vessel.
        '''
        with open(self.path, 'a') as f:
            f.write(f'// Loft path of {vessel.name}\n')
            f.write(f'loft_path({vessel.name}_path, {vessel.name}_diameters, {vessel.name}_euler_angles);\n')
            f.write(f'// ------------------------------------\n')
    
    def start_union(self):
        '''
        Start a union block in the SCAD file.
        '''
        with open(self.path, 'a') as f:
            f.write(f'union() {{\n')

    def end_union(self):
        '''
        End a union block in the SCAD file.
        '''
        with open(self.path, 'a') as f:
            f.write(f'}}\n')
            f.write(f'// ------------------------------------\n')
                                                                