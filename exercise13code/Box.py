class Box:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    @property
    def width(self):
        return self.max_x-self.min_x

    @property
    def height(self):
        return self.max_y-self.min_y

    @classmethod
    def padded(cls, box, margin):
        return cls(box.min_x-margin,
                   box.max_x+margin,
                   box.min_y-margin,
                   box.max_y+margin)
