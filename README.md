# ARS (Advertisement Recommender System)
ARS is a stand-alone, self-contained system which takes a website's user engagement data as input, and for every page in that website outputs a suggested price for an advertisement. ARS also incorporates an ad-keyword query feature so that a user is able to query the system with keywords related to the product which the user is attempting to advertise, and the ARS suggests pages where that keyword would be relevant.

## Getting Started
This section lists all the necessary prerequisites needed for running the ARS as well instructions on how to install them.

### Prerequisites
- Python3
- PIP Package Manager
- Flask Micro Web Framework 
- Flask SQL Alchemy
- Flask Login
- Flask WTF
- WTForms
- Beautiful Soup HTML Parser

### Installing
1. [Python3](https://www.python.org/downloads/)
2. [pip package manager](https://pip.pypa.io/en/stable/installing/)
3. Flask
```
$ pip3 install flask
```
4. Flask SQLAlchemy
```
$ pip3 install flask-sqlalchemy
```
5. Flask Login
```
$ pip3 install flask-login
```
6. Flask WTF
```
$ pip3 install flask-wtf
```
7. WTForms
```
$ pip3 install wtforms
```
8. Beautiful Soup
```
$ pip3 install bs4
```

## Starting the ARS
1. Navigate to the root directory of the ARS
2. Double-click the file app.py
3. Launch a web browser
4. In the URL bar type `localhost:8080`

## Licenses
### The MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
