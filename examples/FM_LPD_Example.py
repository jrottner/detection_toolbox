import radios
from propagation import FreeSpace

tx = radios.Transmitter
dg = radios.Detector_Grid

path_loss_test = FreeSpace

path_loss_test.path_loss(tx,dg)

# in this situation, I would input (power, modulation, location, path loss, link distance)
# I would need to know about detectability (eny array, bandwidth, eny distance)
# I would find (receiver max distance, detector max distance, selectivity metric?)