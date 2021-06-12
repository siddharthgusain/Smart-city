# import statements
import Adafruit_DHT as dht
import time
import Adafruit_CharLCD as LCD
import requests
import Adafruit_BMP.BMP085 as BMP085
import spidev

# pin configuration(all sensors)
lcd_rs        = 26  
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 06
lcd_d6        = 05
lcd_d7        = 11
backlight = 21
lcd_columns = 16
lcd_rows    = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,backlight , lcd_columns,lcd_rows)
lcd.enable_display(1)
lcd.clear()

#global varaibles
api="DA72N0VU7B0CGRUD"

# def dht22 + lcd show + api to thinkspeak
def dht22():
   lcd.clear()
   humidity, temperature= dht.read_retry(dht.DHT22,14)
   if humidity is not None and temperature is not None:
      print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature,humidity))
      lcd.message("Temp={0:0.1f}*C\nHumidity={1:0.1f}%".format(temperature,humidity))
      for x in range(0,16):
          lcd.move_right()
          time.sleep(0.6)
      lcd.clear()
      if temperature>35:
          lcd.message("HOT OUTSIDE\nSTAY AT HOME")
          for x in range(0,16):
           lcd.move_right()
           time.sleep(0.6)
          lcd.clear()
      elif temperature<10:
          lcd.message("COLD OUTSIDE\nTAKE PRECAUTIONS")
          for x in range(0,16):
           lcd.move_right()
           time.sleep(0.6)
          lcd.clear()
      else:
          lcd.message("MODERATE TEMP")
          for x in range(0,16):
           lcd.move_right()
           time.sleep(.6)
          lcd.clear() 
      
   else:
      print("failed to get reading")
      lcd.clear()
   return (humidity,temperature)

# def bmp180 + lcd show + api to thinkspeak
def bmp180():
    lcd.clear()
    sensor=BMP085.BMP085()
    pressure=sensor.read_pressure()
    altitude=sensor.read_altitude()
    sea_level=sensor.read_sealevel_pressure()
    print("Pressure={0:0.2f} Pa".format(pressure))
    print("Altitude={0:0.2f} m".format(altitude))
    print("Sealevel Pressure={0:0.2f} Pa".format(sea_level))
    lcd.message ("Pressure={0:0.2f}Pa".format(pressure))
    for x in range(0,16):
           lcd.move_right()
           time.sleep(.6)
    lcd.clear()
    lcd.message("Altitude={0:0.2f}m".format(altitude))
    for x in range(0,16):
           lcd.move_right()
           time.sleep(.6)
    lcd.clear()
    lcd.message("Sealevel\nPressure={0:0.2f}Pa".format(sea_level))
    for x in range(0,16):
           lcd.move_right()
           time.sleep(.6)
    lcd.clear()
    return (pressure,altitude,sea_level)       
# def mq135 code + lcd show + api to thinkspeak
def ReadChannel(channel):
    spi = spidev.SpiDev() 
    spi.open(0, 0)
    spi.max_speed_hz=1000000
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) | adc[2]
    print(data)
    return data
  
def mq135():
    lcd.clear()
    channel0 = ReadChannel(0)
    channel0_perc = format(channel0 * 4.7, '.2f')
    channel0_volt = channel0
    print("CO2 concentration is " + channel0_perc + "ppm (" + str(channel0_volt) + "V).")
    lcd.message("Concentration:{}".format(channel0_perc))
    for x in range(0,16):
          lcd.move_right()
          time.sleep(.6)
    lcd.clear()
    return channel0_perc

# def UV index + lcd show + api call to think speak
def uv_index():
   lcd.clear()
   named_tuple = time.localtime()
   time_string = time.strftime("%m/%d/%Y,%H:%M:%S", named_tuple)
   lat = 28.7041
   lon = 77.1025
   appid = "d0d88a594db2d6a6496f363ff2c432f5"
   city = "delhi"
   url_uv = 'http://api.openweathermap.org/data/2.5/uvi?appid={}&lat={}&lon={}'.format(appid,lat,lon)
   res = requests.get(url_uv)
   UvIndex = res.json()['value']
   print("Today:{}\nUv-Index:{}".format(time_string,UvIndex))
   lcd.message("Today:{}\nUv-Index:{}".format(time_string,UvIndex))
   for x in range(0,16):
             lcd.move_right()
             time.sleep(.6)
   lcd.clear()
   return UvIndex

# def  get call to thinkspeak api for water readings(ph,turbidity,water temp) + lcd show
def water_Quality():
   lcd.clear()
   api = "WE15XY55QOB0YVXW"
   channel_id = "876968"
   field1 = "https://api.thingspeak.com/channels/{}/fields/1.json?api_key={}&results=1".format(channel_id,api)
   r1 = requests.get(field1).json()
   turbidity = r1['feeds'][0]['field1']
   lcd.message("TURBIDITY:{}".format(turbidity))
   for x in range(0,16):
             lcd.move_right()
             time.sleep(.6)
   lcd.clear()
   field2 = "https://api.thingspeak.com/channels/{}/fields/2.json?api_key={}&results=1".format(channel_id,api)
   r2 = requests.get(field2).json()
   pH = r2['feeds'][0]['field2']
   lcd.message("PH:{}".format(pH))
   for x in range(0,16):
             lcd.move_right()
             time.sleep(.6)
   lcd.clear()
   field3 = "https://api.thingspeak.com/channels/{}/fields/3.json?api_key={}&results=1".format(channel_id,api)
   r3 = requests.get(field3).json()
   temp = r3['feeds'][0]['field3']
   lcd.message("WATER TEMP:{}".format(temp))
   for x in range(0,16):
             lcd.move_right()
             time.sleep(.6)
   lcd.clear()
   print("{}\n{}\n{}".format(turbidity,pH,temp))


def water_quality():
    url_water = "https://api.thingspeak.com/channels/876968/feeds.json?api_key=WE15XY55QOB0YVXW"
    res = requests.get(url_water).json()
    arr = res['feeds']
    current = arr[len(arr)-1]
    turb = current['field1']
    ph = current['field2']
    temp = current['field3']
    print("Current Turbidity:{}\nPh:{}\nWater Temperature:{}".format(turb,ph,temp))


while True:
        lcd.clear()
        lcd.message("WELCOME TO\nSMART CITY")
        for x in range(0,16):
             lcd.move_right()
             time.sleep(.6)
        humidity,temperature = dht22()
        pressure,altitude,sea_level = bmp180()
        UvIndex = uv_index()
        channel0_perc = mq135()
        water_quality()
        r= requests.post("https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}&field4={}&field5={}&field6={}&field7={}".format(api,temperature,humidity,pressure,altitude,sea_level,UvIndex,channel0_perc))
        print(r)
