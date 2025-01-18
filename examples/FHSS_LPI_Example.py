import radios
from propagation import FreeSpace

tx = radios.Transmitter
dg = radios.Detector_Grid

path_loss_test = FreeSpace

path_loss_test.path_loss(tx,dg)
