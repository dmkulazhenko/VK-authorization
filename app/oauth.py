import json
from rauth import OAuth2Service
from flask import current_app


class Provider:
    # TODO: U can get NoneType error, bcs ur method create_providers
    #  uses unsave index access to Provider.providers,
    #  but init of dict is in get_provider.
    #  So, that creates smth like inconsistently call order.
    #  U should init providers not that way or make create_providers private.
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name

    def authorize(self):
        pass

    def callback(self, code):
        pass

    # TODO: private?
    def get_callback_url(self):
        return current_app.config['URL'] + 'api/callback/' + self.provider_name

    @classmethod
    def create_providers(cls):
        for provider_class in cls.__subclasses__():
            provider = provider_class()
            cls.providers[provider.provider_name] = provider_class()

    @classmethod
    def get_provider(cls, provider_name):
        if provider_name not in current_app.config['OAUTHS']:
            return None

        if cls.providers is None:
            cls.providers = {}
            cls.create_providers()

        return cls.providers.get(provider_name)


class VKProvider(Provider):
    def __init__(self):
        super(VKProvider, self).__init__('vk')
        # TODO: PEP8 E501
        self._service = OAuth2Service(
            name='vk',
            client_id=current_app.config['OAUTHS']['vk']['client_id'],
            client_secret=current_app.config['OAUTHS']['vk']['client_secret'],
            authorize_url=current_app.config['OAUTHS']['vk']['authorize_url'],
            access_token_url=current_app.config['OAUTHS']['vk']['access_token_url']
        )

    def authorize(self):
        return self._service.get_authorize_url(
            scope='2',
            response_type='code',
            redirect_uri=self.get_callback_url()
        )

    def callback(self, code):
        # TODO: Im not sure, that its good idea to return tuple with info,
        #   maybe u should create base class and return class instance.
        #   Bcs, if we will talk about scalability on other providers,
        #   returning the tuple maybe less readable / elegant.
        def new_decoder(payload):
            return json.loads(payload.decode('utf-8'))

        if code is None:
            return None

        oauth_session = self._service.get_auth_session(
            data={'code': code,
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=new_decoder
        )

        # TODO: move requests URL / v to config / class static constants / ...
        user_information = oauth_session.get(
            current_app.config['OAUTHS']['vk']['request_url'] + 'users.get',
            params={'access_token': oauth_session.access_token, 'v': '5.103'}
        ).json()['response'][0]

        friends = oauth_session.get(
            current_app.config['OAUTHS']['vk']['request_url'] + 'friends.get',
            params={'access_token': oauth_session.access_token, 'v': '5.103',
                    'user_id': user_information['id'], 'order': 'random',
                    'count': 5, 'fields': 'city'}
        ).json()['response']['items']

        return (user_information['id'], user_information['first_name'],
                user_information['last_name'], friends)
