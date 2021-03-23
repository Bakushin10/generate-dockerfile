from abc import ABC, abstractmethod, ABCMeta

class dockerfileGeneratorInterface(metaclass=ABCMeta):
    
    def __init__(self):
        super().__init__()

    @abstractmethod
    def generate(self):
        """
            generate Dockerfile
        """
        raise NotImplementedError()
    
    @abstractmethod
    def questions(self):
        """
            method to ask question for Dockerfile
            - project name
            - dependency and its version
        """
        raise NotImplementedError()
    
