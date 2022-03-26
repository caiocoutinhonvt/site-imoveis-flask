from crypt import methods
from re import S
import sqlite3
from flask import Flask, redirect, url_for, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


### DATABASE ###
class Imoveis(db.Model):
    id = db.Column("id", db.Integer, primary_key =True)
    endereco = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    valor = db.Column(db.Numeric(10,3)) 

    def __init__(self,endereco,cidade,valor):
        self.endereco = endereco
        self.cidade = cidade
        self.valor = valor



### LISTAR ###
@app.route("/listar")
def listar():

    imoveis = Imoveis.query.all()

    return render_template("listar.html", imoveis= imoveis)




### CADASTRAR ###
@app.route("/cadastrar", methods= ["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        imoveis = Imoveis(request.form['endereco'], request.form ['cidade'], request.form['valor'])
        db.session.add(imoveis)
        db.session.commit()
        return redirect(url_for('listar'))
    return render_template("cadastrar.html") 
    


### BUSCAR ### 
@app.route("/buscar", methods=["GET"])
def buscar():
    q = request.args.get('q')
    imoveis = []

    if q:
        imoveis= Imoveis.query.filter(Imoveis.endereco.contains(q) | Imoveis.cidade.contains(q) | Imoveis.valor.contains(q) )

    
        
    return render_template("buscar.html", imoveis=imoveis)



### HOME ### 
@app.route("/")
def index():
    return render_template("cadastrar.html")    



###RUN DO APP###

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)












