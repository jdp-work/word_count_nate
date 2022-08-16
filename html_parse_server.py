import json
import urllib.request
import urllib.error
from flask import Flask, request

from func_timeout import func_timeout, FunctionTimedOut
from html_parser import HTMLParser
import utils


app = Flask(__name__)


@app.route('/', methods=['GET'])
def m():
    return "Welcome to the word count service"


@app.route('/count', methods=['POST'])
def count():
    """
    Serve the word count dictionary for all words in given tag

    return: response, code: JSON string and response code for action
    """
    try:
        req = request.json
        _verify_data(req, required_args=['url', 'tag'])
    except RuntimeError:
        return json.dumps({"error": "Expected argument is missing"}), 406

    # todo: As project scales would consider custom error handling decorators

    try:
        parser_class = HTMLParser(url=req['url'])
    except ValueError:
        return json.dumps({"error": "URL provided is not valid"}), 400
    except urllib.error.URLError:
        return json.dumps({"error": "URL provided does not return response"}), 404

    # todo: Current architecture assumes that we should process the URL on every call to get current unique data
    # todo: Could consider processing once assuming there will be multiple calls on same URL

    try:
        tag_value = req['tag']
        response = func_timeout(5, parser_class.tag, args=(str(tag_value),))
    except FunctionTimedOut:
        return json.dumps({"error": "Request took longer than 5 seconds"}), 503

    # todo: There is no request.post=="GET" method implemented which could be considered
    # todo: Would store POST response in .html which could be rendered when GET called.

    return json.dumps(response), 200


@app.route('/health', methods=['GET'])
def health():
    """
    Perform health check on internal service

    return: response, code: JSON string and response code for action
    """
    return utils.health_check()


def _verify_data(req, required_args):
    """ Verify that provided data is present and in correct format """
    for arg in required_args:
        if arg not in req:
            raise RuntimeError("Expected data not present")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
