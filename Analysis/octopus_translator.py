import serial
import csv
from datetime import datetime
import serial.tools.list_ports as ports

e = None
search_mode = False
radio_mode = False

# Parameters
sensor_count = 3

# Functions


def csv_writer():
    csv_file = 'sensor_datas.csv'

    try:
      with open(csv_file, 'a') as csvfile:
          data_df = csv.writer(csvfile)

          data_df.writerow([input_list[0], input_list[1], input_list[2], input_list[3], 
                            input_list[4], input_list[5], input_list[6], input_list[7], 
                            input_list[8], input_list[9], input_list[10], input_list[11], 
                            current_time])

          print("Data Addition Completed")

    except Exception as e:
        print(e)

if search_mode:
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
else:
  ser = ''

if radio_mode:
  for i in range(sensor_count):
      file_name = './sensor' + str(i) + '.csv'
      with open(file_name, 'r+') as csvfile:
          c = csv.writer(csvfile, delimiter=',',
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
  
          c.writerow(['methane', 'hydrogen', 'temperature', 'humidity', 'time'])
else:
  file_name = './sensor_datas.csv'
  with open(file_name, 'r+') as csvfile:
      c = csv.writer(csvfile, delimiter=',',
                     quotechar='|', quoting=csv.QUOTE_MINIMAL)

      c.writerow(['methane', 'hydrogen', 'temperature', 'humidity', 'time'])

  
# read from Arduino
input_str = ser.readline()
print("Read input" + input_str.decode("utf-8").strip() + " from Arduino")

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    input_str = ser.readline().decode("utf-8").strip()
    print(input_str)

    input_list = input_str.split(",")
        
    print('Data from probe 1;',
            'Methane: ', input_list[0],
            'Hydrogen: ', input_list[1],
            'Temperature: ', input_list[2],
            'Humidity: ', input_list[3], )
      
    print('Data from probe 2;',
            'Methane: ', input_list[4],
            'Hydrogen: ', input_list[5],
            'Temperature: ', input_list[6],
            'Humidity: ', input_list[7], )
      
    print('Data from probe 3;',
            'Methane: ', input_list[8],
            'Hydrogen: ', input_list[9],
            'Temperature: ', input_list[10],
            'Humidity: ', input_list[11], )

    csv_writer()
