from flask import Flask, request, jsonify
from seedwork.application.bus import bus
from application.commands import RegisterMachine, SubmitPurchase


app = Flask(__name__)


@app.post('/register')
def register():
    identifier = bus.handle(RegisterMachine(request.json['hardware_id']))
    return jsonify({'id': identifier}), 201


@app.post('/purchase')
def purchase():
    payload = request.json
    identifier = bus.handle(SubmitPurchase(payload['machine'], payload['product'], payload['price']))
    return jsonify({'id': identifier}), 201
