import numpy as np
import sys
import vtktools
#import pyvista as pv
from Variables import x_max, x_min, defaultFilePath
from Norm import normalise, denormalise

def get_tracer(fileNumber):
    """
    Used to get the Tracers as a numpy array corresponding to a vtu file from the Fluids dataset.
    Note this normalises the returned array.
    :param fileNumber: int or string
        Used to identify which vtu file to return
        Values are between 0 and 988
    :return: numpy array
        Tracers are returned as numpy array
    """
    folderPath = defaultFilePath + '/small3DLSBU'
    filePath = folderPath + '/LSBU_' + str(fileNumber) + '.vtu'
    sys.path.append('fluidity-master')
    ug = vtktools.vtu(filePath)
    ug.GetFieldNames()
    p = ug.GetScalarField('Tracer')
    p = np.array(p)

    # Normalise p
    p = normalise(p, x_min, x_max)
    # Convert p into 1 x N array
    p = np.array([p[:]])
    return p

def get_prediction_tracer(fileNumber):
    """
    Used to get the Tracers as a numpy array corresponding to a vtu file from the Fluids dataset .
    Note this normalises the returned array.
    :param fileNumber: int or string
        Used to identify which vtu file to return
        Values are between 0 and 988
    :return: numpy array
        Tracers are returned as numpy array
    """
    networkName = 'tDA2' # Change this to prediction folder name

    folderPath = defaultFilePath + '/' + networkName
    filePath = folderPath + '/' + networkName + '_' + str(fileNumber) + '.vtu' 
    sys.path.append('fluidity-master')
    ug = vtktools.vtu(filePath)
    ug.GetFieldNames()
    p = ug.GetScalarField('Latent-GAN')
    p = np.array(p)

    # Normalise p
    p = normalise(p, x_min, x_max)
    # Convert p into 1 x N array
    p = np.array([p[:]])
    return p

###### LEGACY ######
# def get_tracer_from_latent(fileNumber):
#     """
#     Used to get the Tracers as a numpy array corresponding to a .csv file from 
#     the Latent dataset 
#     :param fileNumber: int or string
#         Used to identify which vtu file to return
#         Values are between 0 and 988
#     :return: numpy array
#         Tracers are returned as numpy array
#     """
#     folderPath = defaultFilePath + '/LatentSpace'
#     filePath = folderPath + '/LS_' + str(fileNumber) + '.csv'
#     p = np.loadtxt(filePath, delimiter=",")
#     return p