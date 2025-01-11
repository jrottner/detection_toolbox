import radios
from propagation import FreeSpace

tx = radios.Transmitter.TransmitterClass(10,"isotropic",0,0)
dg = radios.Detector_Grid.Detector_GridClass()

path_loss_test = FreeSpace.FreeSpaceClass()

path_loss_test.path_loss(tx,dg)
