import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'pv2m5uv239059329c023mc49234c2390m4293vn4234u23940n234238'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OAUTHS = {
        'vk': {
            'client_id': 7442669,
            'client_secret': '44323db544323db544323db5d64443ad5844'
                             '43244323db51a997a0ac47f86d06a00e344 ',
            'authorize_url': 'https://oauth.vk.com/authorize'
        }
    }