import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    URL = 'http://task.leemur.ru/'
    SECRET_KEY = 'pv2m5uv239059329c023mc49234c2390m4293vn4234u23940n234238'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OAUTHS = {
        'vk': {
            'client_id': 7442669,
            'client_secret': 'CepOt6GSo2i9WlrNnSEY',
            'authorize_url': 'https://oauth.vk.com/authorize',
            'access_token_url': 'https://oauth.vk.com/access_token',
            'request_url': 'https://api.vk.com/method/'
        }
    }
