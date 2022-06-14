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


ser2_iterable = 0
if ser2:
    while ser2_iterable < 10 and not ser2_connected:
        try:
            ser2 = serial.Serial("/dev/cu.usbmodem14201", 9600, timeout=5)
            ser2_connected = True
        except serial.serialutil.SerialException:
            print("Serial 2 port didnt connect.")
            ser2_iterable += 1
            ser2_connected = False


while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if ser1_connected:
        input_str1 = ser1.readline().decode("utf-8").strip()
        print(input_str1)

        input_list1 = input_str1.split(",")
        if input_list1
        print('Data from probe ', input_list1[4], ';',
              'Methane: ', input_list1[0],
              'Hydrogen: ', input_list1[1],
              'Temperature: ', input_list1[2],
              'Humidity: ', input_list1[3], )

    if ser2_connected:
        input_str2 = ser2.readline().decode("utf-8").strip()
        print(input_str2)

        input_list2 = input_str2.split(",")
        print(input_list2)
        print('Data from probe ', input_list2[4], ';',
              'Methane: ', input_list2[0],
              'Hydrogen: ', input_list2[1],
              'Temperature: ', input_list2[2],
              'Humidity: ', input_list2[3], )


