class Civilisation:
  
    def __init__(self, name, region):
        self.name = name
        self.region = region

    def __repr__(self):
        return "<Civilisation name:%s region:%s>" % (self.name, self.region)
