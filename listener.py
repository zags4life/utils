# listener.py

from abc import ABC, abstractmethod

from .closeable import Closeable

class Listener(ABC, Closeable):
    ##########################################################
    # Listener ABC definitions
    ##########################################################

    @abstractmethod
    def start_listener(self):
        pass

    @abstractmethod
    def stop_listener(self):
        pass

    ##########################################################
    # Closeable ABC implementation
    ##########################################################

    def close(self):
        return self.stop_listener()
