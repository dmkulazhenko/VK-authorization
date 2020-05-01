from app import app
from rauth import OAuth2Service
from flask import current_app


class Provider:
    pass


class VKProvider:
    def __init__(self):
        if 'vk' not in current_app.config['OAUTHS']:
            raise ValueError('You missed the VK settings in the configuration')

        self._service = OAuth2Service(
            name='vk',
            client_id=current_app.config['OAUTHS']['vk']['client_id'],
            client_secret=current_app.config['OAUTHS']['vk']['client_secret'],
            authorize_url=current_app.config['OAUTHS']['vk']['authorize_url']
        )

    def authorize(self):
        return self._service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri='vk.com'
        )
