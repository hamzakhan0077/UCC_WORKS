
import os, sys
sys.path.insert(0, os.path.abspath(".."))

from uccworks import app










if __name__ == '__main__':

    app.run(debug=True) # this runs in debug mode you don't have to set environment variables
    # print(__name__)
    # print(app)
    # print()
