import numpy as np

class Branch():
    def __init__(self, start_point, end_point, start_diameter, end_diameter, num_points):
        '''
        Initializes a Branch object.

        Parameters
        ----------
        start_point : np.ndarray
            The starting point of the branch.
        end_point : np.ndarray
            The ending point of the branch.
        start_diameter : float
            The diameter at the starting point of the branch.
        end_diameter : float
            The diameter at the ending point of the branch.
        num_points : int
            The number of points to generate in the branch.
        '''
        self.start_point = start_point
        self.end_point = end_point
        
        # Generate a set of points and diameters for each branch 
        p = int(num_points) 
        if p < 2:
            p = 2

        self.points = np.array(np.linspace(start_point, end_point, p))
        self.diameters = np.linspace(start_diameter, end_diameter, p)

class BinaryTree():
    def __init__(self, start_point, length, angle, depth, diameter = 2, num_points_base = 100):
        '''
        Initializes a BinaryTree object.

        Parameters
        ----------
        start_point : np.ndarray
            The starting point of the tree.
        length : float
            The length of the main branch.
        angle : float
            The bifurcation angle in radians.
        depth : int
            The depth of the tree.
        diameter : float, optional
            The diameter of the main branch, defaults to 2.
        num_points_base : int, optional
            The number of points to generate in the base branch, defaults to 100.
        '''
        self.start_point = start_point
        self.length = length    
        self.bifurcation_angle = angle  
        self.depth = depth
        self.num_points_base = num_points_base
        self.diameter = diameter
        self.murray_exponent = 3.0
        self.angle = np.pi / 2
        self.branch_length_reduction = 0.7

    def set_murray_exponent(self, exponent):
        '''
        Sets the Murray's law exponent for the tree generation.

        Parameters
        ----------
        exponent : float
            The exponent value to use in Murray's law.
        '''
        self.murray_exponent = exponent

    def set_branch_length_reduction(self, reduction):
        '''
        Sets the branch length reduction factor for the tree generation.

        Parameters
        ----------
        reduction : float
            The reduction factor for branch length.
        '''
        self.branch_length_reduction = reduction

    def draw_tree(self):
        '''
        Begins recursive tree generation.

        Returns
        -------
        list of Branch
            A list of Branch objects representing the generated tree.
        '''
        self.branches = self.generate_tree(self.start_point, self.length, self.diameter, self.num_points_base, self.angle, self.depth)
        return self.branches

    def generate_tree(self, start_point, length, diameter, num_points, angle, depth):
        '''
        Generates a binary tree structure recursively.

        Parameters
        ----------
        start_point : np.ndarray
            The starting point of the current branch as a 3D coordinate.
        length : float
            The length of the current branch.
        diameter : float
            The diameter of the current branch.
        num_points : int
            The number of points to generate along the branch.
        angle : float
            The angle (in radians) of the current branch relative to the parent.
        depth : int
            The remaining depth of recursion (number of branching levels).

        Returns
        -------
        list of Branch
            A list of Branch objects representing the generated tree structure.
        '''
       
        if depth == 0:
            return []
        
        end_point = start_point + length * np.array([np.cos(angle), np.sin(angle), 0])

        start_diameter = self.calculate_diameter(diameter)
        end_diameter = self.calculate_diameter(start_diameter)
        branch = Branch(start_point=start_point, 
                        end_point=end_point, 
                        start_diameter=start_diameter, 
                        end_diameter=end_diameter, 
                        num_points=num_points)
        
        left_branch = self.generate_tree(end_point, 
                                         length * 0.7, 
                                         self.calculate_diameter(diameter),
                                         int(num_points * self.branch_length_reduction), 
                                         angle + self.bifurcation_angle, 
                                         depth - 1)
        
        right_branch = self.generate_tree(end_point, 
                                          length * 0.7, 
                                          self.calculate_diameter(diameter),
                                          int(num_points * self.branch_length_reduction,),
                                          angle - self.bifurcation_angle, 
                                          depth - 1)
        
        return [branch] + left_branch + right_branch

    def calculate_diameter(self, diameter):
        '''
        Calculates the diameter of the branch based on Murray's law.

        Parameters
        ----------
        diameter : float
            The diameter of the parent branch.

        Returns
        -------
        float
            The calculated diameter for the child branch.
        '''
        return diameter * (2 ** (-1 / self.murray_exponent))

class NodalTree():
    def __init__(self, connectivity, points, diameters, num_points):
        '''
        Initializes a NodalTree object.

        Parameters
        ----------
        connectivity : array_like
            Connectivity matrix. The row index of the matrix represents the branch number. 
            The first column is the starting point of the branch, and the second column is the ending point of the branch.
        points : array_like
            List of points in 3D space.
        diameters : array_like
            List of diameters.
        num_points : int
            Number of points to generate per branch.
        '''
        self.connectivity = np.array(connectivity)
        self.points = np.array(points)
        self.diameters = np.array(diameters)
        self.num_points = np.array(num_points)

    def draw_tree(self):
        '''
        Generates branch objects for each branch (row) in the connectivity matrix.

        Returns
        -------
        list of Branch
            A list of Branch objects.
        '''
        self.branches = []
        for row in self.connectivity:
            start_point = self.points[row[0]]
            end_point = self.points[row[1]]
            start_diameter = self.diameters[row[0]]
            end_diameter = self.diameters[row[1]]
            self.branches.append(Branch(start_point=start_point, 
                                        end_point=end_point, 
                                        start_diameter=start_diameter, 
                                        end_diameter=end_diameter, 
                                        num_points=self.num_points))
            
        return self.branches