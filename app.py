from flask import Flask, jsonify, request

app = Flask(__name__)

data = [ {
        'id': 0,
        'tiempo' : 0,
        'contador_pasadas' : 0,
        'temperatura': 0,
        'humedad': 0
    }
]

@app.route('/data')
def get_incomes():
    return jsonify(data)


@app.route('/data', methods=['POST'])
def add_income():
    data.append(request.get_json())
    return '', 204