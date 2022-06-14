import serial
import pandas as pd
import csv
from datetime import datetime
import serial.tools.list_ports as ports

ser1 = True
ser2 = True
ser1_connected = False
ser2_connected = False

device_ports = list(ports.comports())  # create a list of serial ports
print('List of device ports: ')
print(ports.comports())


ser1_iterable = 0
if ser1:
    while ser1_iterable < 10 and not ser1_connected:
        try:
            ser1 = serial.Serial("/dev/cu.usbmodem14101", 9600, timeout=5)
            ser1_connected = True
        except serial.serialutil.SerialException:
            print("Serial 1 port didnt connect.")
            ser1_iterable += 1
            ser1_connected = False


while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if ser1_connected:
        input_str1 = ser1.readline().decode("utf-8").strip()

    print(input_str1)

    input_list1 = input_str1.split(",")
    try:
        print('Data from probe ', input_list1[4], ';',
              'Methane: ', input_list1[0],
              'Hydrogen: ', input_list1[1],
              'Temperature: ', input_list1[2],
              'Humidity: ', input_list1[3], )

    except Exception as e:
        print(e)
