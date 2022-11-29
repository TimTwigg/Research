# updated 3 November 2022

from App2 import App

import usb.core
import usb.util

def listen(dev, endpoint_in, endpoint_out):
    app = App()
    while(True):
        try:
            buf = dev.read(endpoint_in.bEndpointAddress, 64, 1000)
            buf = bytearray(buf)
            code = buf[1]
            if code == 0:
                continue
            elif code == 1:
                app.callMaze()
            elif code == 2:
                app.callSound()
        except usb.core.USBTimeoutError as e:
            pass
        except NameError:
            # catches the error thrown by gridReaderFinal when it doesn't find
            # the grid and the 'biggest' variable is not defined.
            print("Could not interpret image. Re-focus camera")

def start():
    dev = usb.core.find(idVendor = 0x16C0, idProduct = 0x0486)

    if dev is None:
        raise ValueError("Device not found")

    endpoint_in = dev[0][(0, 0)][0]
    endpoint_out = dev[0][(0 ,0)][1]

    try:
        dev.reset()
    except Exception as e:
        print("reset", e)

    listen(dev, endpoint_in, endpoint_out)

def main():
    try:
        start()
    except usb.core.USBError as e:
        print(e)
        if input("Reconnect (y/n)?") == "y":
            main()

if __name__ == "__main__":
    main()