from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

app = Flask(__name__)
#move bcrypt below app = Flask!!
bcrypt=Bcrypt(app)
app.secret_key ='im done'