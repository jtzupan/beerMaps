#!/bin/bash
if [ "$1" = "Dallas" ]; then
    echo "Generating "${1}" map."
    python ./main.py -u https://www.ratebeer.com/places/regions/dallas-fort-worth/1920/43/#beckwith -t dallasBeer -s tx -c Dallas

if [ "$1" = "Indianapolis" ]; then
    echo "Generating "${1}" map."
    python ./main.py -u https://www.ratebeer.com/places/regions/indianapolis-carmel/3480/13/ -t indyBeer -s in -c indianapolis

else
    echo "No city specified.  Generating default Detroit map"
    python ./main.py
fi