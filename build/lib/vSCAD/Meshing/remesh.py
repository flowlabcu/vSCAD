import numpy as np
import os
import sys

import pymeshlab
from pymeshlab import PercentageValue, PureValue

class Remesh():
    def __init__(self, stl_path):
        self.stl_path = stl_path
        self.init_target_length_percentage = 0.4
        self.final_target_length_percentage = 0.1
        self.target_length_reduction_step_size = 0.1
        self.isotropic_remeshing_iterations = 3
        self.recursive_smoothing_iterations = 10
        self.final_smoothing_iterations = 50
        self.saveout_period = 10

    def set_initial_target_length_percentage(self, target_length_percentage):
        self.init_target_length_percentage = target_length_percentage
        
    def set_final_target_length_percentage(self, target_length_percentage):
        self.final_target_length_percentage = target_length_percentage

    def set_target_length_reduction_step_size(self, target_length_reduction_step_size):
        self.target_length_reduction_step_size = target_length_reduction_step_size

    def set_target_length_reduction_step_size(self, target_length_reduction_step_size):
        self.target_length_reduction_step_size = target_length_reduction_step_size

    def set_isotropic_remeshing_iterations(self, isotropic_remeshing_iterations):
        self.isotropic_remeshing_iterations = isotropic_remeshing_iterations

    def set_recursive_smoothing_iterations(self, recursive_smoothing_iterations):
        self.recursive_smoothing_iterations = recursive_smoothing_iterations

    def set_final_smoothing_iterations(self, final_smoothing_iterations):
        self.final_smoothing_iterations = final_smoothing_iterations

    def set_saveout_period(self, saveout_period):
        self.saveout_period = saveout_period

    def remesh_stl(self):
        '''
        Remesh the STL file using PyMeshLab.
        '''
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(self.stl_path)
        ms.save_current_mesh('scad-stl/original-mesh.stl')

        percent = self.init_target_length_percentage

        count = 0
        while percent > self.final_target_length_percentage:
            print(f'Remeshing step {count+1}')
            print('     Removing duplicate vertices...')
            ms.apply_filter('meshing_remove_duplicate_vertices')
            
            print('     Removing duplicate faces...')
            ms.apply_filter('meshing_remove_duplicate_faces')
            
            print('     Removing unreferenced vertices...')
            ms.apply_filter('meshing_remove_unreferenced_vertices')
            
            print('     Repairing non-manifold edges...')
            ms.apply_filter('meshing_repair_non_manifold_edges')
            ms.apply_filter('meshing_repair_non_manifold_vertices')
            
            print('     Merging close vertices...')
            ms.apply_filter('meshing_merge_close_vertices',)

            ms.apply_filter('meshing_repair_non_manifold_edges')
            ms.apply_filter('meshing_repair_non_manifold_vertices')

            print('     Closing holes...')
            ms.apply_filter('meshing_close_holes')

            print('     Isotropic remeshing...')
            ms.apply_filter('meshing_isotropic_explicit_remeshing', 
                            iterations=self.isotropic_remeshing_iterations, 
                            targetlen = PercentageValue(percent))
            
            print('     Smoothing...')
            ms.apply_filter('apply_coord_laplacian_smoothing_surface_preserving', 
                            iterations=self.recursive_smoothing_iterations, angledeg=1)
            
            ms.apply_filter('meshing_merge_close_vertices')

            if count %self.saveout_period == 0:
                ms.save_current_mesh(f'scad-stl/mesh-{count+1}.stl')

            count += 1 
            percent -= self.target_length_reduction_step_size
        
        print('Applying final smoothing...')
        ms.apply_filter('apply_coord_laplacian_smoothing_surface_preserving', 
                        iterations=self.final_smoothing_iterations, angledeg=1.0)

        ms.apply_filter('meshing_remove_duplicate_vertices')
        ms.apply_filter('meshing_remove_duplicate_faces')
        ms.apply_filter('meshing_remove_unreferenced_vertices')
        ms.apply_filter('meshing_repair_non_manifold_edges')
        ms.apply_filter('meshing_merge_close_vertices')

        print('Saving final mesh')
        ms.save_current_mesh(self.stl_path)
        
        return