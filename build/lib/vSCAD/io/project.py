import os


class vSCADProject():
    def __init__(self, project_name):
        self.project_name = project_name
        self.root = os.path.join(os.getcwd(), project_name)


        self.create_project()

        pass

    def create_project(self):
        self.create_directories()
        self.create_vSCAD_python_file()


    def create_vSCAD_python_file(self):
        '''
        Create a vSCAD python file in the project root directory.
        '''
        path = os.path.join(self.root, 'vscad.py')

        with open(path, 'w') as f:
            f.write(f'import numpy as np\n')
            f.write(f'import os\n')
            f.write(f'import sys\n\n')  
            f.write(f'from vSCAD.Geometry import Vessel\n') 
            f.write(f'from vSCAD.io import ImageJReader\n')
            f.write(f'from vSCAD.io import SCADFile\n\n')
            f.write(f'scad_file = \'{self.project_name}.scad\'\n')
            f.write(f'# Scad file written at scad/{self.project_name}.scad\n\n')

        return



    def create_directories(self):
        '''
        Create directories for a new vSCAD project.
        '''
        directories = ['image_data', 'scad', 'scad-stl']

        try:
            for directory in directories:
                os.makedirs(os.path.join(self.root, directory))

            print(f'Project directories for \'{self.project_name}\' created successfully.')
        
        except Exception as e:
            print(f'An error occurred: {e}')



if __name__ == '__main__':
    '''
    Executable script to create a new vSCAD project in the current working directory.
    '''

    project_name = input('openSCAD project name: ')
    project = vSCADProject(project_name)