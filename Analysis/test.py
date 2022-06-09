import serial
import pandas as pd
import csv
from datetime import datetime
import serial.tools.list_ports as ports


device_ports = list(ports.comports())  # create a list of serial ports

print('Trying to connect port: /dev/cu.usbmodem142:01')
ser = serial.Serial(str("/dev/cu.usbmodem14201"), 9600, timeout=5)


while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    input_str = ser.readline().decode("utf-8").strip()
    print(input_str)

    input_list = input_str.split(",")
    try:
        if input_list[4] <= 3:

            print('Data from probe ', input_list[4], ';',
                  'Methane: ', input_list[0],
                  'Hydrogen: ', input_list[1],
                  'Temperature: ', input_list[2],
                  'Humidity: ', input_list[3], )

        else:
            print("Nope")

    except Exception as e:
        print(e)