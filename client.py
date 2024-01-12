import requests
import xmltodict
import time
from datetime import datetime
import json
from firebase_admin import db
import firebase_admin

url_str ='http://resource.data.one.gov.hk/td/jss/Journeytimev2.xml'
weather_api ='https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc'

cred_obj = firebase_admin.credentials.Certificate("./journeybase-644f6-firebase-adminsdk-x9igp-186e712fa3.json")
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://journeybase-644f6-default-rtdb.asia-southeast1.firebasedatabase.app/'
	})

pre_data=[0,0,0,0,0,0,0]
data_to_store={}
temperature_to_store=0
hum=0
update_data=[]
json_array=[]
status = True
value_to_store=False
jour_interval = 2

client_jour_read_time = 2
client_temp_read_time =60
first_time_start_up=True



def adjust_reading_time():
    global client_temp_read_time ,client_jour_read_time
    client_jour_read_time = 2
    client_temp_read_time = 60


while True:
    my_time = datetime.now()
    my_hour = my_time.hour
    my_minutes = my_time.minute
    my_second = my_time.second






    if ((my_minutes % jour_interval==0 and my_second == 0) or first_time_start_up==True ):

        print(my_minutes)
        print(my_second)
        try:
            text_str = requests.get(url_str)
            dict_data = xmltodict.parse(text_str.content)
            data = dict_data["jtis_journey_list"]['jtis_journey_time']
            H2_CH = next((index for (index, d) in enumerate(data) if d["LOCATION_ID"] == "H2" and d["DESTINATION_ID"] == "CH"),
                         None)
            H2_EH = next((index for (index, d) in enumerate(data) if d["LOCATION_ID"] == "H2" and d["DESTINATION_ID"] == "EH"),
                         None)
            H2_WH = next((index for (index, d) in enumerate(data) if d["LOCATION_ID"] == "H2" and d["DESTINATION_ID"] == "WH"),
                         None)
            K02_CH = next(
                (index for (index, d) in enumerate(data) if d["LOCATION_ID"] == "K02" and d["DESTINATION_ID"] == "CH"), None)
            K02_EH = next(
                (index for (index, d) in enumerate(data) if d["LOCATION_ID"] == "K02" and d["DESTINATION_ID"] == "EH"), None)
            K04_CH = next(
                (index for (index, d) in enumerate(data) if d["LOCATION_ID"] == "K04" and d["DESTINATION_ID"] == "CH"), None)
            K04_WH = next(
                (index for (index, d) in enumerate(data) if d["LOCATION_ID"] == "K04" and d["DESTINATION_ID"] == "WH"), None)

            # 1
            H2_CH_str = "https://api.thingspeak.com/update?api_key=FQHB6D7WC32M98DU&field1=" + data[H2_CH].get(
                "JOURNEY_DATA") + "." + data[H2_CH].get("COLOUR_ID")
            K02_CH_str = "https://api.thingspeak.com/update?api_key=FQHB6D7WC32M98DU&field2=" + data[K02_CH].get(
                "JOURNEY_DATA") + "." + data[K02_CH].get("COLOUR_ID")
            K04_CH_str = "https://api.thingspeak.com/update?api_key=FQHB6D7WC32M98DU&field3=" + data[K04_CH].get(
                "JOURNEY_DATA") + "." + data[K04_CH].get("COLOUR_ID")
            H2_EH_str = "https://api.thingspeak.com/update?api_key=FQHB6D7WC32M98DU&field4=" + data[H2_EH].get(
                "JOURNEY_DATA") + "." + data[H2_EH].get("COLOUR_ID")
            K02_EH_str = "https://api.thingspeak.com/update?api_key=FQHB6D7WC32M98DU&field5=" + data[K02_EH].get(
                "JOURNEY_DATA") + "." + data[K02_EH].get("COLOUR_ID")
            H2_WH_str = "https://api.thingspeak.com/update?api_key=FQHB6D7WC32M98DU&field6=" + data[H2_WH].get(
                "JOURNEY_DATA") + "." + data[H2_WH].get("COLOUR_ID")
            K04_WH_str = "https://api.thingspeak.com/update?api_key=FQHB6D7WC32M98DU&field7=" + data[K04_WH].get(
                "JOURNEY_DATA") + "." + data[K04_WH].get("COLOUR_ID")
            print(data)
           # names = [H2_CH_str, K02_CH_str, K04_CH_str, H2_EH_str, K02_EH_str, H2_WH_str, K04_WH_str]
            update_data = [data[H2_WH].get("JOURNEY_DATA")+ "." + data[H2_WH].get("COLOUR_ID"), data[H2_CH].get("JOURNEY_DATA")+ "." + data[H2_CH].get("COLOUR_ID"), data[H2_EH].get("JOURNEY_DATA")+ "." + data[H2_EH].get("COLOUR_ID"),
                        data[K04_WH].get("JOURNEY_DATA")+ "." + data[K04_WH].get("COLOUR_ID"),0, data[K04_CH].get("JOURNEY_DATA")+ "." + data[K04_CH].get("COLOUR_ID"), data[K02_CH].get("JOURNEY_DATA")+ "." + data[K02_CH].get("COLOUR_ID"),
                        0,data[K02_EH].get("JOURNEY_DATA")+ "." + data[K02_EH].get("COLOUR_ID")]

            value_to_store=True


            get_field = requests.get(weather_api).json()

            if ((my_minutes == 0 and my_second == 0) or first_time_start_up ==True):
                print(my_minutes)
                print(my_second)
                hum=get_field["humidity"]['data'][0]['value']
                for attrs in get_field["temperature"]['data']:
                    if attrs['place'] == '香港天文台':
                        temperature_to_store = attrs['value']

                value_to_store=True

            if value_to_store==True:
                data_to_store["jour"] = update_data
                data_to_store["temp"] = temperature_to_store
                data_to_store["humidity"] = hum
                data_to_store["temp_interval"]=client_temp_read_time
                data_to_store["jour_interval"] = client_jour_read_time

                json_array.append(data_to_store)
                #jsonFile = open("./data.json", "w")
                #jsonFile.write(json.dumps(json_array))
                #jsonFile.close()
                ref = db.reference("/journey")
                ref.set(json_array)
                value_to_store = False
                first_time_start_up = False
                json_array=[]

                time.sleep(1)
        except Exception as error:
            print("An exception occurred:", error)











