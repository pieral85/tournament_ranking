# Doc found on
# https://exploreflask.com/en/latest/organizing.html#:~:text=Module%20%2D%20A%20module%20is%20a,essentially%20multiple%20modules%20packaged%20together.
# run.py	This is the file that is invoked to start up a development server. It gets a copy of the app from your package and runs it. This won’t be used in production, but it will see a lot of mileage in development.

from web.my_app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
