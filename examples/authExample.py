from box import auth

client_id = 'Your App client id'
client_secret = 'Your App Secret'

tempAuth = auth.OAuthHandler(client_id, client_secret)

authUrl = tempAuth.get_auth_url()
print authUrl

access_token = tempAuth.get_access_token("https://localhost/", code="Code returned in url")
print access_token



