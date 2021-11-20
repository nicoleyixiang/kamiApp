class Button(object):
    
    def __init__(self, name):
        self.name = name
        self.topCoordinate = (0,0)
        self.bottomCoordinate = (0,0)

class ColorButton(Button):

    def __init__(self, name, index):
        self.name = name
        self.index = index