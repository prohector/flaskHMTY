#Ατομική εργασία στο μάθημα "Εισαγωγή στην επιστήμη του Ηλ. Μηχ."
#Μια εργασία του 1ο ετή φοιτητή Αλέξανδρου Μαρκόπουλου με ΑΜ: 1107677
#CC0 1.0 License Universal

from flask import Flask
from flask import (redirect, url_for)
from . import auth

def create_app(test_config = None): #Στο documentation αυτή η συνάτηση αποκαλείται app factory
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "DEV"
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True) #Αμα δεν γίνεται testing
    else: #Mόνο για testing
        app.config.from_mapping(test_config) 
    
    @app.route('/test')
    def hello():
        return 'This is for testing purposes'
    
    @app.route('/')#Γενικά αμα παει κανείς στο σκέτο url τον στέλνω στο login
    def home():
        return redirect(url_for("auth.login"))

    app.register_blueprint(auth.bp) #Θέτω το auth.py ως ένα blueprint

    from . import welcome
    app.register_blueprint(welcome.bp)
    app.add_url_rule('/', endpoint='wall')

    return app