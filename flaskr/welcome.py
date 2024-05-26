from flask import (request, url_for, render_template, flash, g, Blueprint, redirect)
from flaskr.auth import login_required


bp  = Blueprint("welcome", __name__) #Φτιάχνω blueprint


@bp.route('/welcome')
@login_required
def index():

    return render_template('welcome/wall.html') 

