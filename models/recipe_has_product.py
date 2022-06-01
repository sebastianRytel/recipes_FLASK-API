from sqlalchemy.ext.hybrid import hybrid_property

from db import db

recipe_has_product = db.Table("recipe_has_product", db.Model.metadata,
                              db.Column('ingredient_id ', db.Integer, db.ForeignKey("ingredients.id")),
                              db.Column("recipe_id", db.Integer, db.ForeignKey("recipe.id")))


class RecipeModel(db.Model):
    __tablename__ = "recipe"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(80))
    _directions = db.Column(db.String(500))

    ingredients = db.relationship("IngredientModel", secondary=recipe_has_product, backref=db.backref("ingredients", lazy='joined'), cascade="all, delete")

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @property
    def directions(self):
        return [direction for direction in self._directions.split("|")]

    @directions.setter
    def directions(self, list_of_directions):
        self._directions = "|".join(direction for direction in list_of_directions)


    def json_get_with_id(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "directions": self.directions,
            "ingredients": [ingredient.json() for ingredient in self.ingredients]
        }

    def json_get_without_id(self):
        return {
            "title": self.title,
            "description": self.description,
            "directions": self.directions,
            "ingredients": [ingredient.json() for ingredient in self.ingredients]
        }

    def get_short_info(self):
        return {
            "id": self.id,
            "title": self.title,
            "ingredients": [ingredient.json() for ingredient in self.ingredients]
        }

    def get_ingredients(self):
        return [ingredient.json()['title'] for ingredient in self.ingredients]

class IngredientModel(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    measure = db.Column(db.String(10))
    amount = db.Column(db.Float)

    def __init__(self, title: str, measure: float, amount: int):
        self.title = title
        self.measure = measure
        self.amount = amount

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def json(self):
        return {
            "title": self.title,
            "measure": self.measure,
            "amount": self.amount,
        }