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

if __name__ == "__main__":
    app.run(debug=True)
