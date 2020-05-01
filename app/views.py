from app import app
from flask import render_template, redirect, url_for, request
from flask_login import logout_user, current_user, login_required, login_user

from app.oauth import Provider
from app.models import User


@app.route('/api/authorize/<string:provider_name>', methods=['GET', 'POST'])
def oauth_authorize(provider_name):
    if not current_user.is_anonymous:
        return url_for('index')

    provider = Provider.get_provider(provider_name)
    if provider is None:
        return url_for('index')

    return provider.authorize()


@app.route('/api/callback/<string:provider_name>', methods=['GET', 'POST'])
def oauth_callback(provider_name):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider = Provider.get_provider(provider_name)
    if provider is None:
        return redirect(url_for('index'))

    data = provider.callback(request.args.get('code'))
    if data is None:
        return redirect(url_for('index'))

    social_id, first_name, last_name, friends = data
    if None in data:
        return redirect(url_for('index'))

    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, first_name=first_name, last_name=last_name)
        user.commit_to_db()
        user.register_friends(friends)

    login_user(user, True)

    return redirect(url_for('index'))


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    return render_template('authorization.html')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template(
        'index.html',
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        friends=current_user.friends
    )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
