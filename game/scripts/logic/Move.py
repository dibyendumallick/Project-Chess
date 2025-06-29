class Move:
    
    #Initial and Final move squares
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final
        
    #equating two Move objects
    def __eq__(self, value):
        return self.initial == value.initial and self.final == value.final