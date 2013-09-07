# box
# Copyright 2013-2014 Dipen Patel
# See LICENSE for details.

import urllib

from error import BoxError


class OAuthHandler(object):
    """OAuth authentication handler"""

    OAUTH_URL = 'https://www.box.com/api/oauth2/'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_auth_url(self, response_type='code', redirect_uri=None):
        """Get the authorization URL to redirect the user"""
        try:
            args = {
                    "response_type": response_type,
                    "client_id": self.client_id,
                    "redirect_uri": redirect_uri
                    }

            url = self.OAUTH_URL + 'authorize?'

            return url + urllib.urlencode(args)
        except Exception, e:
            raise BoxError(e)

    def get_access_token(self, redirect_uri, code=None, refresh_token=None, grant_type="authorization_code"):
        """
        After user has authorized the access to app, get access token.
        """
        try:
            url = self.OAUTH_URL + 'token'

            args = {
                    "grant_type": grant_type,
                    "redirect_uri": redirect_uri,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                    }

            if code:
                args["code"] = code
            if refresh_token:
                args["refresh_token"] = refresh_token
            # send request
            resp = urllib.urlopen(url, urllib.urlencode(args))
            response = resp.read()
            resp.close()
            return response
        except Exception, e:
            raise BoxError(e)

