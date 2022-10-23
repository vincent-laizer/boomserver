from app import app
import os

port = int(os.environ.get('PORT', 33507))

if "__main__" == __name__:
    app.run(host='0.0.0.0', port=port)