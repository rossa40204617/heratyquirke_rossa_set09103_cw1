class Era:
  
    def __init__(self, name, summary, image, time_periods = [], *args):
        self.name = name
        self.time_periods = time_periods
        self.summary = summary
        self.image = image
