#Αυτό το αρχείο είναι υπεύθυνο για τα routes register, login, logout, load-logged-in-user, readurl και login-required
import functools
from . import txtmanager as txt
from . import qrauth

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route('/register', methods=('GET', 'POST')) #Eγγραφή
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        errorcode = None

        if not username: #Έλεγχος για κενά πεδία
            errorcode = 'Username is required.'
        elif not password:
            errorcode = 'Password is required.'
        elif (' ' in username) or (' ' in password):
            errorcode = 'Usernames and passwords cannot contain empty spaces'
        elif len(username)>26 or len(password)>26:
            errorcode = 'Usernames and passwords cannot be larger than 26 characters'
        

        if errorcode is None:
            try:
                txt.new(username, password) #Αποθήκευσε καινούργιο χρήστη
            except ValueError:
                errorcode = f"Username {username} already exists." #Ο χρήστης υπάρχει ήδη
            else:
                return redirect(url_for("auth.login")) #Κανε redirect τον χρήστη στο url της συνάρτησης login του auth.py

        flash(errorcode)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST')) #Log in
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        userpass = txt.search(username)

        if userpass == False: #Δεν υπάρχει ο χρήστης
            error = 'Incorrect username.'
        elif txt.passwordhash(password) != userpass:
            error = 'Incorrect password.'

        if error is None: 
            session.clear()
            session['user_id'] = txt.id(username)
            qrauth.generate(username, txt.passwordhash(password))
            return redirect(url_for('welcome.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request #Εκτελείται πριν να φορτώσει η σελίδα απο οποιαδήποτε διεύθυνση
def load_logged_in_user(): #Φορτώνει τα στοιχεία του ήδη συνδεδεμένου χρήστη
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = txt.info(user_id) #Η global μεταβλητή g.user. παίρνει τα στοιχεία του χρήστη

@bp.route('/logout') #Aποσύνδεση
def logout():
    session.clear() #καθαρίζει τον παρόν χρήστη
    return redirect(url_for('auth.login'))

@bp.route('/qrlogin/<username>-<hash>')
def readurl(username, hash): #Διαβάζει το url για να κάνει login με το QR
    return qrauth.authenticate(username, hash)
    



def login_required(view): #Άμα κάποιος δεν είναι logged in, ανακατεύθεινέ τον
    @functools.wraps(view)
    def wrapper_view(**kwargs):
        if g.user is None: #Άμα δεν είναι συνδεδεμένος
            
            return redirect(url_for('auth.login')) 
        return view(**kwargs)
    return wrapper_view