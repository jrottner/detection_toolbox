<<<<<<< Updated upstream
class Transmitter():
    def __init__(self):
        self.TX_Power_W = []
        self.Antenna = []
        self.Freq = []
        self.Mod = []
        self.Lat = []
        self.Lon = []
        self.Lat_Lon = []
=======
class TransmitterClass():
    def __init__(self, TX_Power_W, Antenna, Lat, Lon):
        # these should be user specified somewhere
        self.TX_Power_W = TX_Power_W
        self.Antenna = Antenna
        self.Lat = Lat
        self.Lon = Lon
        self.Lat_Lon = [self.Lat,self.Lon]
>>>>>>> Stashed changes
        
    def set_tx_power_W(self,input_power_W):
        self.TX_Power_W = input_power_W
        
    def set_tx_power_dBW(self,input_power_dBW):
        self.TX_Power_W = 10 ** (float(input_power_dBW)/10)
    
    def set_antenna(self,input_antenna):
        self.Antenna = input_antenna

    def set_freq(self, input_freq):
        self.Freq = input_freq

    def set_mod(self, modulation):
        self.Mod = modulation
        # this may be a lot of switch statements for modulation to bandwidth
        
    def set_lat_lon(self,input_ll):
        self.Lat_Lon = input_ll
        self.Lat = input_ll[0]
        self.Lon = input_ll[1]
    
    