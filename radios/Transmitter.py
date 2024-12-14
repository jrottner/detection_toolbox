class Transmitter():
    def __init__(self):
        self.TX_Power_W = []
        self.Antenna = []
        self.Lat = []
        self.Lon = []
        self.Lat_Lon = []
        
    def set_tx_power_W(self,input_power_W):
        self.TX_Power_W = input_power_W
        
    def set_tx_power_dBW(self,input_power_dBW):
        self.TX_Power_W = 10 ** (float(input_power_dBW)/10)
    
    def set_antenna(self,input_antenna):
        self.Antenna = input_antenna
        
    def set_lat_lon(self,input_ll):
        self.Lat_Lon = input_ll
        self.Lat = input_ll[0]
        self.Lon = input_ll[1]
    
    