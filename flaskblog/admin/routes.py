from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from flaskblog import db
from flaskblog.models import Recipe, Comment, Tag

admin = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)

@admin.route("/")
@login_required
def dashboard():
    admin_required()
    recipe_count = Recipe.query.count()
    comment_count = Comment.query.count()
    tag_count = Tag.query.count()
    return render_template("admin/dashboard.html", title="Admin", recipe_count=recipe_count, comment_count=comment_count, tag_count=tag_count)

@admin.route("/recipes")
@login_required
def manage_recipes():
    admin_required()
    recipes = Recipe.query.order_by(Recipe.date_posted.desc()).all()
    return render_template("admin/recipes.html", title="Manage Recipes", recipes=recipes)

@admin.route("/comments")
@login_required
def manage_comments():
    admin_required()
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template("admin/comments.html", title="Manage Comments", comments=comments)

@admin.route("/comment/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    admin_required()
    c = Comment.query.get_or_404(comment_id)
    db.session.delete(c)
    db.session.commit()
    flash("Comment removed.", "info")
    return redirect(url_for("admin.manage_comments"))

@admin.route("/tags", methods=["GET", "POST"])
@login_required
def manage_tags():
    admin_required()
    if request.method == "POST":
        name = (request.form.get("name") or "").strip().lower()
        if name and len(name) <= 40:
            if not Tag.query.filter_by(name=name).first():
                db.session.add(Tag(name=name))
                db.session.commit()
                flash("Tag added.", "success")
            else:
                flash("Tag already exists.", "warning")
        else:
            flash("Invalid tag name.", "danger")
        return redirect(url_for("admin.manage_tags"))
    tags = Tag.query.order_by(Tag.name.asc()).all()
    return render_template("admin/tags.html", title="Manage Tags", tags=tags)

@admin.route("/tag/<int:tag_id>/delete", methods=["POST"])
@login_required
def delete_tag(tag_id):
    admin_required()
    t = Tag.query.get_or_404(tag_id)
    db.session.delete(t)
    db.session.commit()
    flash("Tag deleted.", "info")
    return redirect(url_for("admin.manage_tags"))
