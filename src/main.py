"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Bookmarks, Characters, Planets
#from models import Person
import json

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# 
#               -Inicio de GET-
# 

# Endpoint para tarer todos los usuarios
@app.route('/users', methods=['GET'])
def get_all_users():

    users = Users.query.all() # esto obtiene todos los registros de la tabla User
    results = list(map(lambda item: item.serialize(), users)) #esto serializa los datos del arrays users

    return jsonify(results), 200

# Endpoint para traer un usuario
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = Users.query.filter_by(id=user_id).first()

    return jsonify(user.serialize()), 200

# Endpoint para tarer todos los planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planets.query.all() # esto obtiene todos los registros de la tabla Planets
    results = list(map(lambda item: item.serialize(), planets)) #esto serializa los datos del arrays planets

    return jsonify(results), 200

# Endpoint para traer un planeta
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planets.query.filter_by(id=planet_id).first()

    return jsonify(planet.serialize()), 200

# Endpoint para tarer todos los personajes
@app.route('/people', methods=['GET'])
def get_all_characters():

    characters = Characters.query.all() # esto obtiene todos los registros de la tabla Characters
    results = list(map(lambda item: item.serialize(), characters)) #esto serializa los datos del arrays characters

    return jsonify(results), 200

# Endpoint para traer un personaje
@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):

    character = Characters.query.filter_by(id=people_id).first()

    return jsonify(character.serialize()), 200

# Endpoint para tarer todos los favoritos
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_all_bookmarks(user_id):

    bookmarks = Bookmarks.query.filter_by(user_id=user_id).all() # esto obtiene todos los registros de la tabla Bookmarks
    results = list(map(lambda item: item.serialize(), bookmarks)) #esto serializa los datos del arrays bookmarks
    print(results)
    return jsonify(results), 200

# Endpoint para traer un favorito
@app.route('/users/<int:user_id>/favorites/<int:bookmark_id>', methods=['GET'])
def get_bookmark(user_id, bookmark_id):

    bookmark = Bookmarks.query.filter_by(id=bookmark_id).first()

    return jsonify(bookmark.serialize()), 200

# 
#               -fIN de GET-
# 

# 
#               -Inicio de POST-
# 

# Endpoint para crear usuario
@app.route('/users/new', methods=['POST'])
def create_user():
    body = json.loads(request.data)

    query_email = Users.query.filter_by(email=body["email"]).first()
    query_user_name = Users.query.filter_by(user_name=body["user_name"]).first()
    print(query_email)
    print(query_user_name)
    
    if (query_email is None) and (query_user_name is None):
        #guardar datos recibidos a la tabla User
        new_user = Users(user_name=body["user_name"],first_name=body["first_name"],last_name=body["last_name"],email=body["email"],password=body["password"])
        db.session.add(new_user)
        db.session.commit()
        response_body = {
                "msg": "created user"
            }
        return jsonify(response_body), 200

    if query_email is not None:
        response_body = {
                "msg": "existed email"
            }
        return jsonify(response_body), 400

    if query_user_name is not None:
        response_body = {
                "msg": "existed user name"
            }
        return jsonify(response_body), 400

#endpoint para crear planeta
@app.route('/planets/new', methods=['POST'])
def create_planets():
    body = json.loads(request.data)

    query_planet = Planets.query.filter_by(name=body["name"]).first()
    
    if query_planet is None:
        #guardar datos recibidos a la tabla Planet
        new_planet = Planets(name=body["name"],climate=body["climate"],population=body["population"],orbital_period=body["orbital_period"],rotation_period=body["rotation_period"],diameter=body["diameter"])
        db.session.add(new_planet)
        db.session.commit()
        response_body = {
                "msg": "created planet"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "existed planet"
        }
    return jsonify(response_body), 400

# #endpoint para crear personaje
@app.route('/people/new', methods=['POST'])
def create_characters():
    body = json.loads(request.data)

    query_character = Characters.query.filter_by(name=body["name"]).first()
    
    if query_character is None:
        #guardar datos recibidos a la tabla character
        new_character = Characters(name=body["name"],birth_year=body["birth_year"],gender=body["gender"],height=body["height"],skin_color=body["skin_color"],eye_color=body["eye_color"])
        db.session.add(new_character)
        db.session.commit()
        response_body = {
                "msg": "created character"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "existed character"
        }
    return jsonify(response_body), 400

#endpoint para crear favorito
@app.route('/favorites/new', methods=['POST'])
def create_bookmark():
    body = json.loads(request.data)

    query_user = Users.query.filter_by(id=body["user_id"]).first()
    print(query_user)
    
    if query_user is None:
        response_body = {
            "msg": "no existe el usuario"
        }
        return jsonify(response_body), 400

    #guardar datos recibidos a la tabla User
    new_bookmark = Bookmarks(user_id=body["user_id"],character_id=body["character_id"],planet_id=body["planet_id"])
    db.session.add(new_bookmark)
    db.session.commit()
    response_body = {
            "msg": "created favorite"
        }

    return jsonify(response_body), 200

# 
#               -fIN de POST-
# 

# 
#               -Inicio de DELETE-
# 

#endpoint para ELIMINAR un usuario
@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.filter_by(id=user_id).first()

    if user is None:
        raise APIException('User not found', status_code=404)

    db.session.delete(user)
    db.session.commit()
    response_body = {"msg": "Usuario eliminado"}
    return jsonify(response_body), 200


#endpoint para ELIMINAR un personaje
@app.route('/people/delete/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    people = Characters.query.filter_by(id=people_id).first()

    if people is None:
        raise APIException('Character not found', status_code=404)

    db.session.delete(people)
    db.session.commit()
    response_body = {"msg": "Personaje eliminado"}
    return jsonify(response_body), 200

#endpoint para ELIMINAR un planeta
@app.route('/planet/delete/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()

    if planet is None:
        raise APIException('Planet not found', status_code=404)

    db.session.delete(planet)
    db.session.commit()
    response_body = {"msg": "Planeta eliminado"}
    return jsonify(response_body), 200

#endpoint para ELIMINAR un favorito
@app.route('/favorites/delete/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Bookmarks.query.filter_by(id=favorite_id).first()

    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()
    response_body = {"msg": "Se ha eliminado el favorito"}
    return jsonify(response_body), 200


# 
#               -fIN de DELETE-
# 

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
