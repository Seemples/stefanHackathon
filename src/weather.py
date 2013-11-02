from json import load
from urllib2 import urlopen
from pprint import pprint

city="Glasgow" #The city we want information about
    
data = urlopen('http://openweathermap.org/data/2.1/find/name?q='+city)
cities = load(data)
if cities['count'] > 0:
    city = cities['list'][0]
    temp=city['main']['temp']
    temp=str(round(temp-273.15))      #returns in Kelvins; substract 273.15 to get celsius
    print temp.replace(".0","")       # cuts the 0 at the en
    weather=city['weather'][0]['main']   #basic description i.e. rainy/cloudy
    description=city['weather'][0]['description']   #more detailed description i.e. partial/broken clouds
    pressure=city['main']['pressure']   #atmospheric pressure in mmHg(?)
    humidity=city['main']['humidity']    #humidity in %
    temp_min=city['main']['temp_min']-273.15     #self explanatory
    temp_max=city['main']['temp_max']-273.15
    print weather
    #pprint(city['main']['temp'])
    #pprint(city['weather'][0]['main'])
