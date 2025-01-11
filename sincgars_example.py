import radios
from propagation import FreeSpace

fc = 80e6 # carrier freq at 80 MHz (Sincgars)

tx = radios.Transmitter.TransmitterClass(10,"Isotropic",fc, "SINCGARS", 0,0)
dg = radios.Detector_Grid.Detector_GridClass()

path_loss_test = FreeSpace.FreeSpaceClass()

path_loss_test.path_loss(tx,dg)
