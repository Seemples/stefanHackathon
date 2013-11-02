import requests
import json
from datetime import date, timedelta


#Use browse(dep,arr,date1,date2)    -->     returns json
#and livePricing(dep, arr, date)    -->     returns dict


###
#stuff

def browse(dep,arr,date1,date2):
    interval = days(date1,date2)
    output = browseRequest(dep,arr,interval[0])
    for day in interval[1:]:
        r = browseRequest(dep,arr,day)
        output["Quotes"] = r["Quotes"] + output["Quotes"]

    return output


def livePricing(dep, arr, date):        #String date in format YYYY-MM-DD
    part1 = "http://partners.api.skyscanner.net/apiservices/pricing/v1.0/GB/GBP/en-GB/"
    part2 = "?apikey=hck01722056005870195080684980065"
    data = requests.get(part1 + dep + "-sky/" + arr + "-sky/" + date + part2).json()
    
    output = {}
    bestPrice = data["Itineraries"][0]["PricingOptions"][0]["Price"]
    for flight in data["Itineraries"]:
        if flight["PricingOptions"][0]["Price"] <= bestPrice:
            bestPrice = flight["PricingOptions"][0]["Price"]
            bestId = flight["OutboundLegId"]
            bestAgent = flight["PricingOptions"][0]["Agents"][0]

    output["Price"] = bestPrice

    for flight in data["Legs"]:
        if flight["Id"] == bestId:
            output["Arrival"] = flight["Arrival"]
            output["Departure"] = flight["Departure"]
            bestCarrierId = flight["Carriers"][0]

    for carrier in data["Carriers"]:
        if carrier["Id"] == bestCarrierId:
            output["Carrier"] = carrier["Name"]

    for agent in data["Agents"]:
        if agent["Id"] == bestAgent:
            output["AgentName"] = agent["Name"]
            output["AgentLogo"] = agent["ImageUrl"]
        
    return output


###
#other stuff

def browseRequest(dep,arr,date):      #String date: YYYY-MM-DD
    requestPart1 = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/GB/GBP/en-GB/"
    requestPart2 = "?apiKey=hck01722056005870195080684980065"
    r = requests.get(requestPart1 + dep + "/" + arr + "/" + date + requestPart2)

    return r.json()


def days(date1,date2):
    days = [date1]
    nextDate = date1
    while not nextDate == date2:
        
        year = int(nextDate[:4])
        month = int(nextDate[5:7])
        day = int(nextDate[8:10])
        
        nextDate = (date(year,month,day) + timedelta(1)).strftime('%Y-%m-%d')
        days += [nextDate]
        
    return days
