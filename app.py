# Install Flask
from flask import Flask

#Create a New Flask App Instance
app = Flask(__name__)

# create our first route
@app.route('/')

# Create  function called Hello world
def hello_world():
    return 'Hello world'

