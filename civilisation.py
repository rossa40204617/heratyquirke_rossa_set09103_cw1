class Civilisation:
  
    def __init__(self, name, region, time_period):
        self.name = name
        self.region = region
        self.time_period = time_period

    def __repr__(self):
        return "<Civilisation name:%s region:%s time_period:%s>" % (self.name, self.region, self.time_period)
