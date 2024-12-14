class Radiometer:
    def __init__(self,input_with_uncertainty=False):
       self.With_Uncertainty = input_with_uncertainty
       self.Integration_Time_Sec = []
       self.Bandwidth_MHz = []
    
    def detection_probability(self):
        if not self.With_Uncertainty:
            # do something
            return 1
        else:
            #do something else
            return 1