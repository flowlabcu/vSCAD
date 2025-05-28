import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

import numpy as np
import os
import scipy
import sys

import scipy.interpolate

class Vessel():
    def __init__(self, name='vessel'):
        self.name = name
        self.scale_factor = 1.0
        pass

    def set_path(self, path):
        '''
        Sets the path of the vessel as a list of points
        '''
        self.path = path * self.scale_factor
    
    def set_diameters(self, diams):
        '''
        Sets the diameters of the vessel as a list of diameters
        '''
        self.diameters = diams * self.scale_factor

    def set_scale_factor(self, scale_factor):
        '''
        Sets the scale factor for the vessel
        '''
        self.scale_factor = scale_factor

    def get_direction_vectors(self):
        '''
        Determine the direction vectors between each point in the path
        '''
        self.direction_vectors = []
        for i in range(len(self.path) - 1):
            self.direction_vectors.append(GeometricFunctions.get_direction_vector(self.path[i], self.path[i + 1]))
        
        # Sets the last direction vector to be the same as the second to last
        self.direction_vectors.append(self.direction_vectors[-1])
        self.direction_vectors = np.array(self.direction_vectors)

    def get_euler_angles(self):
        '''
        Determine the Euler angles between each point in the path
        '''
        self.euler_angles = []
        for i in range(len(self.direction_vectors)):
            self.euler_angles.append(GeometricFunctions.direction_to_euler(self.direction_vectors[i]))
        
        self.euler_angles = np.array(self.euler_angles)

    def interpolate_paths(self, n):
        self.path = GeometricFunctions.interpolate_coordinates_3d(self.path, n)
        self.diameters = GeometricFunctions.interpolate_scalar(self.diameters, n)

class GeometricFunctions():
    def interpolate_coordinates_3d(points, n):
        '''
        Interpolates a list of points using cubic spline interpolation

        Parameters:
        - points: List of points (3D), formatted as a list of lists
        - n: The number of additional points to add between original point pairs  
        
        Returns:
        - interpolated_points: A list of newly interpolated points
        '''
        points = np.array(points)
        t = np.arange(len(points)) 

        x, y, z = points[:, 0], points[:, 1], points[:, 2]

        # Create cubic spline object from coordinates, we interpolate the coordinates
        # by their index in the points list
        cs_x = scipy.interpolate.CubicSpline(t, x)
        cs_y = scipy.interpolate.CubicSpline(t, y)
        cs_z = scipy.interpolate.CubicSpline(t, z)

        # [0, 0.25, 0.5... example]
        t_fine = np.linspace(0, len(points) - 1, (len(points) - 1) * (n + 1) + 1)

        # Make a new list of x coordinates (interpolated)
        x_fine = cs_x(t_fine)
        y_fine = cs_y(t_fine)
        z_fine = cs_z(t_fine)

        # Combine into list
        return np.vstack((x_fine, y_fine, z_fine)).T

    def interpolate_scalar(scalar_data, n):
        '''
        Interpolates a list of points using cubic spline interpolation

        Parameters:
        - scalar_data: list of scalar
        - n: The number of additional points to add between original point pairs  
        
        Returns:
        - interpolated_scalar: A list of newly interpolated scalars
        '''
        scalar = np.array(scalar_data)
        t = np.arange(len(scalar_data))
        
        # Create cubic spline of scalar data vs index
        cs_scalar = scipy.interpolate.CubicSpline(t, scalar)
        
        # Create finer grid
        t_fine = np.linspace(0, len(scalar) - 1, (len(scalar) - 1) * (n + 1) + 1)
        scalar_fine = cs_scalar(t_fine)

        return scalar_fine

    def get_direction_vector(point1, point2):
        '''
        Calculates the tangent vector between two points

        Parameters:
        - point1: First point
        - point2: Second point

        Returns:
        - tangent_vector: The normalized tangent vector between the two points 
        '''
        return (point2 - point1) / np.linalg.norm(point2 - point1)
    
    def direction_to_euler(direction, normal = None):
        '''
        Converts a direction vector to Euler angles
        
        Parameters: 
            Direction: The direction vector to convert
            Normal: The normal vector of the plane to convert the direction vector to Euler angles, default is [0, 0, 1]
        
        Returns:
            Euler angles in degrees (ZYX rotation)
        '''
        # Default normal vector is [0, 0, 1]
        if normal is None:
            normal = [0, 0, 1]
        
        # Catch the case where the direction vector is [0, 0, 0] (dividing by zero)
        if np.linalg.norm(direction) < 1e-15:
            return [0, 0, 0]
        
        # Normalize vectors, just in case
        normal = normal / np.linalg.norm(normal)
        direction = direction / np.linalg.norm(direction)

        # Calculate the rotation axis and angle
        rotation_axis = np.cross(normal, direction)
        rotation_angle = np.arccos(np.clip(np.dot(normal, direction), -1.0, 1.0)) # clips incase of floating point error

        # If the vector's are parallel, no rataion is needed
        # Also, prevents further division by zero
        if np.linalg.norm(rotation_axis) < 1e-15:
            return [0, 0, 0]
        
        # Normalize the rotation axis
        rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)

        # Compute Rodrigues' rotation formula (rotation matrix)
        K = np.array([
            [0, -rotation_axis[2], rotation_axis[1]],
            [rotation_axis[2], 0, -rotation_axis[0]],
            [-rotation_axis[1], rotation_axis[0], 0]
        ])
        
        I = np.eye(3)

        R = I + np.sin(rotation_angle) * K + (1 - np.cos(rotation_angle)) * np.dot(K, K)

        # Convert rotation matrix to Euler angles
        sin_yaw = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
        singular = sin_yaw < 1e-6

        if not singular:
            yaw = np.arctan2(R[1, 0], R[0, 0]) # rotation about z-axis
            pitch = np.arctan2(-R[2, 0], sin_yaw) # rotation about y-axis
            roll = np.arctan2(R[2, 1], R[2, 2]) # rotation about x-axis
        
        else: # Gimbal lock, two rotation axis aligned
            yaw = np.arctan2(-R[0, 1], R[1, 1])
            pitch = np.arctan2(-R[2, 0], sin_yaw)
            roll = 0

        return np.array([np.degrees(roll), np.degrees(pitch), np.degrees(yaw)])

class BinaryTree():
    class Branch():
        def __init__(self, start_point, end_point, start_diameter, end_diameter, num_points):
            self.start_point = start_point
            self.end_point = end_point
            
            # Generate a set of points and diameters for each branch 
            p = int(num_points) 
            if p < 2:
                p = 2

            self.points = np.array(np.linspace(start_point, end_point, p))
            self.diameters = np.linspace(start_diameter, end_diameter, p)

    def __init__(self, start_point, length, angle, depth, diameter = 2, num_points_base = 100):
        self.start_point = start_point
        self.length = length    
        self.bifurcation_angle = angle  
        self.depth = depth
        self.num_points_base = num_points_base
        self.diameter = diameter
        self.murray_exponent = 3.0
        self.angle = np.pi / 2

    def draw_tree(self):
        '''
        Begins recursive tree generation
        '''
        self.branches = self.generate_tree(self.start_point, self.length, self.diameter, self.num_points_base, self.angle, self.depth)
        return self.branches

    def generate_tree(self, start_point, length, diameter, num_points, angle, depth):
        '''
        Generates a Binary tree

        Parameters:
        - start_point: The starting point of the tree
        - length: The length of the brach
        - diameter: The diameter of the branch
        - num_points: The number of points to generate in the branch
        - angle: The angle of the tree
        - depth: The depth of the tree
        '''
        if depth == 0:
            return []
        
        end_point = start_point + length * np.array([np.cos(angle), np.sin(angle), 0])

        start_diameter = self.calculate_diameter(diameter)
        end_diameter = self.calculate_diameter(start_diameter)
        branch = BinaryTree.Branch(start_point=start_point, 
                                   end_point=end_point, 
                                   start_diameter=start_diameter, 
                                   end_diameter=end_diameter, 
                                   num_points=num_points)
        
        left_branch = self.generate_tree(end_point, 
                                         length * 0.7, 
                                         self.calculate_diameter(diameter),
                                         int(num_points * 0.7), 
                                         angle + self.bifurcation_angle, 
                                         depth - 1)
        
        right_branch = self.generate_tree(end_point, 
                                          length * 0.7, 
                                          self.calculate_diameter(diameter),
                                          int(num_points * 0.7),
                                          angle - self.bifurcation_angle, 
                                          depth - 1)
        
        return [branch] + left_branch + right_branch

    def calculate_diameter(self, diameter):
        return diameter * (2 ** (-1 / self.murray_exponent))

class NodalTree():
    class Branch():
        def __init__(self, start_point, end_point, start_diameter, end_diameter, num_points):
            self.start_point = start_point
            self.end_point = end_point
            
            # Generate a set of points and diameters for each branch 
            p = int(num_points) 
            if p < 2:
                p = 2

            self.points = np.array(np.linspace(start_point, end_point, p))
            self.diameters = np.linspace(start_diameter, end_diameter, p)

    def __init__(self, connectivity, points, diameters, num_points):
        '''
        Parameters:
        - connectivity: Connectivity matrix
            The row index of the matrix represents the branch number. 
            The first column is the starting point of the branch,
            and the second column is the ending point of the branch.
        - points: List of points in 3d space
        - diameters: List of diameters
        - num_points: Number of points to generate per branch
        '''
        self.connectivity = np.array(connectivity)
        self.points = np.array(points)
        self.diameters = np.array(diameters)
        self.num_points = np.array(num_points)

    def draw_tree(self):
        '''
        Generates branch objects for each branch (row) in the 
        connectivity matrix. 

        TO-DO: Add support for different diameters at the start and end of the branch
        '''
        self.branches = []
        for row in self.connectivity:
            start_point = self.points[row[0]]
            end_point = self.points[row[1]]
            start_diameter = self.diameters[row[0]]
            self.branches.append(NodalTree.Branch(start_point=start_point, 
                                                  end_point=end_point, 
                                                  start_diameter=start_diameter, 
                                                  end_diameter=start_diameter, 
                                                  num_points=self.num_points))
            
        return self.branches
        
class Distortions():
    def __init__(self):
        pass

    def add_path_noise(vessel, noise_level=0.1, noise_type='x', hold=3):
        '''
        Adds noise to the path of the vessel

        Parameters:
        - vessel: Vessel object
        - noise_level: The level of noise to add to the path
        '''
        length = np.linalg.norm(vessel.path[0] - vessel.path[-1])
        noise_level = noise_level * length
        
        x = vessel.path[:, 0]
        y = vessel.path[:, 1]
        z = vessel.path[:, 2]

        x_noise = np.random.normal(-noise_level, noise_level, len(x))
        y_noise = np.random.normal(-noise_level, noise_level, len(y))
        z_noise = np.random.normal(-noise_level, noise_level, len(z))

        if noise_type == 'x':
            y_noise = np.zeros(len(y))
            z_noise = np.zeros(len(z))
        
        elif noise_type == 'y':
            x_noise = np.zeros(len(x))
            z_noise = np.zeros(len(z))

        elif noise_type == 'z':
            x_noise = np.zeros(len(x))
            y_noise = np.zeros(len(y))

        elif noise_type == 'xy':
            z_noise = np.zeros(len(z))
        
        elif noise_type == 'xz':
            y_noise = np.zeros(len(y))

        elif noise_type == 'yz':
            x_noise = np.zeros(len(x))

        elif noise_type == 'all':
            pass

        else:
            print('Invalid noise type, defaulting to all')
        x_noise[:hold] = 0; x_noise[-hold:] = 0
        y_noise[:hold] = 0; y_noise[-hold:] = 0
        z_noise[:hold] = 0; z_noise[-hold:] = 0

        vessel.path[:, 0] = x + x_noise
        vessel.path[:, 1] = y + y_noise
        vessel.path[:, 2] = z + z_noise



