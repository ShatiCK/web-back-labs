from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    return "Третья лабораторная работа - в разработке"