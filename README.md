# EarthDaily

I created an api that allows someone to input the name, location and date that they saw a bird. 
Or they can search for birds with a bounding box with options to filter by name or date.

For GET calls the JSON body has the following required numeric fields : north, south, east, and west
    -name is an optional 100 character max string field
    -day, month, and year are also optional integer fields, but all three are needed
        -currently the api returns a warning if you have the day but not the other two, and ignores those three if day isn't there.
            if I had more time I would have made this part more robust

For POST call the JSON body requires the following fields: name, lat, lng, day, month, year

For both POST and GET there is schema validation, date validation (including dealing with leap years), 
    and a check to make sure north is not south of south.

I ran out of time while writing tests, so the test suite is not anywhere near as robust as I would like.

Make sure to use the requirements.txt to get Flask and jsonschema packages

I wrote this in Python 3.8 using Pycharm in a Linux environment
        