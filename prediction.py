"""import requests


city = "New Delhi"
country = "IN"
url = "http://api.openweathermap.org/data/2.5/forecast?q={},in&appid={}".format(city,api_key)
data = requests.get(url)
data = data.json()
print(data['list'])
print(data['weather'][0]['description'])"""

# Machine learning Prediction

# thermometer to measure temperature
# barometer to measure air pressure
# anemometers to measure wind speed
# traditional methods uses complex numerical forecast equations on the above parameters
# for predicting we require certain input parameters like humidity,dewpoint,pressure etc
# so according to the geographical regions we are extracting the data like humidity,pressure for that particular region
# from internet using a particular API i.e Open Weather Map API

import pandas as pd
import numpy as np

api_key = "d0d88a594db2d6a6496f363ff2c432f5"

df1 = pd.read_csv("weather_pred.csv").set_index("date")
df1["mintemp"] = df1["mintempm"]
df1["maxtemp"] = df1["maxtempm"]
df1["meantemp"] = df1["meantempm"]
df1 = df1.drop("maxtempm",1)
df1 = df1.drop("mintempm",1)
df1 = df1.drop("meantempm",1)
df1 = df1.drop("mindewptm",1)
df1["maxdewptm"] = (df1["maxhumidity"]+df1["minhumidity"])/2
df1 = df1.rename(columns={"maxdewptm":"meanhumidity"})
# here we are updating the dataframe not the actual table so it remains same as previous
# to update actual table write
# df1.to_csv("filename")
x = df1.iloc[:,1:7]
#y1=df1["meantemp"]
#y2=df1["maxtemp"]
#y3=df1["mintemp"]
#y4=df1["precipm"]
y1 = df1.iloc[:,-3:]

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y1,test_size=8,random_state=7)
from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(x_train,y_train)
y_pred=reg.predict(x_test)
print(y_pred)
print(y_test)
from sklearn.metrics import r2_score
print(r2_score(y_test,y_pred))   #accuracy score

from datetime import datetime,timedelta
import requests
api_address='http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID={}&q='.format(api_key)
city = input('City Name :')
url = api_address + city
response=requests.get(url)
json_res=response.json()
    #print(json_res['list'][i]['dt_txt'][0:10])
    #print((datetime.now()+timedelta(i)).strftime('%Y-%m-%d'))
    # or
   # print((datetime.now()+timedelta(days=i)).strftime('%Y-%m-%d'))
j=0
sum1=0
sum2=0
count=0
s=0
mean_h=[]
mean_p=[]
max_h=[]
min_h=[]
max_p=[]
min_p=[]
max_h1=json_res['list'][0]['main']['humidity']
min_h1=json_res['list'][0]['main']['humidity']
max_p1=json_res['list'][0]['main']['pressure']
min_p1=json_res['list'][0]['main']['pressure']
for i in json_res['list']:
    if((datetime.now()+timedelta(j)).strftime('%Y-%m-%d')==json_res['list'][s]['dt_txt'][0:10]):
        sum1=sum1+json_res['list'][s]['main']['humidity'] 
        sum2=sum2+json_res['list'][s]['main']['pressure']
        if(max_h1<json_res['list'][s]['main']['humidity']):
            max_h1=json_res['list'][s]['main']['humidity']
        elif(min_h1>json_res['list'][s]['main']['humidity']):
            min_h1=json_res['list'][s]['main']['humidity']
        if(max_p1<json_res['list'][s]['main']['pressure']):
            max_p1=json_res['list'][s]['main']['pressure']
        elif(min_p1>json_res['list'][s]['main']['pressure']):
            min_p1=json_res['list'][s]['main']['pressure']   
        count=count+1
        s=s+1
        print((datetime.now()+timedelta(j)).strftime('%Y-%m-%d'))
        print(count)
    else:
        print(count)
        avg1=sum1/count
        avg2=sum2/count
        j=j+1
        count=0
        sum1=0
        sum2=0
        mean_h.append(avg1)
        mean_p.append(avg2)
        max_h.append(max_h1)
        min_h.append(min_h1)
        max_p.append(max_p1)
        min_p.append(min_p1)
        sum1=sum1+json_res['list'][s]['main']['humidity'] 
        sum2=sum2+json_res['list'][s]['main']['pressure']
        max_h1=json_res['list'][s]['main']['humidity']
        min_h1=json_res['list'][s]['main']['humidity']
        max_p1=json_res['list'][s]['main']['pressure']
        min_p1=json_res['list'][s]['main']['pressure']
        count=count+1
        #print((datetime.now()+timedelta(j)).strftime('%Y-%m-%d'))
        #print(count)
        s=s+1
avg1=sum1/count
avg2=sum2/count       
mean_h.append(avg1)
mean_p.append(avg2)
max_h.append(max_h1)
min_h.append(min_h1)
max_p.append(max_p1)
min_p.append(min_p1)
       
print(mean_h)
print(mean_p)
print(max_h)
print(min_h)
print(max_p)
print(min_p)
for i in range(0,5):
    l=[]
    l.append(mean_p[i])
    l.append(max_h[i])
    l.append(min_h[i])
    l.append(mean_h[i])
    l.append(max_p[i])
    l.append(min_p[i])
    q=np.array(l)
    y_pred=reg.predict(q.reshape(1,-1))
    print("DAY ",i+1,y_pred)
