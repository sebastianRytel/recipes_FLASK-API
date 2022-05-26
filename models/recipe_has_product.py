from db import db


class RecipeHasProductModel(db.Model):
    __tablename__ = "recipe_has_product"

    id = db.Column(db.Integer, primary_key=True)
    id_ingredient = db.Column(db.Integer, db.ForeignKey("ingredient.id"))
    id_recipe = db.Column(db.Integer, db.ForeignKey("recipe.id"))


class RecipeModel(db.Model):
    __tablename__ = "recipe"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    directions = db.Column(db.String(80))
    recipe_has_product = db.relationship("RecipeHasProductModel")

    def __init__(self, title: str, directions: str):
        self.title = title
        self.directions = directions

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class IngredientModel(db.Model):
    __tablename__ = "ingredient"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    measure = db.Column(db.String(10))
    amount = db.Column(db.Float)
    recipe_has_product = db.relationship("RecipeHasProductModel")

    def __init__(self, title: str, measure: float, amount: int):
        self.title = title
        self.measure = measure
        self.amount = amount

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()