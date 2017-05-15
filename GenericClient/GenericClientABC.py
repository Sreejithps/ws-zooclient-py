from abc import ABCMeta, abstractmethod


class GenericClientABC(ABCMeta):
    """abstract class for web service invoker"""
    @abstractmethod
    def processrequest(self, inputcontext, params):
        pass
    
    @abstractmethod
    def getinputs(self):
        pass    

    @abstractmethod
    def getparams(self):
        pass    

    @abstractmethod
    def setparams(self):
        pass    

    @abstractmethod
    def getservicedesription(self):
        pass    
    
