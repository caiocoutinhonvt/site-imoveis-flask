from crypt import methods
import email
from enum import unique

from functools import wraps
from io import UnsupportedOperation
from operator import truediv
import sqlite3
import string
from textwrap import wrap
from flask import Flask, flash, redirect, session, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user,login_required, logout_user
from forms import LoginForm, PostForm
from functools import wraps
import mysql.connector



app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senha@127.0.01:3310/imoveis_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)


# LOGIN CONFIG
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





# DATABASE MYSQL

class Imoveis(db.Model): 
    __tablename__ = "Imoveis"                  
    id = db.Column("id", db.Integer, primary_key =True)
    endereco = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    valor = db.Column(db.Numeric(10,2)) 

    def __init__(self,endereco,cidade,valor):
        self.endereco = endereco
        self.cidade = cidade
        self.valor = valor

class User(db.Model, UserMixin):
    __tablename__ = "Usuarios"     
    _id = db.Column("id", db.Integer, primary_key =True)
    usuario = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(10)) 

    @property
    def login_required(self):
        return True

    @property
    def is_authenticated(self):
        return True
        
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self._id)

    def __init__(self,usuario,email,password):
        self.usuario = usuario
        self.email = email
        self.password = password

db.create_all()


# ROUTES

@app.route("/") 
def index():
    return redirect(url_for('login'))


# LOGIN
@app.route('/login', methods = ["GET", "POST"])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        u = User.query.filter_by(usuario = form.usuario.data).first()
        if u and u.password == form.password.data:
            login_user(u)
            return redirect(url_for('cadastrar'))

        

    return render_template('login.html', form=form)


#LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# REGISTRAR
@app.route('/registrar', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form["usuario"]
        email = request.form["email"]
        pwd = request.form ["password"]
   
        user = User(usuario,email,pwd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    

    return render_template('register.html')


# CADASTRAR
@app.route("/cadastrar", methods= ["GET", "POST"])
@login_required

def cadastrar():
    if request.method == "POST":
        imoveis = Imoveis(request.form['endereco'], request.form ['cidade'], request.form['valor'])
        db.session.add(imoveis)
        db.session.commit()
        return redirect(url_for('listar'))
    return render_template("cadastrar.html") 


# BUSCAR
@app.route("/buscar", methods=["GET"])
@login_required
def buscar():
    q = request.args.get('q')
    imoveis = []

    if q:
        imoveis= Imoveis.query.filter(Imoveis.endereco.contains(q) | Imoveis.cidade.contains(q) | Imoveis.valor.contains(q) )

    return render_template("buscar.html", imoveis=imoveis)


# LISTAR
@app.route("/listar")
@login_required
def listar():
    
    imoveis = Imoveis.query.all()
    

    return render_template("listar.html", imoveis= imoveis)


# EDITAR
@app.route('/editar/<int:id>', methods = ['GET', "POST"])
@login_required
def edit_posts(id):
    
    post = Imoveis.query.get_or_404(id)
    form = PostForm() 

    if request.method == "POST":
        post.endereco = form.endereco.data
        post.cidade = form.cidade.data
        post.valor = form.valor.data

        db.session.add(post)
        db.session.commit()     
        print('FOI')
        return redirect(url_for('listar', id = Imoveis.id))

    form.id.data = post.id
    form.endereco.data = post.endereco
    form.cidade.data = post.cidade
    form.valor.data = post.valor
    return render_template("editar.html", form=form)


# DELETAR
@app.route('/delete/<int:id>') 
@login_required
def delete_post(id):
    post_to_delete = Imoveis.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        return redirect(url_for("listar"))

    except:
        return redirect(url_for(cadastrar))



# APPRUN
if __name__ == "__main__":
    app.run(debug=True)












