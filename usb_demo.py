#!/usr/bin/python

# pip install PyUSB

#from numpy import byte
import usb.core
import usb.util

def listen(dev, endpoint_in, endpoint_out):
    while(True):
        try:
            buf = dev.read(endpoint_in.bEndpointAddress,64,1000)
            buf = bytearray(buf)
            if buf[1] > 0:
                print(buf[1])
        except usb.core.USBTimeoutError as e:
            pass

def start():
    dev = usb.core.find(idVendor=0x16C0, idProduct=0x0486)

    if dev is None:
        raise ValueError("Device not found")

    endpoint_in = dev[0][(0,0)][0]
    endpoint_out = dev[0][(0,0)][1]


    try:
        dev.reset()
    except Exception as e:
        print('reset', e)

    #if dev.is_kernel_driver_active(0):
    #    print('detaching kernel driver')
    #    dev.detach_kernel_driver(0)

    listen(dev, endpoint_in, endpoint_out)
    #send command to teensy

    #endpoint_out.write("version".encode() + bytes([0]))

def main():
    try:
        start()
    except usb.core.USBError as e:
        print(e)
        if input("Reconnect (y/n)?") == "y":
            main()

main()