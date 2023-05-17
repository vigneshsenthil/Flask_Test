
Flask Healthcare API
Using Flask to build a Restful API

Integration with 
Flask-SQLalchemy

SQL ORM: Flask-SQLalchemy




Installation
Install with pip:

$ pip install -r requirements.txt
Flask Application Structure
.
| |────DBmodels/
| | |────__init__.py
| | | ------ models.py
|──────main.py

Flask Configuration
Example
app = Flask(__name__)
app.config['DEBUG'] = True
Configuring From Files
Example Usage
app = Flask(__name__ )
app.config.from_pyfile('config.Development.cfg')
cfg example

##Flask settings
DEBUG = True  # True/False
TESTING = False


Builtin Configuration Values
SERVER_NAME: the name and port number of the server.





Run Flask
Run flask for develop
$ python main.py
In flask, Default port is 5000


Run flask for production
** Run with gunicorn **

In webapp/

$ gunicorn -w 4 -b 127.0.0.1:5000 run:app

-w : number of worker
-b : Socket to bind
Run with Docker
$ docker build -t flask-example .

$ docker run -p 5000:5000 --name flask-example flask-example 
 
In image building, the webapp folder will also add into the image

Flask
Flask-SQLalchemy
gunicorn
