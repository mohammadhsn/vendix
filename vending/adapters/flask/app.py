from flask import Flask, request
from seedwork.application.bus import bus
from application.commands import CashIn, Choose

app = Flask(__name__)


@app.post('/cash-in')
def cash_in():
    bus.handle(CashIn(request.json['cash']))
    return "", 204


@app.post('/choose')
def choose():
    bus.handle(Choose(request.json['product_id']))
    return "", 204
