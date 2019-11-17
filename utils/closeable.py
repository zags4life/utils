from abc import ABCMeta, abstractmethod

class Closeable(object):
    __metaclass__ = ABCMeta
        
    @abstractmethod
    def close(self):
        pass
    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()