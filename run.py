from flask import Flask
from app import app_init

app: Flask = app_init()

if __name__ == "__main__":
    app.run(debug=False)