import numpy as np 
import pandas as pd 

class ImageJReader():
    def __init__():
        return
    
    def get_path(csv_path):
        '''
        Returns the path of the vessel as a list of points

        Parameters
        ----------  
        csv_path : str
            The path to the CSV file containing the vessel data.
        Returns
        -------
        np.ndarray
            A 2D numpy array where each row represents a point in the vessel path.
            The first two columns are the X and Y coordinates, and the third column is filled with zeros.
        '''
        data = pd.read_csv(csv_path)
        coordinates = data[['X', 'Y']].to_numpy()
        zeros_column = np.zeros((coordinates.shape[0], 1))
        
        return np.hstack((coordinates, zeros_column)) 
    
    def get_diam(csv_path):
        '''
        Returns the diameters of the vessel as a list of diameters

        Parameters
        ----------
        csv_path : str
            The path to the CSV file containing the vessel data.
        Returns
        -------
        np.ndarray
            A 1D numpy array containing the diameters of the vessel.
        '''
        data = pd.read_csv(csv_path)
        return data['Length'].to_numpy().flatten()
        

        
        
        
 