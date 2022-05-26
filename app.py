from flask import Flask, request, jsonify, make_response
from db import db
from models.recipe_has_product import IngredientModel
from models.recipe_has_product import RecipeModel
from models.recipe_has_product import RecipeHasProductModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/api/recipe/new", methods=["POST"])
def recipe():

    response = request.get_json()
    # # try:
    # #     response = json.loads(response)
    # # except json.JSONDecodeError:
    # #     return make_response("Invalid input", 400)
    # for key in ["title", "directions", "ingredients"]:
    #     if key not in response.keys():
    #         return make_response("Invalid input", 400)
    #
    #
    #
    new_recipe = {
        "title": response["title"],
        "directions": response["directions"],
        "ingredients": response["ingredients"],
    }

    recip = RecipeModel(title=new_recipe["title"], directions=new_recipe["directions"])
    recip.save_to_db()
    for ingredient in new_recipe["ingredients"]:
        new_ingredient = IngredientModel(title=ingredient["title"], measure=ingredient["measure"], amount=ingredient["amount"])
        new_ingredient.save_to_db()

    return jsonify({"id": recip.id}), 200

    # recipes.append(new_recipe)
    # return jsonify({"id": new_recipe["id"]}), 200


# @app.route("/api/recipe", methods=["GET"])
# def get_recipe():
#     if not recipes:
#         return jsonify({{"error": "No recipe here yet"}})
#     ingredients = request.args
#     split_ingredients = ingredients.get("ingredients").split("|")
#     matching_recips = []
#     not_matching_recips = []
#     for recip in recipes:
#         ingredients = recip.get("ingredients")
#         ingr = [ingredient.get("title") for ingredient in ingredients]
#         remaining_ingredients = set(ingr) - set(split_ingredients)
#
#         if not remaining_ingredients:
#             matching_recips.append(recip)
#
#         elif remaining_ingredients:
#             not_matching_recips.append(recip)
#
#     if matching_recips:
#         return jsonify(matching_recips), 200
#     elif not matching_recips:
#         return jsonify({"error": "No recipe here yet"})
#     elif not_matching_recips:
#         return jsonify({"error": "No recipe for these ingredients"})
#
#
#
# @app.route("/api/recipe/<int:id>", methods=["GET"])
# def get_recipe_by_id(id):
#     for recip in recipes:
#         if recip["id"] == id:
#             print(recip["id"])
#             return {
#                 "title": recip["title"],
#                 "directions": recip["directions"],
#                 "ingredients": recip["ingredients"],
#             }
#     return jsonify("Recip not found"), 404
#
#
# @app.route("/api/recipe/all", methods=["GET"])
# def get_recipe_all():
#     return jsonify({"recipes": recipes})


if __name__ == "__main__":
    app.run(debug=True)
