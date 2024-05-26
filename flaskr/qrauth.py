#Διαχείρηση του συστήματος login με κωδικό QR 
from flask import session, redirect, url_for
from . import txtmanager as txt
import qrcode
import os

qr = qrcode.QRCode( #Κλάση QR code
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

def authenticate(user, passhash):
    error = None
    userpass = txt.passwordhash(txt.search(user))
    if userpass == False: #Δεν υπάρχει ο χρήστης
                error = 'Incorrect username.'
    elif passhash != userpass:
        error = 'Incorrect password.'

    if error is None: 
        session.clear()
        session['user_id'] = txt.id(user)
        return redirect(url_for('welcome.index'))
    
    return NameError

def generate(username, password): #Δημιουργώ QR
      doublehash = txt.passwordhash(password) #Ξανα hashing ωστε να μην είναι αναγνωρίσιμο το url
      url = f'http://127.0.0.1:5000/auth/qrlogin/{username}-{doublehash}'
      qr.add_data(url)
      qr.make(fit=True)
      img = qr.make_image(fill_color="black", back_color="white") #Φτιάχνει εικόνα
      img.save(os.path.join('flaskr', "static", "images", "qrgenerated.png"))