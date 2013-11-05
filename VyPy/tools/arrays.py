

try:
    import numpy as np
    numpy_isloaded = True
except ImportError:
    numpy_isloaded = False
    
try:
    import scipy as sp
    scipy_isloaded = True
except ImportError:
    scipy_isloaded = False


if numpy_isloaded:
    array_type  = np.ndarray
    matrix_type = np.matrixlib.defmatrix.matrix
else:
    array_type  = None
    matrix_type = None

def vector_distance(X,P=None):
    ''' calculates distance between points in matrix X 
        with each other, or optionally to given point P
        returns min, max and matrix/vector of distances
    '''
    
    # distance matrix among X
    if P is None:
        
        nK,nD = X.shape
        
        d = np.zeros([nK,nK,nD])
        for iD in range(nD):
            d[:,:,iD] = np.array([X[:,iD]])-np.array([X[:,iD]]).T
        D = np.sqrt( np.sum( d**2 , 2 ) )
        
        diag_inf = np.diag( np.ones([nK])*np.inf )
        dmin = np.min(np.min( D + diag_inf ))
        dmax = np.max(np.max( D ))
        
    # distance vector to P
    else:
        P = check_array(P,'row')
        assert P.shape[0] == 1 , 'P must be a horizontal vector'
        D = np.array([ np.sqrt( np.sum( (X-P)**2 , 1 ) ) ]).T
        dmin = D.min()
        dmax = D.max()
        
    return (dmin,dmax,D)


def check_list(val):
    if not isinstance(val,list): val = [val]
    return val

def check_array(A,oned_as='row'):
    ''' ensures A is an array and at least of rank 2
    '''
    if not isinstance(A,np.ndarray):
        A = np.array(A)
    if np.rank(A) < 2:
        A = np.array(np.matrix(A))
        if oned_as == 'row':
            pass
        elif oned_as == 'col':
            A = A.T
        else:
            raise Exception , "oned_as must be 'row' or 'col' "
            
    return A


