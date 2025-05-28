import numpy as np 
import pandas as pd 

class ImageJReader():
    def __init__():
        return
    
    def get_path(csv_path):
        '''
        Returns the path of the vessel as a list of points
        '''
        data = pd.read_csv(csv_path)
        coordinates = data[['X', 'Y']].to_numpy()
        zeros_column = np.zeros((coordinates.shape[0], 1))
        
        return np.hstack((coordinates, zeros_column)) 
    
    def get_diam(csv_path):
        '''
        Returns the diameters of the vessel as a list of diameters
        '''
        data = pd.read_csv(csv_path)
        return data['Length'].to_numpy().flatten()
        

        
        
        
 