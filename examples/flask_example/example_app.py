from flask import Flask
from ecl_facebook.flask_decorators import facebook_begin, facebook_callback

app = Flask(__name__)

@facebook_begin(app, '/oauth/facebook/begin')
def oauth_facebook_begin():
    pass

@facebook_callback(app, '/oauth/facebook/complete')
def oauth_facebook_complete(token, error):
    return token

# You can also break apart the route specification and the decorator itself.
# For example:
#
#     @app.route('/oauth/facebook/complete')
#     @facebook_callback
#     def oauth_facebook_complete(token, error):
#         return token

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

