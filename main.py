import serial
import pandas as pd
import csv
from datetime import datetime
import serial.tools.list_ports as ports

e = None

# Parameters
sensor_count = 2

device_ports = list(ports.comports())  # create a list of serial ports
for i in device_ports:
    try:
        print('Trying to connect port: ', i)
        ser = serial.Serial(i, 9600, timeout=5)
    except serial.serialutil.SerialException:
        print('RX not here, checking next port...')
    except Exception as e:
        print(e)
        exit()


def csv_writer(sensor):
    csv_file = 'sensor' + str(sensor) + '.csv'

    try:
        with open(csv_file, 'a') as csvfile:
            data_df = csv.writer(csvfile)

            data_df.writerow([input_list[0], input_list[1], input_list[2],
                              input_list[3], current_time])

            print("Data Addition Completed")

    except Exception as e:
        print(e)


for i in range(sensor_count):
    file_name = './sensor' + str(i) + '.csv'
    with open(file_name, 'r+') as csvfile:
        c = csv.writer(csvfile, delimiter=',',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)

        c.writerow(['methane', 'hydrogen', 'temperature', 'humidity', 'time'])

# read from Arduino
input_str = ser.readline()
print("Read input" + input_str.decode("utf-8").strip() + " from Arduino")

d = {'methane', 'hydrogen', 'temperature', 'humidity'}

df = pd.DataFrame(data=d)

while 1:

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    input_str = ser.readline().decode("utf-8").strip()
    print(input_str)

    input_list = input_str.split(",")

    if input_list[4] <= sensor_count:

        print('Data from probe ', input_list[4], ';',
              'Methane: ', input_list[0],
              'Hydrogen: ', input_list[1],
              'Temperature: ', input_list[2],
              'Humidity: ', input_list[3], )

    else:
        print("Data was not received well. Check connection of ", previousReception + 1, ".")

    csv_writer(input_list[4])
    previousReception = input_list[4]
