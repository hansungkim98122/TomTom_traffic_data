import requests
import json
from datetime import datetime
import schedule
import time

def callTomTomAPI(url,coordinate, APIkey, name):

    #Define request object
    params = {'key': APIkey, 'point': coordinate, 'format': 'json'}
    response = requests.get(url,params=params)


    data = response.json()

    # Serializing json
    json_object = json.dumps(data)

    save_dir = '/home/hansung/Repository/TomTom/TrafficData/'
    time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    name = 'traffic_flow_data_' + time + '_' + name +'.json'
    filename = save_dir + name

    with open(filename, "w") as outfile:
        outfile.write(json_object)
    print(f'{name}-file saved'.center(80,'#'))

def traffic_data_query():
    APIkey = 'UFWWJ1cwavLuAVxB8N6eOV9cXXlGYAIH'
    url = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json'

    coordinates = ['37.439643, -122.162922', '37.437300, -122.160224' , '37.432518, -122.154788', '37.429964, -122.151870','37.427704, -122.149300','37.425556, -122.146865','37.425040, -122.146024','37.4230729357566, -122.14223053565247','37.421126797450704, -122.13852715752465','37.419129353825056, -122.1346571365209','37.41756548960628, -122.13167769683619','37.416757718706585, -122.13013035417022','37.4157158321831, -122.1282556966762','37.41200750590724, -122.12472780007374','37.41042439234972, -122.12344785742778','37.4067369126977, -122.12046503212848']
    name_arr = ['1001','1002','1003','1004','1005','1006','1007','1008','1009','1010','1011','1012','1013','1014','1015','1016'] #intersection ID on ECR

    '''
    See https://caconnectedvehicletestbed.org/datasample 
    1001: Medical Foundation Dr
    1002: Embarcadero Rd
    1003: Churchill Ave
    1004: Serra St/Park Blvd
    1005: Stanford Ave	
    1006: Cambridge Ave
    1007: S California Ave
    1008: Page Mill Rd
    1009: Portage/Hansen
    1010: Matadero Ave
    1011: Curtner Ave
    1012: Ventura Ave
    1013: Los Robles Ave
    1014: Maybell Ave
    1015: W Charleston Ave
    1016: Dinah CT
    '''
    for i, coordinate in enumerate(coordinates):
        callTomTomAPI(url=url,coordinate=coordinate,APIkey=APIkey,name= name_arr[i])


if __name__ == '__main__':

    for hour in range(7,22):
        schedule.every().hour.at("{0:02d}".format(hour)+":00").do(traffic_data_query)
        
    print('Traffic Data Colletion Started...'.center(80,'*'))
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
