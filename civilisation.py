class Civilisation:
  
    def __init__(self, name, region, image, info):
        self.name = name
        self.region = region
        self.image = image
        self.info = info

    def __repr__(self):
        return "<Civilisation name:%s region:%s>" % (self.name, self.region)
