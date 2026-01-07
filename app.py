from flask import Flask, render_template, request, redirect

app = Flask(__name__)

products = []

@app.route("/")
def home():
    return render_template("index.html", products=products)

@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        products.append({"name": name, "price": price})
        return redirect("/")
    return render_template("add_product.html")

app.run(debug=True)
