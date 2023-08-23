import os
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from sqlalchemy import inspect

from flask import Flask, jsonify, render_template, redirect

app = Flask(__name__)
Base = automap_base()
engine = create_engine("sqlite:///foreignaid.sqlite")
Base.prepare(engine, reflect=True)

# create references to tables

gdp_lit_aid = Base.classes.gdp_lit_aid
health = Base.classes.health
sector = Base.classes.sector

session = Session(engine)


# create routes to data for our api
@app.route("/")
def dashboard():
    """Return the rendered homepage."""
    return render_template("index.html")


@app.route("/gla")
def gla_return():
    """A country, the year, gdp per cap, lit rate, and aid received that year"""
    results = session.query(
        gdp_lit_aid.country,
        gdp_lit_aid.year,
        gdp_lit_aid.gdp_per_capita,
        gdp_lit_aid.literacy_rate,
        gdp_lit_aid.net_aid_received,
    ).all()
    list_of_gla = []
    for result in results:
        dictt = {
            "country": result[0],
            "year": result[1],
            "gdp_per_capita": result[2],
            "literacy_rate": result[3],
            "net_aid_received": result[4],
        }
        list_of_gla.append(dictt)
    return jsonify(list_of_gla)


@app.route("/health")
def health_return():
    """Return life expectancy, spending, and countries as aggregators"""
    results = session.query(
        health.year,
        health.ida_only,
        health.lower_middle_income,
        health.low_middle_income,
        health.health,
    ).all()
    json_list = []
    for result in results:
        da_dict = {
            "year": result[0],
            "ida_only_life_expectancy": result[1],
            "lower_middle_income_life_expectancy": result[2],
            "low_middle_income_life_expectancy": result[3],
            "health_aid_received": result[4],
        }
        json_list.append(da_dict)
    return jsonify(json_list)


@app.route("/sector_spending")
def sector_return():
    """return year, and the money spent on each sector during that year"""
    results = session.query(
        sector.year,
        sector.education,
        sector.health,
        sector.government,
        sector.economic,
        sector.business,
        sector.production,
        sector.multi_sector,
    ).all()
    json_list = []
    for result in results:
        json_dict = {}
        json_dict["year"] = result[0]
        json_dict["education"] = result[1]
        json_dict["health"] = result[2]
        json_dict["government"] = result[3]
        json_dict["economic"] = result[4]
        json_dict["business"] = result[5]
        json_dict["multi_sector"] = result[6]
        json_list.append(json_dict)
    #    for result in results:
    #        da_dict = {result[0]:{'education':result[1],
    #        'health':result[2],
    #        'government':result[3],
    #        'economic':result[4],
    #        'business':result[5],
    #        'multi_sector':result[7]}}
    #        json_list.append(da_dict)
    return jsonify(json_list)

if __name__ == "__main__":
    app.run(debug=True)
