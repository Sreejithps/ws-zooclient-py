from abc import ABCMeta, abstractmethod


class GenericClientABC(ABCMeta):
    """abstract class for web service invoker"""
    @abstractmethod
    def ProcessRequest(self, inputcontext, params):
        pass
    
    @abstractmethod
    def GetInputs(self):
        pass    

    
