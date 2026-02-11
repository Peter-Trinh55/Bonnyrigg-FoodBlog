from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

recipe_tags = db.Table(
    "recipe_tags",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipe.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(80), nullable=False, default="default.jpg")
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    recipes = db.relationship("Recipe", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', admin={self.is_admin})"

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    summary = db.Column(db.String(240), nullable=True)
    image_file = db.Column(db.String(80), nullable=False, default="default_recipe.jpg")

    cuisine = db.Column(db.String(50), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)
    cook_time_mins = db.Column(db.Integer, nullable=True)

    ingredients = db.Column(db.Text, nullable=False)      # newline separated
    instructions = db.Column(db.Text, nullable=False)     # newline separated
    video_url = db.Column(db.String(255), nullable=True)

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    comments = db.relationship("Comment", backref="recipe", lazy=True, cascade="all, delete-orphan")
    tags = db.relationship("Tag", secondary=recipe_tags, lazy="subquery",
                           backref=db.backref("recipes", lazy=True))

    def __repr__(self):
        return f"Recipe('{self.title}', '{self.date_posted}')"

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return f"Tag('{self.name}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Comment(recipe_id={self.recipe_id}, user_id={self.user_id})"
