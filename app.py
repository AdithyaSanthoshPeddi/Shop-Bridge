from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "shopbridge_secret_key"

# Store shops and products
shops = {}

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]
        session["role"] = role
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- HOME ----------------
@app.route("/")
def home():
    if "role" not in session:
        return redirect("/login")

    # Buyer sees all shops
    if session["role"] == "buyer":
        return render_template("shops.html", shops=shops, role="buyer")

    # Owner sees his shop only
    if session["role"] == "owner":
        if "shop_name" in session:
            return redirect(url_for("view_shop", shop_name=session["shop_name"]))
        return redirect("/add_shop")

# ---------------- ADD SHOP (OWNER ONLY) ----------------
@app.route("/add_shop", methods=["GET", "POST"])
def add_shop():
    if session.get("role") != "owner":
        return "Access Denied"

    if request.method == "POST":
        shop_name = request.form["shop_name"]
        shops[shop_name] = []
        session["shop_name"] = shop_name
        return redirect(url_for("view_shop", shop_name=shop_name))

    return render_template("add_shop.html")

# ---------------- VIEW PRODUCTS ----------------
@app.route("/shop/<shop_name>")
def view_shop(shop_name):
    products = shops.get(shop_name, [])
    return render_template(
        "products.html",
        shop_name=shop_name,
        products=products,
        role=session["role"]
    )

# ---------------- ADD PRODUCT (OWNER ONLY) ----------------
@app.route("/add/<shop_name>", methods=["GET", "POST"])
def add_product(shop_name):
    if session.get("role") != "owner":
        return "Access Denied"

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        shops[shop_name].append({"name": name, "price": price})
        return redirect(url_for("view_shop", shop_name=shop_name))

    return render_template("add_product.html", shop_name=shop_name)

app.run(debug=True)
