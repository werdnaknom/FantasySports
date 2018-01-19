from flask import render_template, redirect, url_for, abort, flash, request, \
current_app, make_response

from app.main import main
from app.main.forms import CreateProductForm

from app.models import Product, Silicon, ProductSilicon

from app import db


@main.route('/', methods=['GET', 'POST'])
def index():
    products = Product.query.all()
    silicon = Silicon.query.all()
    ps = ProductSilicon.query.all()
    return render_template('index.html', products=products)

@main.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    title = "Add Product"
    form = CreateProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data)
        Products.add(product)
        return redirect(url_for('.index'))
    return render_template('basic_form.html', form=form, title=title) 

