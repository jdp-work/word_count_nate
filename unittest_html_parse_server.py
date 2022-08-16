import json
import os
import requests
import unittest
import threading


class UnittestHTMLParser(unittest.TestCase):
    """ Unit tests for the html parser server """

    headers = {'content-type': 'application/json'}

    def test_simple_health_request(self):
        test_resp = requests.get('http://localhost:8080/health')
        self.assertEqual(test_resp.status_code,
                         200,
                         "Health service returns expected good service")

    def test_simple_tag_request(self):
        payload = {"url": "https://www.bbc.co.uk/news", "tag": 'title'}
        test_resp = requests.post('http://localhost:8080/count', data=json.dumps(payload), headers=self.headers)

        # Assumption that "bbc" will be contained in title at least once
        try:
            test_data = json.loads(test_resp.text)
            test_count = test_data['bbc']
        except KeyError:
            test_count = 0

        self.assertGreater(test_count,
                           0,
                           "Text from known URL can be parsed")

    def test_full_tag_request(self):
        payload = {"url": "https://www.bbc.co.uk/news", "tag": 'html'}
        test_resp = requests.post('http://localhost:8080/count', data=json.dumps(payload), headers=self.headers)

        # Assumption that "bbc" will be contained multiple times (verified by inspection)
        try:
            test_data = json.loads(test_resp.text)
            test_count = test_data['bbc']
        except KeyError:
            test_count = 0

        self.assertGreater(test_count,
                           10,
                           "Text from entire URL page can be parsed")

    def test_bad_url_tag_request(self):
        payload = {"url": "https://www.fakefakedefinitelynotreal", "tag": 'title'}
        test_resp = requests.post('http://localhost:8080/count', data=json.dumps(payload), headers=self.headers)

        self.assertEqual(test_resp.status_code, 404,
                         "Identified that a bad URL cannot be found when requesting tag")

    def test_malformed_url_tag_request(self):
        payload = {"url": "test123", "tag": 'title'}
        test_resp = requests.post('http://localhost:8080/count', data=json.dumps(payload), headers=self.headers)

        self.assertEqual(test_resp.status_code, 400,
                         "Identified that a malformed URL cannot be found when requesting tag")

    def test_large_data_set(self):

        # todo: Some machines may process the test dataset quickly enough to fail this condition

        url = r'file:test_files/large_data_set.html'
        payload = {"url": url, 'tag': 'html'}
        test_resp = requests.post('http://localhost:8080/count', data=json.dumps(payload), headers=self.headers)

        self.assertEqual(test_resp.status_code, 503,
                         "Identified that dataset will take longer than five seconds to process")

    def test_missing_arg_tag(self):
        payload = {"url": "https://www.bbc.co.uk/news"}

        test_resp = requests.post('http://localhost:8080/count', data=json.dumps(payload), headers=self.headers)

        self.assertEqual(test_resp.status_code, 406,
                         "Identified that a required argument is missing for tag response")

    def test_health_under_load(self):
        payload = {"url": r'file:test_files/large_data_set.html', "tag": "html"}

        health_count = []
        for i in range(20):
            threading.Thread(target=requests.post, args=('http://localhost:8080/count',
                                                         json.dumps(payload),
                                                         self.headers)).start()

            test_resp = requests.get('http://localhost:8080/health')
            health_count.append(test_resp.status_code)

        self.assertEqual(set(health_count), {200},
                         "Health service has remained up for duration of request spam")


if __name__ == "__main__":
    # Run the html parser server
    # subprocess.Popen(['python', 'html_parse_server.py'])
    # Run the unittests
    unittest.main()
