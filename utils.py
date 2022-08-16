import os

import urllib.request
import urllib.error
from html_parser import HTMLParser


def health_check():
    """
    Run set of health checks contained in this file

    :return response, code: string and integer response from health request to service
    """
    s_resp, s_code = service_health_check()
    c_resp, c_code = connection_health_check()

    # If there is an internal server error we report that as more fundamental than other checks
    # Otherwise report the outbound connection result whether positive/negative.
    if s_code != 200:
        return s_resp, s_code
    else:
        return c_resp, c_code


def service_health_check():
    """
    Verify that service is running by parsing local file

    :return: JSON string specifying whether service is working
    """
    url = 'file:' + os.path.join('test_files', 'basic_test.html')
    parser = HTMLParser(url=url)
    response = parser.text()

    expected_response = {'tell': 2, 'the': 1, 'audience': 1, 'what': 2, "youre": 1, 'going': 1,
                         'to': 1, 'say': 2, 'it': 1, 'then': 1, 'them': 1, "youve": 1, 'said': 1}

    if expected_response != response:
        return {"health": "HTML Parser service not running"}, 503

    return {"health": "HTML Parser service is good"}, 200


def connection_health_check():
    """
    Verify outbound connection from service.
    Assumption made that BBC news will always be up and accessible

    :return: JSON string specifying health of outbound connection
    """
    try:
        HTMLParser(url='https://www.bbc.co.uk/news')
    except ValueError:
        return {"health": "URL provided is not valid"}, 504
    except urllib.error.URLError:
        return {"health": "URL provided does not return response"}, 504

    return {"health": "HTML Parser service is good"}, 200



