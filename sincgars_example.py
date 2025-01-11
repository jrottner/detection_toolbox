import radios
from propagation import FreeSpace

fc = 80e6 # carrier freq at 80 MHz (Sincgars)

radio_position = [0,0]
rx_position = [20,20]
tx = radios.Transmitter.TransmitterClass(10,"Isotropic",fc, "SINCGARS", radio_position[0], radio_position[1])
# dg = radios.Detector_Grid.Detector_GridClass()
# receiver function just computes GO/NOGO. Setup similar to DG will be used for heatmap
rx = radios.Receiver.ReceiverClass(rx_position[0],rx_position[1])

# path_loss_dg = FreeSpace.FreeSpaceClass()

# path_loss_dg.path_loss(tx,dg)

path_loss_rx = FreeSpace.FreeSpaceClass()

print(path_loss_rx.path_loss(tx,rx))