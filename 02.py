from flask import Flask, render_template


@app.route('/')
def hello_world():
    return 'Hello, World!'
