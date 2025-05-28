import numpy as np

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

class BinaryTree():
    def __init__(self, start_point, length, angle, depth, diameter = 2, num_points_base = 100):
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
        self.murray_exponent = exponent

    def set_branch_length_reduction(self, reduction):
        self.branch_length_reduction = reduction

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
        Calculates the diameter of the branch based on the Murray's law
        '''
        return diameter * (2 ** (-1 / self.murray_exponent))

class NodalTree():
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
        connectivity matrix. s
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