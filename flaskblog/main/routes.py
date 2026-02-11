from flask import Blueprint, render_template, request
from flaskblog.models import Recipe, Tag

# Create the Blueprint for the "main" section of the site (home/about/tips).
main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    # Read the current page number from the query string (e.g. /home?page=2).
    page = request.args.get("page", 1, type=int)

    # Query recipes in reverse chronological order and paginate results for performance.
    recipes = (
        Recipe.query
        .order_by(Recipe.date_posted.desc())
        .paginate(page=page, per_page=6)
    )

    # Pull recipes tagged as "featured" to display in the homepage carousel.
    # This query MUST stay inside the route to ensure an active Flask app context.
    featured = (
        Recipe.query
        .join(Recipe.tags)
        .filter(Tag.name == "featured")
        .order_by(Recipe.date_posted.desc())
        .limit(5)
        .all()
    )

    # Fetch a small list of tags for the sidebar "Top tags" section.
    top_tags = [
        t.name
        for t in Tag.query.order_by(Tag.name.asc()).limit(10).all()
    ]

    # Render the homepage with recipes, featured carousel items, and sidebar tags.
    return render_template(
        "main/home.html",
        recipes=recipes,
        featured=featured,
        top_tags=top_tags
    )

@main.route("/tips")
def tips():
    # Simple tips list used to make the site feel complete for marking.
    tips_list = [
        {"title": "Kitchen Safety Basics", "body": "Wash hands, tie hair back, and keep your bench clean."},
        {"title": "How to Season Properly", "body": "Taste as you go. Add salt gradually and balance with acid (lemon/vinegar)."},
        {"title": "Food Storage", "body": "Cool foods quickly, refrigerate within 2 hours, and label containers."},
    ]

    # Render the tips page as a clean, static content section.
    return render_template("main/tips.html", title="Cooking Tips", tips=tips_list)

@main.route("/about")
def about():
    # About page gives context for the school project and how to use the site.
    return render_template("main/about.html", title="About")

@main.route("/categories")
def categories():
    tiles = [
        {"title": "Italian", "q": {"cuisine": "Italian"}, "img": "cat_italian.jpg"},
        {"title": "Asian", "q": {"cuisine": "Asian"}, "img": "cat_asian.jpg"},
        {"title": "Mexican", "q": {"cuisine": "Mexican"}, "img": "cat_mexican.jpg"},
        {"title": "Dessert", "q": {"cuisine": "Dessert"}, "img": "cat_dessert.jpg"},
        {"title": "Easy", "q": {"difficulty": "Easy"}, "img": "cat_easy.jpg"},
        {"title": "Under 30 mins", "q": {"max_time": "30"}, "img": "cat_quick.jpg"},
    ]

    # Latest recipes preview (fills the page visually).
    latest = Recipe.query.order_by(Recipe.date_posted.desc()).limit(6).all()

    # Popular tags (quick navigation).
    top_tags = [t.name for t in Tag.query.order_by(Tag.name.asc()).limit(12).all()]

    return render_template(
        "main/categories.html",
        title="Categories",
        tiles=tiles,
        latest=latest,
        top_tags=top_tags
    )
