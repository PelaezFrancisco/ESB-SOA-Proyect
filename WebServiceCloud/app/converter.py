import http.client
from types import MethodType
from flask import Flask, jsonify, request
from decimal import Decimal

app = Flask(__name__)

@app.route('/convertidor/<mon1>/<mon2>/<cant>',methods=['GET'])
def get_clientes_id(mon1, mon2, cant):

    conn = http.client.HTTPSConnection("currency-exchange.p.rapidapi.com")
    headers = {
        'x-rapidapi-host': "currency-exchange.p.rapidapi.com",
        'x-rapidapi-key': "83fc875e99msh6903c2b2a8859bdp1138abjsna3ada827c7f2"
        }
    valor = Decimal(cant)
    conn.request("GET", "/exchange?from="+str(mon1)+"&to="+str(mon2)+"&q="+str(valor), headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    
    return data.decode("utf-8")


if __name__ =="__main__":
    app.run(debug=True)