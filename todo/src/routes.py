from flask import Flask, jsonify, redirect,request,session,flash, url_for
from flask import render_template
import requests
  
app=Flask(__name__)





if __name__ == '__main__':
    app.run(debug=True, port=8000)
    