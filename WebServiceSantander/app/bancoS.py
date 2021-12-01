#Librerias
from types import MethodType
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from decimal import Decimal
import requests
import http.client
app = Flask(__name__)

#Cadema de colecciones
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:FranciscoPelaez_1995-1@localhost:3306/BancoSantander'
#Para que no salga alertas o warming
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#Inicializar SQLAlchemiz con la app
db = SQLAlchemy(app)
#Instanciamos marshmello
ma = Marshmallow(app)

#Creamos nuestra tabla Cliente
class BancoS(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cedula = db.Column(db.String(10))
    nombre = db.Column(db.String(100))
    cuenta = db.Column(db.String(13))
    saldo = db.Column(db.Numeric(10,2))
    entidadB = db.Column(db.String(100))
    
    def __init__(self, cedula, nombre, cuenta, saldo, entidadB ):
        self.cedula=cedula
        self.nombre=nombre
        self.cuenta=cuenta
        self.saldo=saldo
        self.entidadB=entidadB


#Creamos un esquema
class BancoSantanderSchema(ma.Schema):
    class Meta:
        fields= ('cedula','nombre','cuenta','saldo','entidadB')

#Una sola respuesta
cliente_schema= BancoSantanderSchema()
client_schema=BancoSantanderSchema()
#Varias Respuestas
clientes_schema= BancoSantanderSchema(many=True)

#Metodo GET Clientes del Banco
@app.route('/list',methods=['GET'])
def get_clientes():
    all_clientes = BancoS.query.all()
    result = clientes_schema.dump(all_clientes)
    return jsonify(result)

#Metodo GET por ID Clientes 
@app.route('/list/<id>',methods=['GET'])
def get_clientes_id(id):
    un_cliente= BancoS.query.get(id)
    return cliente_schema.jsonify(un_cliente)

#Metodo POST Agregar 
@app.route('/add', methods=['POST'])
def addCuenta():
    data=request.get_json(force=True)
    cedula=data['cedula']
    nombre=data['nombre']
    cuenta=data['cuenta']
    saldo=data['saldo']
    entidadB=data['entidadB']

    nuevo= BancoS(cedula, nombre, cuenta, saldo, entidadB)
    db.session.add(nuevo)
    db.session.commit()
    return cliente_schema.jsonify(nuevo)

#Metodo UPDATE 
@app.route('/update/<id>',methods=['PUT'])
def update(id):
    updatePer= BancoS.query.get(id)
    data=request.get_json(force=True)
    
    cedula=data['cedula']
    nombre=data['nombre']
    cuenta=data['cuenta']
    saldo=data['saldo']
    entidadB=data['entidadB']

    db.session.commit()

    return cliente_schema.jsonify(updatePer)

#Metodo DELETE 
@app.route('/delete/<id>',methods=['DELETE'])
def delete(id):
    deleteBan = BancoS.query.get(id)
    db.session.delete(deleteBan)
    db.session.commit()

    return cliente_schema.jsonify(deleteBan)

#Metodo Retiro
@app.route('/retiro/<cuenta>/<monto>',methods=['PUT'])
def retiro(cuenta, monto): 
    print("Cuenta Cliente: ", cuenta ," Cantidad a retirar: ", monto)
    un_cliente= BancoS.query.filter_by(cuenta=cuenta).first()
    #Convertirmos el valor string en decimal
    cantidadRetiro =Decimal(monto)
    #Realizamos la operacion
    cantidad = un_cliente.saldo - cantidadRetiro
    #Restamos la cantidad de retiro
    un_cliente.saldo = cantidad
    #Guardamos cambios
    db.session.commit()
    print( "Cuenta: ", cuenta, " Saldo: ",cantidad)
    return cliente_schema.jsonify(un_cliente)

#Metodo Deposito
@app.route('/deposito/<cuenta>/<monto>',methods=['PUT'])
def deposito(cuenta, monto): 
    print("Cuenta Cliente: ", cuenta ," Cantidad a Depositar: ", monto)
    un_cliente= BancoS.query.filter_by(cuenta=cuenta).first()
    #Convertirmos el valor string en decimal
    cantidadDeposito =Decimal(monto)
    #Realizamos la operacion
    cantidad = un_cliente.saldo + cantidadDeposito
    #Restamos la cantidad de retiro
    un_cliente.saldo = cantidad
    #Guardamos cambios
    db.session.commit()
    print( "Cuenta: ", cuenta, " Saldo: ",cantidad)
    return cliente_schema.jsonify(un_cliente)


#Metodo Transferencia al mismo banco 
@app.route('/transferencia/<cuenta>/<banco1>/<monto>/<cuenta2>/<banco2>',methods=['PUT'])
def tranferencia(cuenta, banco1, monto, cuenta2, banco2): 

    print("Banco Emisor: ", banco1," Cuenta Emisor: ", cuenta ," Cantidad a Retirar: ", monto, " Banco Receptor: ", banco2, " Cuenta Receptor: ",cuenta2) 

    cliente1= BancoS.query.filter_by(cuenta=cuenta).first()
    #Convertirmos el valor string en decimal
    cantidadE =Decimal(monto)
    #Realizamos la operacion
    cantidad = cliente1.saldo - cantidadE
    #Restamos la cantidad de retiro
    cliente1.saldo = cantidad

    #Llamamos a la API de Cambiar Moneda
    conn = http.client.HTTPSConnection("currency-exchange.p.rapidapi.com")
    headers = {
        'x-rapidapi-host': "currency-exchange.p.rapidapi.com",
        'x-rapidapi-key': "83fc875e99msh6903c2b2a8859bdp1138abjsna3ada827c7f2"
        }
    mon1 = 'MXN'
    mon2 = 'USD'
    valor=cantidadE
    conn.request("GET", "/exchange?from="+str(mon1)+"&to="+str(mon2)+"&q="+str(valor), headers=headers)
    res = conn.getresponse()
    data = res.read()
    valorC= data.decode("utf-8")
    resAux= Decimal(valorC)
    total= resAux * cantidadE
    valor = str(total)
    print('Cantidad a Transferir: ',valor)

    #Llamamos a la Api Desposito Banco Pichincha
    if banco2 == 'pichincha':
        print('Llama API deposito banco Pichincha')
        bancoPichincha= requests.put('http://127.0.0.1:5000/deposito/'+cuenta2+'/'+valor)
        print(bancoPichincha.text)

    #Llamamos a la Api Desposito Banco Pacifico
    if banco2 == 'pacifico':
        print('Llama API deposito banco Pacifico')
        bancoPacifico= requests.put('http://127.0.0.1:9567/deposito/'+cuenta2+'/'+valor)
        print (bancoPacifico.text)

    #Ralizamos el desposito en el Banco Santander
    if banco2=='santander':
        cliente2= BancoS.query.filter_by(cuenta=cuenta2).first()
        #Realizamos la operacion
        cantidad2 = cliente2.saldo + cantidadE
        #Restamos la cantidad de retiro
        cliente2.saldo = cantidad2

    db.session.commit()

    return cliente_schema.jsonify(cliente1)

#MENSAJE DE BIENVENIDA

@app.route('/')
def index():
    return render_template('index.html')

if __name__ =="__main__":
    app.run(host="localhost", port=9566)
