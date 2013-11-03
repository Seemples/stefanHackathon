import json
import datetime
import time
import dateutil.parser
import skyscannerAPI

def getSpecific(c1, c2, d1):
    print c1
    print c2
    print d1
    print "-----"
    return skyscannerAPI.livePricing(c1, c2, d1)

# Returns -1 if cheapest ticket is > budget, returns price of ticket if not whilst making changes to data structures
def chooseCityBasic(route, routeId, flightDetails, d1, d2, budget):
    outFlights = skyscannerAPI.browse(route[-1], "Anywhere", d1, d2)
    
    # Need to search routeId[0] in order to avoid conflicts later on
    if not routeId:
        for i in outFlights["Places"]:
            if i.get("IataCode") == route[0]:
                routeId += [i["PlaceId"]]
                break

    cheapest = outFlights["Quotes"][0]  # TODO Handle no flights
    for i in outFlights["Quotes"]:
        if i["MinPrice"] < cheapest["MinPrice"] and i["OutboundLeg"]["DestinationId"] not in routeId:
            cheapest = i

    # Consider budget
    if cheapest["MinPrice"] > budget:
        return -1

    # Get Iata code
    for i in outFlights["Places"]:      # Figure out more efficient method....
        if cheapest["OutboundLeg"]["DestinationId"] == i["PlaceId"]:
            route += [i["IataCode"]]
            routeId += [i["PlaceId"]]
            break
    temp = dateutil.parser.parse(cheapest["OutboundLeg"]["DepartureDate"])
    stemp = temp.strftime("%Y-%m-%d")
    flightDetails += [getSpecific(route[-2], route[-1], stemp)]
    
    return cheapest["MinPrice"]

# Backtraces until can afford to go home :(
def goHome(route, flightDetails, budget, duration): 
    if len(route) == 1:
        return
    # parse date
    rd = flightDetails[-1]["Arrival"];
    dtrd = dateutil.parser.parse(rd)
    dtrd += datetime.timedelta(days=duration)
    srd = dtrd.strftime("%Y-%m-%d") 
    flightHome = getSpecific(route[-1], route[0], srd) # Need to handle no flights TODO
    while flightHome["Price"] > budget:
        route.pop()
        budget += flightDetails[-1]["Price"]
        rd = flightDetails[-1]["Arrival"]
        dtrd = dateutil.parser.parse(rd)
        dtrd += datetime.timedelta(days=duration)
        srd = dtrd.strftime("%Y-%m-%d")
        flightDetails.pop()
        flightHome = getSpecific(route[-1], route[0], srd)
    route += [route[0]]
    flightDetails += [flightHome]
    return
    
# Return some json with the relevant info
def aroundTheWorld(startingCity, budget, startingDate, duration):
    sd = dateutil.parser.parse(startingDate)
    ssd = startingDate # Reduce potential inconsistency when modification occurs later
    route = [startingCity]
    routeId = []
    flightDetails = []
    while True:
        i = chooseCityBasic(route, routeId, flightDetails, ssd, ssd, budget)
        if i == -1: # No flight is affordable
            break
        budget -= i
        if budget <= 0:
            break
        sd += datetime.timedelta(days=duration)
        ssd = sd.strftime("%Y-%m-%d")
    goHome(route, flightDetails, budget, duration)
    return flightDetails

print aroundTheWorld("GLA", 100.00, "2013-11-09", 2)
