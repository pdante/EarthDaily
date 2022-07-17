from flask import Flask, request, jsonify
from DBInterface import DBInterface as DB

app = Flask(__name__)
db = DB()


class Error(Exception):
    pass


class BadDay(Error):
    pass


def invalidateDay(day, month, year):
    if year < 1 or year > 2099:
        raise ValueError
    if month < 1 or month > 12:
        raise ValueError
    if day < 1 or day > 31:
        raise ValueError
    if month in [4, 6, 9, 11] and day == 31:
        return True
    if month ==2:
        if day in [30, 31]:
            return True
        if day == 29:
            if not year%4 == 0 or(year %4 == 0 and (year % 100 == 0 and not year % 400 == 0)):
                return True
    return False


def invalidLat(north):
    pass


def invalidLng(east):
    pass


@app.route('/', methods=['GET','POST'])
def birds():
    if request.method == 'GET':
        try:
            body = request.get_json()
            north = float(body["north"])
            south = float(body["south"])
            east = float(body["east"])
            west = float(body["west"])
            name = ""
            start = -1
            end = -1
            day = 0
            month = 0
            year = 0
            named = False
            timed = False
            dayed = False
            if invalidLat(north) or invalidLat(south) or invalidLng(east) or invalidLng(west):
                raise ValueError
            if "name" in body and not body["name"]:
                name = body["name"]
                if len(name) > 100:
                    raise ValueError
                named =  True
            if "start_hour" in body and "end_hour" in body and not body["start_hour"] and not body["end_hour"]:
                start = int(body["start_hour"])
                end = int(body["end_hour"])
                if start < 0 or start > 24 or end < 0 or end > 24:
                    raise ValueError
                timed = True
            if "day" in body and "month" in body and "year" in body and not body["day"] and not body["month"] and not body["year"]:
                day = int(body["day"])
                month = int(body["month"])
                year = int(body["year"])
                if invalidateDay(day, month, year):
                    raise ValueError
                dayed = True
            if not named and not timed and not day:
                return jsonify(db.getAllBirds(north, south, east, west))
            elif not named and not dayed:
                return jsonify(db.getAllBirdsTimed(north, south, east, west, start, end))
            elif not timed and not dayed:
                return jsonify(db.getBirds(north, south, east, west, name))
            elif not named and not timed:
                return jsonify(db.getAllBirdsDay(north,south,east,west,day,month,year))
            elif not named:
                return jsonify(db.getAllBirdsDayTime(north,south,east,west,day,month,year,start,end))
            elif not timed:
                return jsonify(db.getBirdsDay(north,south,east,west,name, day,month, year))
            elif not dayed:
                return jsonify(db.getBirdsTimed(north,south,east, west,name,start, end))
            else:
                return jsonify(db.getBirdsDayTime(north, south, east, west, name, day, month, year, start, end))
        except ValueError:
            errorMessage = """The json included in the body of this Get request was an invalid json for this api endpoint. The following numeric fields are required [north, south, east, west], the string field [name] is optional, the integer fields [start_hour and end_hour] are optional but must both exist to be used, and the integer fields [day, month, year] are also optional but must all exist to be used, no other fields are allowed. [north] and [south] must be <= 90 and >=-90. [east] and [west] must be <= 180 and >=-180. [name] is maximum 100 characters. [start_hour] and [end_hour] must each be between 0 and 24, inclusive. [year] must be between 1 and 2099. [day], [month], and [year] must be a valid combo to account for both different length months and leap years"""
            return jsonify(message=errorMessage)

    elif request.method == 'POST':
        try:
            body = request.get_json()
            lat = float(body["lat"])
            lng = float(body["lng"])
            name = body["name"]
            day = int(body["day"])
            month = int(body["month"])
            year = int(body["year"])
            start =  int(body["start_hour"])
            end = int(body["end_hour"])
            if invalidateDay(day, month, year):
                raise BadDay
            if invalidLat(lat) or invalidLng(lng):
                raise ValueError
            if len(name) > 100:
                raise ValueError
            if start < 0 or start > 24 or end < 0 or end > 24:
                raise ValueError
        except ValueError:
            errorMessage = """The json included in the body of this request to create a new bird sighting was an invalid json for this api endpoint.The following numeric fields are required [lat, lng, day, month, year, start_hour, and end_hour], as well as the string field [name]; no other fields are allowed. [lat] must be <= 90 and >=-90. [lng] must be <= 180 and >=-180. [Day] must be between 1 and 31, [month] between 1 and 12, and [year] between 1 and 2099. [name] is maximum 100 characters"""
            return jsonify(message=errorMessage)
        except BadDay:
            errorMessage = """The day of the month you indicated does not exist with your selected month and year"""
            return jsonify(message=errorMessage)
        db.createBird(name, lat, lng, start, end, day, month, year)
    else:
        error_message = """Currently only GET and POST requests are allowed. Please try again."""
        return jsonify(message=error_message)