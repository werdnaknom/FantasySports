
from flask import render_template, redirect, url_for, abort, flash, request,
current_app, make_response

from app.main import main
from app.main.forms import CreateProductForm

from app.models import Product

from app import db


@main.route('/', methods=['GET', 'POST'])
def index():
    form = CreateProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('index.html', form=form)
