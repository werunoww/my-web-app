from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/index')
@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/rules')
def rules():
    return render_template('main/rules.html')