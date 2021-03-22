import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi


class ESP_Tools():
    def __init__(self, ssid_input, pwd_input, channel = 1221440, thingspeak_api_key = 'E22PR7IQ5E7IVKHT'):
        self._ssid = ssid_input
        self._pwd = pwd_input
        self._channel_ID = channel
        self._api_key = thingspeak_api_key
        self.setup()
       
       
    def setup(self):
       
        esp32_cs = DigitalInOut(board.D13)
        esp32_ready = DigitalInOut(board.D11)
        esp32_reset = DigitalInOut(board.D12)
       
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
       
        requests.set_socket(socket, esp)

        if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
            print("ESP32 found and in idle mode")
           
           
        print("Connecting to network")
        while not esp.is_connected:
            try:
                esp.connect_AP(self._ssid, self._pwd)
            except RuntimeError as e:
                print("could not connect to AP, retrying: ", e)
                continue
        print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
        print("My IP address is", esp.pretty_ip(esp.ip_address))
       
       
    def push_to_field(self, field, data):
        request_msg = "https://api.thingspeak.com/update?api_key={}&field{}={}".format(self._api_key,field,data)
        print(request_msg)
        try:
            r = requests.get(request_msg)
            response = r.text
            r.close()
        except RuntimeError as e:
            print("could not complete request error: ", e)
            return e
        return response
       
       
       
    #Returns the json given from the pull request
    def pull_from_field(self, field, number_of_results = 1):
        request_msg = "https://api.thingspeak.com/channels/{}/fields/{}.json?results={}".format(self._channel_ID, field, number_of_results)
        print(request_msg)
        try:
            r = requests.get(request_msg)
            response = r.json()
            r.close()
        except RuntimeError as e:
            print("could not complete request error: ", e)
            return e
        return response
       

    #Returns the json given from the pull request
    def pull_from_feed(self, number_of_results = 1):
        request_msg = "https://api.thingspeak.com/channels/{}/feeds.json?results={}".format(self._channel_ID,number_of_results)
        r = requests.get(request_msg)
        response = r.json()
        r.close()
        return response
   

    #Returns the json given from the pull request
    def pull_channel_status_updates(self):
        request_msg = "https://api.thingspeak.com/channels/{}/status.json".format(self._channel_ID)
        r = requests.get(request_msg)
        response = r.json()
        r.close()
        return response

       

##Example
if(True):
    tool_time = ESP_Tools("JamesDesktop", "Gemima12", 1000433, 'TPQROJW5N4FYQDQB')


    print("Testing pushing to a Channel")
    print("pushing '1231' and then '9876' both to field 2")

    tool_time.push_to_field(2, 1231)
    tool_time.push_to_field(2, 9876)

    print("Done")
    print()

    print("testing pulling from a field")
    print("Pulling from field 2 so it should be the same as what I pushed")
    print()

    response = (tool_time.pull_from_field(2,2))



    print()
    print('Done')
