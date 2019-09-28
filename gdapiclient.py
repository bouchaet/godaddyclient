from flask import Flask, jsonify, url_for
from requests import get, put
import os
import json


class GdApiClient(object):
    def __init__(self, domain):
        self.domain = domain
        self.key = os.environ.get('GODADDY_KEY')
        self.secret = os.environ.get('GODADDY_SECRET')
        self.apiv1_baseurl = 'https://api.godaddy.com/v1'

    @staticmethod
    def get_external_ip():
        return get('https://api.ipify.org').text

    def update_a_record(self, name, ipaddress, ttl):
        """
        Update or create A record.
        :param name: <string> Name of the record
        :param ipaddress: <string> ipv4 address
        :param ttl: <int> time to live
        :return: <string> empty if successful, error message otherwise
        """
        url = f'{self.apiv1_baseurl}/domains/{self.domain}/records/A/{name}'
        body = [{
            'data': ipaddress,
            'ttl': ttl
        }]

        print(f'json = {json.dumps(body)}')

        return put(url, headers=self.get_auth_header(), data=json.dumps(body))

    def get_auth_header(self):
        """
        :return: <dict> authorization header entry using sso-key
        """
        auth = {
            'Authorization': f'sso-key {self.key}:{self.secret}',
            'Content-Type': 'application/json'
        }
        return auth

    def get_a_records(self):
        """
        Return all A records in the domain.
        :return: <dict> godaddy response 
        """
        url = f'{self.apiv1_baseurl}/domains/{self.domain}/records/A'
        return get(url, headers=self.get_auth_header()).json()

    def __repr__(self):
        return f'domain: {self.domain}, key={self.key}'


app = Flask(__name__)
client = GdApiClient(os.environ.get('GODADDY_DOMAIN'))


@app.route('/', methods=['GET'])
def get_home():
    return jsonify({
        'links': [
            url_for('get_external_ipaddress', _external=True),
            url_for('get_A_records', _external=True)],
    })


@app.route('/myexternalip', methods=['GET'])
def get_external_ipaddress():
    return client.get_external_ip(), 200


@app.route('/records/A', methods=['GET'])
def get_A_records():
    resp = client.get_a_records()
    return jsonify(resp), 200


@app.route('/records/A/<name>/refresh', methods=['GET'])
def get_update_record(name):
    addr = client.get_external_ip()
    r = client.update_a_record(name, addr, 3600)
    if r.ok:
        return jsonify({"message": f"A record {name} was updated to {addr}."}), 200

    return jsonify(r.json()), r.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
