from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "I got your secret key right here"
