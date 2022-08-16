"""
Example API for requesting from the html_parse_server.py

Example usage:
parser = HTMLAPI()
return_dict, return_code = parser.fetch_word_count(url='http://www.google.co.uk', tag='title')
return_dict, return_code = parser.fetch_health()
"""


import requests
import json


class HTMLAPI:

    def __init__(self):
        # Known URLs in service
        self.route_data = 'http://localhost:8080/count'
        self.route_health = 'http://localhost:8080/health'
        # Header format for requests
        self.headers = {'content-type': 'application/json'}

    def fetch_word_count(self, url, tag='html'):
        """
        Request the number of words contained with in tag for a given URL

        :param url: string url of website from which to fetch data
        :param tag: string HTML tag to search in given URL
        :return data, code: dict, int of returned word count and HTTP response
        """
        payload = {"url": url, "tag": tag}
        response = requests.post(self.route_data, data=json.dumps(payload), headers=self.headers)

        data = json.loads(response.text)
        code = response.status_code

        return data, code

    def fetch_health(self):
        """ Request the health status of the running service """
        response = requests.get(self.route_health)

        data = json.loads(response.text)
        code = response.status_code

        return data, code


if __name__ == "__main__":
    # Run example use case if this script is called directly
    parser = HTMLAPI()
    return_dict, return_code = parser.fetch_word_count(url='http://www.google.co.uk', tag='title')
    print(return_dict, return_code)
    return_dict, return_code = parser.fetch_health()
    print(return_dict, return_code)
