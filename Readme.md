# Word count Web Service
***
This project runs a web service that will count the number of words contained in a HTML tag.
Given a request containing a URL and tag the service will download the source from the URL and count the number of words contained in the provided HTML tag.

## Table of contents
[Summary](#summary)
[Environment](#environment)
[Installation] (#installation)
[Discussion] (#discussion)
[Usage] (#usage)

## Summary
The server is "html_parse_server.py" which has dependencies on "html_parser.py" and "utils.py" to serve the word cout and health functionality of the web service. By default we run our service on localhost:8080.

There is a "unittest_html_parse_server.py" included alongside a coverage report for those unittests - expected PASS is 100%.

## Environment
* Windows 11 (Build 22000.856)
* python 3.9.13
* python packages contained in requirements.txt
* docker client version 20.10.17

## Installation
### Docker
To create and run the docker container:
* cd .
* docker build . --tag html_server:latest
* docker run -ti -p 8080:8080 html_server:latest

This will expose port 8080 to the local machine so unittests can be run either inside container or on local operating system.

To log into container and run a unittest:
* docker exec -it <CONTAINER_ID> /bin/bash
* cd /home
* python .\unittest_html_parse_server.py --verbose

### Python
Following initial install of Python run the following to install dependencies:
* python -m pip install requirements.txt

## Discussion
Python was chosen as the programming language as it is the primary language of the developer.
Flask was chosen as it is a lightweight, industry standard web service with good online documentation and support.

Discussions around maintainability/extension are contained inside the python scripts under "# todo:" statements.

An example customer API has been included.

## Usage
Create docker container and run server using the command above.
Log into container /home directory and run the unittest or extend the customer API.


