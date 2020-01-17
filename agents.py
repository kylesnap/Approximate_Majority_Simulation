from typing import List

class Agent:

    def __init__(self, id, state) -> None:
        self.id : int = id
        self.state : str = state
        self.__learnt : int = -1 #Set to -1 if haven't learnt yet.

    def __str__(self):
        return str("ID: %5d, State: %c" % (self.id, self.state))

    

    
    

    

    

    