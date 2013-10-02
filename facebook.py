import requests
from urllib import urlencode
from urlparse import parse_qs

class Facebook:
	URL_API = 'https://graph.facebook.com'
	URL_AUTH = 'https://www.facebook.com/dialog/oauth'

	_id = 0
	_secret = None
	_token = None

	def __init__(self, id, secret, token=None):
		self._id = id
		self._secret = secret
		self._token = token

	def get_access_token(self):
		return self._token

	def set_access_token(self, token):
		self._token = token

	def get_login_url(self, **kwargs):
		kwargs['client_id'] = self._id
		return '%s?%s' % (self.URL_AUTH, urlencode(kwargs))

	def code2token(self, code, redirect_uri):
		response = requests.get('%s/oauth/access_token' % self.URL_API, params={
			'client_id': self._id,
			'redirect_uri': redirect_uri,
			'client_secret': self._secret,
			'code': code,
		}).text
		token = parse_qs(response)['access_token'][0]
		self.set_access_token(token)
		return token

	def api(self, path, method='GET', **kwargs):
		if self._token:
			kwargs['access_token'] = self._token
		if method == 'POST':
			return requests.post('%s%s' % (self.URL_API, path), data=kwargs).json()
		else:
			return requests.get('%s%s' % (self.URL_API, path), params=kwargs).json()