from flask import jsonify, render_template, redirect, request
from os import path 
from flask_login import login_user, logout_user, login_required, current_user
from models import Command, Product, User
from forms import ProductForm, RegisterForm, LoginForm
from ext import app,db

products = []

profiles = []

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("miro.html", products=products)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit_product/<int:product_id>", methods=["POST", "GET"] )
@login_required
def edit_product(product_id):
    product= Product.query.get(product_id)
    form= ProductForm(name=product.name, price=product.price)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.save()
        return redirect("/")
    return render_template("create_product.html", form=form)

@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    
    product.delete()

    return redirect("/")

@app.route("/product/<int:product_id>")
def product(product_id):
    product= Product.query.get(product_id)
    commands = Command.query.filter_by(product_id=product_id).all()
    return render_template("prod_details.html", product=product, commands=commands )

@app.route("/login", methods=["GET","POST"])
def login():

    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        valid = User.query.filter(User.username == form.username.data).first()
        if valid:
            print(User.username)
        else:
            new_user= User(username=form.username.data, password= form.password.data)
            new_user.create()
            login_user(new_user)
            return redirect("/")
    return render_template("reg.html", form=form)

@app.route("/create_product", methods=["GET","POST"] )
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product=Product(name=form.name.data, price=form.price.data, info=form.info.data)

        image= form.img.data
        directory= path.join(app.root_path, "static", "images", image.filename )
        image.save(directory)
        new_product.img = image.filename

        new_product.create()
        return redirect("/")

    return render_template("create_product.html", form=form)

@app.route("/profile/<int:profile_id>")
def profile(profile_id):
    print("Reccived profile id", profile_id)
    return render_template("profile.html", user=profiles[profile_id])

@app.route('/buy_product', methods=['POST'])
def buy_product():
    data = request.get_json()
    product_id = data.get('productId')

    success = True

    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 400
    
@app.route('/save_command', methods=['POST'])
def save_command():
    data = request.get_json()
    new_command = Command(command=data['command'], product_id=data['product_id'])
    try:
        db.session.add(new_command)
        db.session.commit()
        return jsonify({'success': True}), 200
    except:
        return jsonify({'success': False}), 500
    
@app.route('/search')
def search():
    query = request.args.get('query')
    products = Product.query.filter(Product.name.contains(query)).all()
    return render_template('search_results.html', products=products)