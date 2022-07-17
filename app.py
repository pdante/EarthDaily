from flask import Flask, request, jsonify
import DBInterface as DB

app = Flask(__name__)
db = DB()


class Error(Exception):
    pass


class BadDay(Error):
    pass


def validateDay(day, month, year):
    if year < 1 or year > 2099:
        raise ValueError
    if month < 1 or month > 12:
        raise ValueError
    if day < 1 or day > 31:
        raise ValueError
    if month in [4, 6, 9, 11] and day == 31:
        raise BadDay
    if month ==2:
        if day in [30, 31]:
            raise BadDay
        if day == 29:
            if not year%4 == 0 or(year %4 == 0 and (year % 100 == 0 and not year % 400 == 0)):
                raise BadDay


@app.route('/', methods=['GET','POST'])
def birds():
    if request.method == 'GET':
        pass
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
            validateDay(day, month, year)
            if lat < -90 or lat > 90 or lng < -180 or lng > 180:
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
        pass
    else:
        error_message = """Currently only GET and POST requests are allowed. Please try again."""
        return jsonify(message=error_message)