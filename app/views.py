from app import app
from flask import render_template, redirect, url_for
from flask_login import logout_user, current_user

from app.oauth import VKProvider


@app.route('/api/authorize/<string:provider>', methods=['GET', 'POST'])
def authorize_provider(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    return VKProvider().authorize()


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    return render_template('authorization.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
