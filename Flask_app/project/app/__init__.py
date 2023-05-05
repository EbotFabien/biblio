from flask import Flask, render_template, url_for,flash,redirect,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
#from flask_mail import Mail
from app.config import Config
import os
from firebase_admin import credentials, firestore, initialize_app
# Initialize Flask App

# Initialize Firestore DB



cred = credentials.Certificate('/work/www/microservice_edl/biblio/Flask_app/project/app/biblio.json')
default_app = initialize_app(cred)
db = firestore.client()
bcrypt = Bcrypt()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

   
    bcrypt.init_app(app)
   

    from app.entity.compteurs.routes import compteurs
    from app.entity.rubric.routes import rubric
    from app.entity.clefs.routes import clefs
    from app.entity.piece.routes import piece
    from app.entity.voie.routes import voie
    from app.entity.extension.routes import extension 
    from app.entity.typeloge.routes import typeloge
    from app.entity.typecom.routes import typecom
    from app.entity.commentaire.routes import commentaire
    from app.entity.logement.routes import logement
    
    app.register_blueprint(compteurs)
    app.register_blueprint(rubric)
    app.register_blueprint(clefs)
    app.register_blueprint(piece)
    app.register_blueprint(voie)
    app.register_blueprint(extension)
    app.register_blueprint(typeloge)
    app.register_blueprint(typecom)
    app.register_blueprint(commentaire)
    app.register_blueprint(logement)
    


    return app
