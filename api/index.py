import json
import os
from http.server import BaseHTTPRequestHandler
import requests
import logging

logger = logging.getLogger(__name__)

SECRET_TOKEN = os.getenv('Z_TOKEN')
BASE_URL = os.getenv('Z_URL')


class handler(BaseHTTPRequestHandler):

    FIELDS = ('email', 'category', 'message', 'title', 'name')
    TRAP_FIELD = 'last_name'

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        message = 'It works (tm)'
        self.wfile.write(message.encode())
        return

    def post_zammad_ticket(self, data):
        headers = {'Authorization': 'Bearer %s' % SECRET_TOKEN}
        # try to create user, failure is not a problem
        name = data['name']
        split = name.split(' ')
        firstname = split[0]
        lastname = ' '.join(split[1:]) if len(split) > 1 else ''
        r = requests.post('%s/users' % BASE_URL, json={
            'firstname': firstname,
            'lastname': lastname,
            'email': data['email'],
            'roles': ['Customer']
        }, headers=headers)
        logger.debug('Create user: %s', r.json())
        # create ticket
        post_data = {
            'title': data['title'],
            'group': data['category'],
            'article': {
                'body': data['message'],
                'type': 'web',
                'from': data['email'],
                'to': data['category'],
                'internal': False,
            },
            'customer': data['email'],
        }
        headers['X-On-Behalf-Of'] = data['email']
        r = requests.post('%s/tickets' % BASE_URL, json=post_data, headers=headers)
        logger.debug('Create ticket: %s', r.json())
        return r.status_code, r.json()

    def do_POST(self):
        data = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        data = json.loads(data)
        for field in self.FIELDS:
            if field not in data:
                self.send_error(400, 'Missing json parameter')
                return
        if self.TRAP_FIELD in data and data[self.TRAP_FIELD]:
            # dummy response for bot spammers
            self.send_response(200)
            return
        try:
            status, data = self.post_zammad_ticket(data)
        except Exception as e:
            self.send_response(500)
            data = {'error': str(e)}
        else:
            self.send_response(status)
        finally:
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
