from os import environ as e
from httplib2 import Http
from argparse import ArgumentParser

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from flask import (
    Flask,
    jsonify as j
)

flags = ArgumentParser(parents=[tools.argparser]).parse_args()
flow = OAuth2WebServerFlow(
    client_id=e.get('client_id'),
    client_secret=e.get('client_secret'),
    scope='https://www.googleapis.com/auth/urlshortener'
)

storage = Storage('creds.dat')
credentials = storage.get()
if credentials is None or credentials.invalid is True:
    credentials = tools.run_flow(flow, storage, flags)

http = Http()
http_auth = credentials.authorize(http)

shortener = build('urlshortener', 'v1', http=http_auth).url()

app = Flask(__name__)


@app.route('/')
def get_recos():
    history = shortener.list().execute()
    return j(history)

if __name__ == '__main__':
    app.run('0.0.0.0')
