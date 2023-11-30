import requests as req


def index_check():
    r = req.get('127.0.0.1:5000/')
    if r == 200:
        return '200 OK'
    else:
        return 'TEST NOT ASSERTED'


def catalog_check():
    r = req.get('127.0.0.1:5000/catalog')
    if r == 200:
        return '200 OK'
    else:
        return 'TEST NOT ASSERTED'


def cart_check():
    r = req.get('127.0.0.1:5000/cart')
    if r == 200:
        return '200 OK'
    else:
        return 'TEST NOT ASSERTED'


def signin_check():
    r = req.get('127.0.0.1:5000/signin')
    if r == 200:
        return '200 OK'
    else:
        return 'TEST NOT ASSERTED'


def signup_check():
    r = req.get('127.0.0.1:5000/signup')
    if r == 200:
        return '200 OK'
    else:
        return 'TEST NOT ASSERTED'


def contact_check():
    r = req.get('127.0.0.1:5000/contact')
    if r == 200:
        return '200 OK'
    else:
        return 'TEST NOT ASSERTED'