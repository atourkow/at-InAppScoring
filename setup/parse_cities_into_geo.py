#!/usr/bin/env python

# This parses GeoLightCity-Location.csv from
# http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity-latest.zip
# And outputs the US Codes
# Usage
#   python parse_cities_into_geo.py GeoLiteCity-Location.csv

import sys
# Command line arguements
if len(sys.argv) < 2:
    print "Usage:"
    print "python parse_cities_into_geo.py GeoLiteCity-Location.csv"
    print ""
    sys.exit()

f_out = open('GeoLocationsUS.delim.txt','w')

total = 0
with open(sys.argv[1], 'r') as fp:
    for line in fp:
        # It's just some text
        if "," not in line:
            continue

        line = line.split(',')

        # Only get the us
        if "US" not in line[1]:
            continue

        total += 1
        #locId,country,region,city,postalCode,latitude,longitude,metroCode,areaCode
        country = line[1].replace('"', "")
        city = line[3].replace('"', "").decode('unicode_escape').encode('ascii','ignore')
        zip = line[4].replace('"', "")
        lat = line[5].replace('"', "")
        lon = line[6].replace('"', "")

        if not zip or lat=="0.0000" or lon=="0.0000":
            continue

        print "{} Country:{} City:{:25} Zip:{:5} Lat:{:10} Lon:{:10}".format(total, country, city, zip, lat, lon)
        f_out.write( "{}||{}||{},{}\n".format(city, zip, lat, lon) )
