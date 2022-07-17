from flask import Flask
import DBInterface as DB

app = Flask(__name__)
db = DB()

