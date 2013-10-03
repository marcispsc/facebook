Facebook
========

Python wrapper for Facebook Graph API

Features
--------

* Authentification
* Graph API supprt

Installation
------------

Install via [pip](http://www.pip-installer.org/)

	pip install FacebookGraph

or, with [easy_install](http://pypi.python.org/pypi/setuptools)

	easy_install FacebookGraph

Or, if you want the code that is currently on GitHub

	git clone git://github.com/BUHARDI/facebook.git
	cd facebook
	python setup.py install

Starting Out
------------

Register an application https://developers.facebook.com/apps

After you have registered the application, copy and save ID and API SECRET. Example below shows that I have stored those variables in Django settings as `FACEBOOK_ID` and `FACEBOOK_SECRET`.

Now you're ready to use Facebook Graph API. Import the wrapper class.

	from facebook import Facebook

Authentification
----------------

> This example is based on [Django framework](https://www.djangoproject.com/)

Example shows how to get Facebook user data. You only need to do this, if you created an application of type "Website with Facebook Login".

Typically this would be the process starting view.

	from django.conf import settings

	def login_facebook(request):
	    facebook = Facebook(settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
	    callback_url = 'http://domain.tld/login/facebook/callback'
	    login_url = facebook.get_login_url(redirect_uri=callback_url) # you can pass extra keyword arguments to the login url, like scope='publish_stream,email' or display='popup'
	    return redirect(login_url)

`callback_url` is url where user will be redirected after login on Facebook. In this view you will receive extra GET variables to complete the autorization.

Last things to end the login process - callback view. [Read the documentation.](https://developers.facebook.com/docs/facebook-login/login-flow-for-web-no-jssdk/)

	def login_facebook_callback(request):
	    if not request.GET.get('code'):
		    return HttpResponseBadRequest()
	    facebook = Facebook(settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
	    token = facebook.code2token(request.GET['code'], callback_url)
	    me = facebook.api('/me')

Thats it! `me` variable contains dictionary of user profile.

It's good idea store the user token in case you want use API again later. In Django you can take advantage of sessions.

	request.session['facebook_token'] = token

To use API, you have to set user token.

	facebook.set_access_token(request.session['facebook_token'])

Using the API
-------------

Chekout the code and the [documentation](https://developers.facebook.com/docs/reference/api/). You should be ready to dive in by now.

	facebook = Facebook(settings.FACEBOOK_ID, settings.FACEBOOK_SECRET, request.session['facebook_token'])

Create an instance. Third argument is user token which you received after user authorization.

More examples:

	me = facebook.api('/me')

	feed = facebook.api('/kalnins.marcis/feed')

	post = facebook.api('/me/feed', 'POST', message='My test message!')