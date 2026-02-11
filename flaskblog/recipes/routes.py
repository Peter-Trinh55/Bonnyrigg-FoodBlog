from flask import Blueprint, render_template, request, url_for, flash, redirect, abort
from flask_login import login_required, current_user

# Import the database session so we can commit changes.
from flaskblog import db

# Import models used in recipe CRUD, filtering, and comments.
from flaskblog.models import Recipe, Tag, Comment

# Import WTForms used for creating/editing recipes and adding comments.
from flaskblog.recipes.forms import RecipeForm, CommentForm

# Utility function for safely saving and resizing uploaded images.
from flaskblog.utils import save_image

# Create a Blueprint to logically group all recipe-related routes.
recipes = Blueprint("recipes", __name__)


def _parse_tags(tag_string: str):
    """
    Convert a comma-separated tag string into a clean list of unique tag names.

    This function:
    - Normalises case (lowercase)
    - Trims whitespace
    - Enforces a maximum length
    - Preserves user-entered order
    """
    # If no tags were provided, return an empty list early.
    if not tag_string:
        return []

    # Split by commas and normalise individual tag strings.
    raw = [t.strip().lower() for t in tag_string.split(",")]

    # Filter out empty or excessively long tag names.
    names = []
    for t in raw:
        if t and len(t) <= 40:
            names.append(t)

    # Remove duplicates while preserving original order.
    seen = set()
    out = []
    for n in names:
        if n not in seen:
            out.append(n)
            seen.add(n)

    return out


@recipes.route("/recipes")
def recipe_list():
    """
    Display a paginated list of recipes with optional filters applied.

    Filters are passed via query parameters so they can be combined:
    - search
    - cuisine
    - difficulty
    - max_time
    - ingredient
    - tag
    """
    # Read the current page number for pagination (?page=2).
    page = request.args.get("page", 1, type=int)

    # Read and sanitise all filter inputs from the query string.
    search = request.args.get("search", "", type=str).strip()
    cuisine = request.args.get("cuisine", "", type=str).strip()
    difficulty = request.args.get("difficulty", "", type=str).strip()
    max_time = request.args.get("max_time", "", type=str).strip()
    ingredient = request.args.get("ingredient", "", type=str).strip()
    tag = request.args.get("tag", "", type=str).strip().lower()

    # Start with a base query that can be built dynamically.
    query = Recipe.query

    # Apply keyword search across title and summary fields.
    if search:
        query = query.filter(
            (Recipe.title.ilike(f"%{search}%")) |
            (Recipe.summary.ilike(f"%{search}%"))
        )

    # Apply cuisine filter if provided.
    if cuisine:
        query = query.filter(Recipe.cuisine == cuisine)

    # Apply difficulty filter if provided.
    if difficulty:
        query = query.filter(Recipe.difficulty == difficulty)

    # Apply maximum cook time filter (only if numeric).
    if max_time.isdigit():
        query = query.filter(Recipe.cook_time_mins <= int(max_time))

    # Apply ingredient keyword search inside ingredients text.
    if ingredient:
        query = query.filter(Recipe.ingredients.ilike(f"%{ingredient}%"))

    # Apply tag-based filtering using the many-to-many relationship.
    if tag:
        query = query.join(Recipe.tags).filter(Tag.name == tag)

    # Order results newest-first and paginate to limit DB load.
    recipes_paginated = (
        query
        .order_by(Recipe.date_posted.desc())
        .paginate(page=page, per_page=6)
    )

    # Build lists used to populate filter dropdowns in the UI.
    cuisines = [
        c[0]
        for c in db.session.query(Recipe.cuisine)
        .distinct()
        .filter(Recipe.cuisine.isnot(None))
        .all()
    ]
    difficulties = ["Easy", "Medium", "Hard"]
    tags = [t.name for t in Tag.query.order_by(Tag.name.asc()).all()]

    # Render the recipe list page with filters and paginated results.
    return render_template(
        "recipes/list.html",
        title="Recipes",
        recipes=recipes_paginated,
        cuisines=cuisines,
        difficulties=difficulties,
        tags=tags,
        filters=dict(
            search=search,
            cuisine=cuisine,
            difficulty=difficulty,
            max_time=max_time,
            ingredient=ingredient,
            tag=tag
        )
    )


@recipes.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def recipe_detail(recipe_id):
    """
    Display a single recipe and handle comment submission.

    Comments are only accepted from authenticated users.
    """
    # Fetch the recipe or return a 404 if it does not exist.
    recipe = Recipe.query.get_or_404(recipe_id)

    # Initialise the comment form.
    form = CommentForm()

    # Handle comment submission.
    if form.validate_on_submit():
        # Prevent anonymous users from posting comments.
        if not current_user.is_authenticated:
            flash("Please log in to comment.", "info")
            return redirect(
                url_for(
                    "users.login",
                    next=url_for("recipes.recipe_detail", recipe_id=recipe_id)
                )
            )

        # Create and persist the new comment.
        comment = Comment(
            body=form.body.data,
            recipe_id=recipe.id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()

        flash("Comment added.", "success")
        return redirect(url_for("recipes.recipe_detail", recipe_id=recipe_id))

    # Render the recipe detail page with the comment form.
    return render_template(
        "recipes/detail.html",
        title=recipe.title,
        recipe=recipe,
        form=form
    )


@recipes.route("/recipe/new", methods=["GET", "POST"])
@login_required
def recipe_new():
    """
    Create a new recipe.

    Only authenticated users may submit recipes.
    """
    form = RecipeForm()

    if form.validate_on_submit():
        # Default image ensures the UI works even without an upload.
        image_file = "default_recipe.jpg"

        # Save and resize uploaded image if provided.
        if form.picture.data:
            image_file = save_image(
                form.picture.data,
                folder="recipe_pics",
                output_size=(1200, 1200)
            )

        # Create the recipe object using form data.
        recipe = Recipe(
            title=form.title.data,
            summary=form.summary.data,
            cuisine=form.cuisine.data or None,
            difficulty=form.difficulty.data or None,
            cook_time_mins=form.cook_time_mins.data,
            ingredients=form.ingredients.data.strip(),
            instructions=form.instructions.data.strip(),
            video_url=form.video_url.data or None,
            image_file=image_file,
            author=current_user
        )

        # Parse and attach tags using a helper function.
        tag_names = _parse_tags(form.tags.data)
        for name in tag_names:
            t = Tag.query.filter_by(name=name).first()
            if not t:
                t = Tag(name=name)
            recipe.tags.append(t)

        # Commit the new recipe and its relationships.
        db.session.add(recipe)
        db.session.commit()

        flash("Recipe published!", "success")
        return redirect(url_for("recipes.recipe_detail", recipe_id=recipe.id))

    # Render the recipe creation form.
    return render_template(
        "recipes/create_edit.html",
        title="New Recipe",
        form=form,
        legend="New Recipe"
    )


@recipes.route("/recipe/<int:recipe_id>/update", methods=["GET", "POST"])
@login_required
def recipe_update(recipe_id):
    """
    Update an existing recipe.

    Only the author or an admin user may edit a recipe.
    """
    recipe = Recipe.query.get_or_404(recipe_id)

    # Enforce ownership or admin permissions.
    if recipe.author != current_user and not current_user.is_admin:
        abort(403)

    form = RecipeForm()

    if form.validate_on_submit():
        # Replace image only if a new one is uploaded.
        if form.picture.data:
            recipe.image_file = save_image(
                form.picture.data,
                folder="recipe_pics",
                output_size=(1200, 1200)
            )

        # Update recipe fields from the form.
        recipe.title = form.title.data
        recipe.summary = form.summary.data
        recipe.cuisine = form.cuisine.data or None
        recipe.difficulty = form.difficulty.data or None
        recipe.cook_time_mins = form.cook_time_mins.data
        recipe.ingredients = form.ingredients.data.strip()
        recipe.instructions = form.instructions.data.strip()
        recipe.video_url = form.video_url.data or None

        # Reset and re-attach tags to reflect changes.
        recipe.tags.clear()
        tag_names = _parse_tags(form.tags.data)
        for name in tag_names:
            t = Tag.query.filter_by(name=name).first()
            if not t:
                t = Tag(name=name)
            recipe.tags.append(t)

        db.session.commit()
        flash("Recipe updated.", "success")
        return redirect(url_for("recipes.recipe_detail", recipe_id=recipe.id))

    # Pre-fill the form fields when loading the edit page.
    elif request.method == "GET":
        form.title.data = recipe.title
        form.summary.data = recipe.summary
        form.cuisine.data = recipe.cuisine
        form.difficulty.data = recipe.difficulty
        form.cook_time_mins.data = recipe.cook_time_mins
        form.ingredients.data = recipe.ingredients
        form.instructions.data = recipe.instructions
        form.video_url.data = recipe.video_url
        form.tags.data = ", ".join([t.name for t in recipe.tags])

    return render_template(
        "recipes/create_edit.html",
        title="Update Recipe",
        form=form,
        legend="Update Recipe"
    )


@recipes.route("/recipe/<int:recipe_id>/delete", methods=["POST"])
@login_required
def recipe_delete(recipe_id):
    """
    Delete a recipe.

    Only the author or an admin user may delete content.
    """
    recipe = Recipe.query.get_or_404(recipe_id)

    # Enforce permission check before deletion.
    if recipe.author != current_user and not current_user.is_admin:
        abort(403)

    # Remove the recipe and persist the change.
    db.session.delete(recipe)
    db.session.commit()

    flash("Recipe deleted.", "info")
    return redirect(url_for("recipes.recipe_list"))
