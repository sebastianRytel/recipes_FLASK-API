import json
import sys
import re
from sqlalchemy import any_
import tests

from flask import Flask, request, jsonify, make_response
from werkzeug.exceptions import abort

from db import db
from models.recipe_has_product import IngredientModel
from models.recipe_has_product import RecipeModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

def input_validation(response):
    for key in ["title", "directions", "description", "ingredients"]:
        if key not in response.keys():
            return False
    for k, v in response.items():
        if not v:
            return False
    return True


@app.route("/api/recipe/new", methods=["POST"])
def recipe():
    response = request.get_json()
    try:
        response = json.loads(response)
    except json.JSONDecodeError:
        return make_response("Invalid input", 400)

    if not input_validation(response):
        return make_response("Invalid input", 400)

    new_recipe = {
        "title": response["title"],
        "directions": response["directions"],
        "description": response["description"],
        "ingredients": response["ingredients"],
    }

    recipe = RecipeModel.query.filter_by(title=new_recipe['title']).first()
    if not recipe:
        recip = RecipeModel(title=new_recipe["title"], description=new_recipe["description"])
        recip.directions = response['directions']
        recip.save_to_db()
        for ingredients in new_recipe["ingredients"]:
            new = IngredientModel(**ingredients)
            recip.ingredients.append(new)
            new.save_to_db()
        return jsonify({"id": recip.id}), 200
    else:
        return jsonify({'message': f'Recipe "{new_recipe["title"]}" already exists'})


@app.route("/api/recipe", methods=["GET"])
def get_recipe():
    all_recipes = RecipeModel.query.all()
    if not all_recipes:
        return jsonify({"error": "No recipe here yet"})
    ingredients = request.args
    max_directions = ingredients.get("max_directions")
    split_ingredients = ingredients.get("ingredients").split("|")
    matching_recips = []
    for recip in all_recipes:
        ingredients = recip.get_ingredients()
        remaining_ingredients = set(ingredients) - set(split_ingredients)
        if not remaining_ingredients:
            matching_recips.append(recip.json_get_with_id())
    if matching_recips:
        for x in matching_recips:
            if max_directions:
                if len(x['directions']) > int(max_directions):
                    return jsonify([])
        return jsonify(sorted(matching_recips, key=lambda x: x['title'], reverse=True)), 200
    return jsonify(matching_recips)


@app.route("/api/recipe/<int:id>", methods=["GET"])
def get_recipe_by_id(id):
    recipe = RecipeModel.query.filter_by(id=id).first()
    if not recipe:
        return make_response("Recip not found"), 404
    return recipe.json_get_without_id()


@app.route("/api/recipe/<int:id>", methods=["PUT"])
def update_recipe_by_id(id):
    recipe_by_id = RecipeModel.query.filter_by(id=id).first()
    if not recipe_by_id:
        return make_response("Recip not found"), 404

    response = request.get_json()
    response = json.loads(response)

    if not input_validation(response):
        return make_response("Invalid input", 400)

    if recipe_by_id:
        db.session.delete(recipe_by_id)
        db.session.commit()

        new_recipe = {
            "title": response["title"],
            "directions": response["directions"],
            "description": response["description"],
            "ingredients": response["ingredients"],
        }

        recip = RecipeModel(title=new_recipe["title"], description=new_recipe["description"])
        recip.directions = response['directions']
        recip.save_to_db()
        for ingredients in new_recipe["ingredients"]:
            new = IngredientModel(**ingredients)
            recip.ingredients.append(new)
            new.save_to_db()

    return make_response(""), 204


@app.route("/api/recipe/<int:id>", methods=["DELETE"])
def delete_recipe_by_id(id):
    recipe = RecipeModel.query.filter_by(id=id).first()
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return make_response("", 204)
    return abort(404)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)
