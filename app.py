from flask import Flask, request, jsonify
from DBInterface import DBInterface as DB
from jsonschema import validate, ValidationError, SchemaError

app = Flask(__name__)
db = DB()

getSchemaBird = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "maxLenghth": 100},
        "north": {"type": "number", "minimum": -90, "maximum": 90},
        "south": {"type": "number", "minimum": -90, "maximum": 90},
        "east": {"type": "number", "minimum": -180, "maximum": 180},
        "west": {"type": "number", "minimum": -180, "maximum": 180},
    },
    "required": ["name","north","south","east","west"]
}

getSchemaBirdDay = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "maxLenghth": 100},
        "north": {"type": "number", "minimum": -90, "maximum": 90},
        "south": {"type": "number", "minimum": -90, "maximum": 90},
        "east": {"type": "number", "minimum": -180, "maximum": 180},
        "west": {"type": "number", "minimum": -180, "maximum": 180},
        "day": {"type": "integer", "minimum": 1, "maximum": 31},
        "month": {"type": "integer", "minimum": 1, "maximum": 12},
        "year": {"type": "integer", "minimum": 1, "maximum": 2099},
    },
    "required": ["name","north","south","east","west","day","month","year"]
}

getSchemaNoBird = {
    "type": "object",
    "properties": {
        "north": {"type": "number", "minimum": -90, "maximum": 90},
        "south": {"type": "number", "minimum": -90, "maximum": 90},
        "east": {"type": "number", "minimum": -180, "maximum": 180},
        "west": {"type": "number", "minimum": -180, "maximum": 180},
    },
    "required": ["north","south","east","west"]
}

getSchemaNoBirdDay = {
    "type": "object",
    "properties": {
        "north": {"type": "number", "minimum": -90, "maximum": 90},
        "south": {"type": "number", "minimum": -90, "maximum": 90},
        "east": {"type": "number", "minimum": -180, "maximum": 180},
        "west": {"type": "number", "minimum": -180, "maximum": 180},
        "day": {"type": "integer", "minimum": 1, "maximum": 31},
        "month": {"type": "integer", "minimum": 1, "maximum": 12},
        "year": {"type": "integer", "minimum": 1, "maximum": 2099},
    },
    "required": ["name", "north", "south", "east", "west", "day", "month", "year"]
}

newBirdSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "maxLength": 100},
        "lat": {"type": "number", "minimum": -90, "maximum": 90},
        "lng": {"type": "number", "minimum": -180, "maximum": 180},
        "day": {"type": "number", "minimum": 1, "maximum": 31},
        "month": {"type": "number", "minimum": 1, "maximum": 12},
        "year": {"type": "number", "minimum": 1, "maximum": 2099},
    },
}

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


def invalidLat(lat):
    return lat > 90 or lat < -90


def invalidLng(lng):
    return lng > 180 or lng < -180


@app.route('/', methods=['GET','POST'])
def birds():
    if request.method == 'GET':
        try:
            body = request.get_json()
            if invalidGETJSON(body):
                  raise ValueError
            north = float(body["north"])
            south = float(body["south"])
            east = float(body["east"])
            west = float(body["west"])
            name = ""
            day = 0
            month = 0
            year = 0
            named = False
            dayed = False
            if invalidLat(north) or invalidLat(south) or invalidLng(east) or invalidLng(west) or north < south:
                raise ValueError
            if "name" in body and not body["name"]:
                name = body["name"]
                if len(name) > 100:
                    raise ValueError
                named =  True
            if "day" in body and "month" in body and "year" in body and not body["day"] and not body["month"] and not body["year"]:
                day = int(body["day"])
                month = int(body["month"])
                year = int(body["year"])
                if invalidateDay(day, month, year):
                    raise ValueError
                dayed = True
            if not named and not dayed:
                return jsonify(db.getAllBirds(north, south, east, west))
            elif not dayed:
                return jsonify(db.getBirds(north, south, east, west, name))
            elif not named:
                return jsonify(db.getAllBirdsDay(north,south,east,west,day,month,year))
            else:
                return jsonify(db.getBirdsDay(north, south, east, west, name, day, month, year))
        except ValueError:
            errorMessage = """The json included in the body of this GET request was an invalid json for this api endpoint. The following numeric fields are required [north, south, east, west], the string field [name] is optional, and the integer fields [day, month, year] are also optional but must all exist to be used, no other fields are allowed. [north] and [south] must be <= 90 and >=-90. [east] and [west] must be <= 180 and >=-180. [name] is maximum 100 characters. [year] must be between 1 and 2099. [day], [month], and [year] must be a valid combo to account for both different length months and leap years"""
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
            if invalidateDay(day, month, year):
                raise BadDay
            if invalidLat(lat) or invalidLng(lng):
                raise ValueError
            if len(name) > 100:
                raise ValueError
        except ValueError:
            errorMessage = """The json included in the body of this request to create a new bird sighting was an invalid json for this api endpoint.The following numeric fields are required [lat, lng, day, month, year], as well as the string field [name]; no other fields are allowed. [lat] must be <= 90 and >=-90. [lng] must be <= 180 and >=-180. [Day] must be between 1 and 31, [month] between 1 and 12, and [year] between 1 and 2099. [name] is maximum 100 characters"""
            return jsonify(message=errorMessage)
        except BadDay:
            errorMessage = """The day of the month you indicated does not exist with your selected month and year"""
            return jsonify(message=errorMessage)
        return db.createBird(name, lat, lng, day, month, year)
    else:
        error_message = """Currently only GET and POST requests are allowed. Please try again."""
        return jsonify(message=error_message)


def invalidGETJSON(jsonbody):
    if "name" in jsonbody:
        if "day" in jsonbody:
            try:
                validate(instance=jsonbody, schema=getSchemaBirdDay)
            except (ValidationError, SchemaError):
                return True
            return False
        else:
            try:
                validate(instance=jsonbody, schema=getSchemaBird)
            except (ValidationError, SchemaError):
                return True
            return False
    else:
        if "day" in jsonbody:
            try:
                validate(instance=jsonbody, schema=getSchemaNoBirdDay)
            except (ValidationError, SchemaError):
                return True
            return False
        else:
            try:
                validate(instance=jsonbody, schema=getSchemaNoBird)
            except (ValidationError, SchemaError):
                return True
            return False
