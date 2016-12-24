class Profile(object):
    def __init__(self, id, name=""):
        self.images = []
        self.name = name
        self.id = id
    
    def add_image(self, img):
        self.images.append(img)
    
    def set_name(self, name):
        self.name = name


class Image(object):
    def __init__(self, src, location):
        self.src = src
        self.location = location
        