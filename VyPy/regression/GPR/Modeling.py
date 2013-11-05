
import sys, copy, weakref,gc

import numpy as np
import scipy as sp
import scipy.linalg

from VyPy import EvaluationFailure
from VyPy.tools import IndexableDict

import tools
from tools import vector_distance, check_array


class Modeling(object):
    
    def __init__(self,Learn):
        
        # pack
        self.Learn  = Learn
        self.Infer  = Learn.Infer
        self.Kernel = Learn.Kernel
        self.Train  = Learn.Train
        self.Hypers = Learn.Hypers
        
        # useful data
        self.RIE = {}
        self._current = False
        
        # reinterpolated model
        self.RI = None
        
        # try to precalc Kernel
        self.safe_precalc()
        
        return
    
    #: def __init__()
    
    def predict(self,XI):
        
        # will skip if current
        self.safe_precalc()
        
        # prediction
        data = self.Infer.predict(XI)
        
        return data
    
    def safe_precalc(self):
        if self._current:
            return
        
        try:
            self.precalc()
            
        except EvaluationFailure:
            try:
                self.learn()
            except EvaluationFailure:
                raise EvaluationFailure , 'could not precalculate Kernel'
        
        self._current = True
        
        return 
    
    def precalc(self):
        self.Infer.precalc()
        
    def learn(self):
        self.Learn.learn()
            
    def reinterpolate(self):
            
        # new noise param (log10)
        sig_nR = -6.0
        
        # copy model data
        Learn = copy.deepcopy( self.Learn )
        
        new_Model = Modeling( Learn )
        new_Model.safe_precalc()
        
        # kernel output data names
        self.RIE = IndexableDict()
                
        # evaluate training data with model
        X = self.Train.X
        The_Data = new_Model.predict(X)
        
        try:
            The_Data.keys()
        except KeyError:
            raise Exception, 'Kernel must return pack_outputs() to use Modeling.reinterpolate()'
        
        # operate on each training output
        for output in Train.keys():
            
            # check if returned by data
            if output == 'X':
                continue
            
            # pull old data
            D = Train[output]
            if D.shape[0] == 0: continue
            
            # pull new data
            output_i = output + 'I'
            DI = The_Data[output_i]
            
            # calculate errors
            RIE = np.log10( np.mean( np.abs( DI  - D ) ) )
            self.RIE[output] = RIE
            print 'RIE %s: %.4f' % (output,RIE)
            
            # reassign reinterpolated redata
            Train.setitem(output,The_Data[output_i])
            
        #: for each output    
        
        # reinterpolated implies no noise
        new_Model.Hypers.sig_ny  = sig_nR
        new_Model.Hypers.sig_ndy = sig_nR
        
        # store
        self.RI = new_Model
                
        return
    
    #: def reinterpolate()   

     
#: class Modeling()