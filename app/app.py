from flask import render_template, redirect, session, flash, url_for, request, logging, jsonify
from flask_mail import Message

from sqlalchemy.dialects.postgresql import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user

import psycopg2
import logging

from app.forms.email_form import EmailSenderForm
from app.forms.signin_form import LoginForm
from app.forms.signup_form import RegisterForm

from app.functions import resize_and_convert_to_jpg
from app.models import User, Poop, CartItem
from app import app, db, mail, login_manager


def get_pg_connect():
    conn = psycopg2.connect(host="localhost", port=44444, database='postgres', user='yana',
                            password='yana', )
    return conn


@app.route('/')
def index():
    form = EmailSenderForm()
    cart_items = CartItem.query.all()
    total_cart_price = sum(item.subtotal for item in cart_items)
    items_quantity = sum(item.quantity for item in cart_items)
    if form.validate_on_submit():
        email = request.form.get("email")
        msg = "Лучший корм у нас."
        sender = "tel89103680607@gmail.com"
        message = Message(msg, sender=sender, recipients=[email])
        msg_body = (
            "Корм для животных бывает разный. Выбирайте нашу компанию и делайте своих животных здоровее!"
        )
        data = {
            "title": msg,
            "body": msg_body
        }
        message.html = render_template("/Email/email.html", data=data)
        try:
            mail.send(message)
            flash("Вы успешно зарегистрировались в нашей компании!")
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            return f"error {e}"

    return render_template('/MainPage/index.html', form=form, cart=total_cart_price, quantity=items_quantity)


@app.route('/cart')
def cart():
    cart_items = CartItem.query.all()
    total_cart_price = sum(item.subtotal for item in cart_items)
    return render_template('/Cart/index.html', cart_items=cart_items, total_price=total_cart_price)


@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    product = Poop.query.get_or_404(product_id)
    cart_item = CartItem(product=product)
    db.session.add(cart_item)
    db.session.commit()

    cart_item.update_total_price()
    db.session.commit()

    return redirect(url_for('catalog'))


@app.route('/catalog')
def catalog():
    poop = Poop.query.all()
    return render_template('/Catalog/index.html', poop=poop)


@app.route('/cart_empty')
def cart_empty():
    return render_template('/CartEmpty/index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if session.get('data'):
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            try:
                user = User.query.filter_by(email=email).first()

                if user and not check_password_hash(user.password, password):
                    flash('Перепроверь входные данные.')
                    return render_template('/Authorization/index.html', form=form)
                login_user(user)
                return redirect(url_for('profile'))

            except Exception as ex:
                logging.error(ex, exc_info=True)
                flash("Произошла ошибка при входе. Пожалуйста, попробуйте снова позже.")

    return render_template('/Authorization/index.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if session.get('data'):
        return redirect('/')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        form = RegisterForm()
        try:
            user = User.query.filter_by(email=email).first()

            if user:
                flash(f'Пользователь с почтой {email} уже зарегистрирован')
                return render_template('/Registration/index.html', form=form)

            new_user = User(email=email,
                            password=generate_password_hash(password),)
            db.session.add(new_user)
            db.session.commit()
            flash("Вы зарегистрировались!")
            return redirect('/signin')
        except Exception as ex:
            logging.error(ex, exc_info=True)

            return f"Error: {ex}"

    return render_template('/Registration/index.html', form=form)


@app.route('/profile')
def profile():
    return render_template('/Profile/index.html')


@app.route('/delete_session')
def delete_session():
    session.pop('data', None)
    return redirect('/')


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        email = request.form.get("email")
        msg = Message("Вам поступило новое обращение на сайте", sender='petts.shop123@gmail.com',
                      recipients=[email])
        msg.body = f"""
        Корм для животных бывает разный. Выбирайте нашу компанию и делайте своих животных здоровее!
        """
        mail.send(msg)
        flash("")
        return redirect('/')
    else:
        return redirect('/')


@app.route('/p', methods=['GET', 'POST'])
def p():
    if request.method == 'POST':
        photo = request.files['photo']

        if photo:
            photo_data = photo.read()
            conn = get_pg_connect()

            cursor = conn.cursor()
            try:
                jpg_data = resize_and_convert_to_jpg(photo_data)

                cursor.execute(
                    "UPDATE poop SET photo = %s WHERE id = 1",
                    (jpg_data,)
                )

                conn.commit()
                conn.close()
            except Exception as ex:
                logging.error(ex, exc_info=True)
                conn.rollback()
                conn.close()
                return f"Error:"

    return render_template('PhotoUpdate/photo.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
