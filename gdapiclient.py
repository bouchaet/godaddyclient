from flask import Flask, jsonify
from requests import get, put
import os


class GdApiClient(object):
    def __init__(self, domain):
        self.domain = domain
        self.key = os.environ.get('GODADDY_KEY')
        self.secrect = os.environ.get('GODADDY_SECRET')
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
        url = f'{self.apiv1_baseurl}/domains/{self.domain}/A/{name}'
        body = {
            'data': ipaddress,
            'ttl': ttl
        }

        put(url, headers=self.get_auth_header(), data=body)

    def get_auth_header(self):
        """
        :return: <dict> authorization header entry using sso-key
        """
        auth = {
            'Authorization': f'sso-key {self.key}:{self.secrect}'
        }
        return auth

    def get_a_records(self):
        """
        Return all A records in the domain.
        :return: <dict> godaddy response 
        """
        url = f'{self.apiv1_baseurl}/domains/{self.domain}/records/A'
        
        return get(url, headers=self.get_auth_header()).json()

app = Flask(__name__)
client = GdApiClient(os.environ.get('GODADDY_DOMAIN'))


@app.route('/myexternalip', methods=['GET'])
def get_external_ipaddress():
    return client.get_external_ip(), 200


@app.route('/records/A', methods=['GET'])
def get_A_records():
    resp = client.get_a_records()
    
    return jsonify(resp), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)