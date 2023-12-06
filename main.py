from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods=["GET"])
def random_cafe():
    cafes = Cafe.query.all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })

@app.route("/all", methods=["GET"])
def all_cafes():
    cafes = Cafe.query.all()
    all_cafes = []
    for cafe in cafes:
        all_cafes.append({
            "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
        })
    return jsonify(cafes=all_cafes)

@app.route("/search", methods=["GET"])
def search_cafe():
    location = request.args.get("loc")
    cafes = Cafe.query.filter_by(location=location).all()
    all_cafes = []
    for cafe in cafes:
        all_cafes.append({
            "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
        })
    if len(all_cafes) == 0:
        return jsonify(error={
            "Not Found": "Sorry, we don't have a cafe at that location."
        })
    return jsonify(cafes=all_cafes)

@app.route("/add", methods=["POST"])
def add_cafe():
    data = request.json
    print(data)
    new_cafe = Cafe(
        id=random.randint(1, 100000),
        name=data.get("name"),
        map_url=data.get("map_url"),
        img_url=data.get("img_url"),
        location=data.get("location"),
        seats=data.get("seats"),
        has_toilet=bool(data.get("has_toilet")),
        has_wifi=bool(data.get("has_wifi")),
        has_sockets=bool(data.get("has_sockets")),
        can_take_calls=bool(data.get("can_take_calls")),
        coffee_price=data.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={
        "success": "Successfully added the new cafe."
    })

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        new_price = request.json.get("new_price")
        print(new_price)
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={
            "success": "Successfully updated the price."
        })
    else:
        return jsonify(error={
            "Not Found": "Sorry, we don't have a cafe with that id."
        }), 404
    
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.json.get("api_key")
    print(api_key)
    if api_key == "TopSecretAPIKey":
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={
                "success": "Successfully deleted the cafe."
            })
        else:
            return jsonify(error={
                "Not Found": "Sorry, we don't have a cafe with that id."
            }), 404
    else:
        return jsonify(error={
            "Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."
        }), 403

# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
