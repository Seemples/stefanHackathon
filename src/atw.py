import json
import datetime
import time
import dateutil.parser
import skyscannerAPI
import random

# Can't be used due to limited amount of live price sessions being allowed per minute
def getSpecific(c1, c2, d1):
    print c1
    print c2
    print d1
    print "-----"
    return skyscannerAPI.livePricing(c1, c2, d1)

# Returns -1 if cheapest ticket is > budget, returns price of ticket if not whilst making changes to data structures
def chooseCityBasic(route, routeIata, routeCountry, d1, d2, budget, initRand):
    print routeIata[-1]
    print d1
    print d2
    outFlights = skyscannerAPI.browse(routeIata[-1], "Anywhere", d1, d2)
    print "o/"
    
    if len(outFlights) == 0:
        print "outFlights returned no flights... wat"
        return -1

    # Choose first destination by random
    affordableFlights = []
    if len(route) == 0 and initRand:
        for i in outFlights:
            if i["MinPrice"] < budget:
                affordableFlights += [i]
        for i in range(0, len(affordableFlights)):
            r = random.randint(0, len(affordableFlights)-1)
            countryId = skyscannerAPI.getCountryId(affordableFlights[r].get("DestCode"))
            if countryId in routeCountry:
                continue
            if countryId != None:
                routeCountry += [countryId]
            routeIata += [affordableFlights[r]["DestCode"]]
            route += [affordableFlights[r]]
            break
        if len(route) != 0:
            return route[-1]["MinPrice"]

    # TODO Make this modular to plug and play various choosing algorithms
    cheapest = outFlights[0] 
    countryId = None
    for i in outFlights:
        if i.get("DestCode") != None:
            if i["MinPrice"] < cheapest["MinPrice"]:
                countryId = skyscannerAPI.getCountryId(i.get("DestCode"))
                if countryId not in routeCountry:
                    cheapest = i

    # Consider budget
    if cheapest["MinPrice"] > budget:
        return -1

    if countryId != None:
        routeCountry += countryId
    routeIata += [cheapest.get("DestCode")]
    route += [cheapest]
    return cheapest["MinPrice"]

# Backtraces until can afford to go home :(
def goHome(route, budget, duration): 
    for i in route:
        print i
    print "----"
    while True:
        if len(route) == 0:
            return -1
        # parse date
        rd = route[-1]["OutboundLeg"]["DepartureDate"]
        dtrd = dateutil.parser.parse(rd)    # Should encapsulate this shiz or something
        dtrd += datetime.timedelta(days=duration)
        srd = dtrd.strftime("%Y-%m-%d")
        flightHome = skyscannerAPI.browse(route[-1]["DestCode"], route[0]["DestCode"], srd, srd)
        # There should be only one flight home
        if len(flightHome) != 0 and flightHome[0]["MinPrice"] < budget:
            route += [flightHome[0]]
            return 0
        budget += route[-1]["MinPrice"]
        rd = route[-1]["OutboundLeg"]["DepartureDate"]
        dtrd = dateutil.parser.parse(rd)
        dtrd += datetime.timedelta(days=duration)
        srd = dtrd.strftime("%Y-%m-%d")
        route.pop()
        print "popping <(^.^)>"
    return -1
    
# Return some json with the relevant info
def aroundTheWorld(startingCity, budget, startingDate, duration, ran):
    initBudget = budget     # Because I can't be bothered fixing up budget
    sd = dateutil.parser.parse(startingDate)
    ssd = startingDate # Reduce potential inconsistency when modification occurs later
    route = []
    routeIata = [startingCity]
    routeCountry = []
    cId = skyscannerAPI.getCountryId(startingCity)
    if cId != None:
        routeCountry += [cId]
    routeCountry = [skyscannerAPI.getCountryId(startingCity)]
    while True:
        i = None
        if ran == 5:
            i = chooseCityBasic(route, routeIata, routeCountry, ssd, ssd, budget, False)
        else:
            i = chooseCityBasic(route, routeIata, routeCountry, ssd, ssd, budget, True)
        if i == -1: # No flight is affordable
            break
        budget -= i
        if budget <= 0:
            break
        sd += datetime.timedelta(days=duration)
        ssd = sd.strftime("%Y-%m-%d")
    if goHome(route, budget, duration) == -1:   # Budget is no longer correct val
        if ran == 5:
            print "I CANNAE FIND A ROUTE CAPTIN"
            return route
        print "Retrying, hoping for better starting rand city"
        aroundTheWorld(startingCity, initBudget, startingDate, duration, ran+1)
    return route

def start(startingCity, budget, startingDate, duration):
    return aroundTheWorld(startingCity, budget, startingDate, duration, 0)

# print start("GLA", 100, "2013-11-09", 2)
#aroundTheWorld("GLA", 100, "2013-11-09", 2, 0)
