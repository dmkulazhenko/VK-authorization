from app import app
from flask import render_template, redirect, url_for, request
from flask_login import logout_user, current_user, login_required, login_user

from app.oauth import Provider
from app.models import User


# TODO: Exclude api views to separate file
# TODO: Create decorator (same as login_required),
#  which checks that user is anonymous and use it with API routes
# TODO: *on ur choice* u can exclude provider instance parsing,
#  to remove code duplicates


@app.route('/api/authorize/<string:provider_name>', methods=['GET', 'POST'])
def oauth_authorize(provider_name):
    if not current_user.is_anonymous:
        return url_for('index')

    provider = Provider.get_provider(provider_name)
    # TODO: User is anonymous, so maybe u should redirect him to auth
    #   btw, index page will do it, so, u can do on ur choice
    if provider is None:
        return url_for('index')

    return provider.authorize()


# TODO: 'code' is session key for user and u shouldn't request it every time


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
        # TODO: PEP8 E501
        user = User(social_id=social_id, first_name=first_name, last_name=last_name)
        user.commit_to_db()
        # TODO: U can register friend in overridden constructor
        user.register_friends(friends)

    # TODO: mark kwargs
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
