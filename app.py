import os
import secrets
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pyotp


# ------------------------------------------------------------
# Flask application setup
# ------------------------------------------------------------
app = Flask(__name__)

# Use an environment secret if available, otherwise generate one.
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_hex(16))

# Store data in SQLite for this school project.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bonnyrigg_pizza_blog.db"

# Disable tracking overhead to improve performance.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Keep cookies safer in the browser.
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Folder for uploaded profile pictures.
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")

# Allow common image formats only.
app.config["ALLOWED_IMAGE_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

db = SQLAlchemy(app)


# ------------------------------------------------------------
# Database models
# ------------------------------------------------------------
class User(db.Model):
    # Unique ID for each user account.
    id = db.Column(db.Integer, primary_key=True)

    # Public username shown on the site.
    username = db.Column(db.String(80), nullable=False)

    # Email used for login and verification.
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Hashed password so plain text passwords are never stored.
    password_hash = db.Column(db.String(255), nullable=False)

    # Admin accounts can access the admin dashboard.
    is_admin = db.Column(db.Boolean, default=False)

    # Optional profile image filename saved in static/uploads.
    profile_image = db.Column(db.String(150), nullable=False, default="default_avatar.png")

    # Store whether 2FA is enabled for the account.
    two_factor_enabled = db.Column(db.Boolean, default=False)

    # Secret used by authenticator apps like Google Authenticator.
    two_factor_secret = db.Column(db.String(32), nullable=True)

    # Temporary one-time email code for login or password reset.
    email_verification_code = db.Column(db.String(10), nullable=True)

    # Expiry time for the email verification code.
    email_code_expiry = db.Column(db.DateTime, nullable=True)

    # Optional password reset token for the reset flow.
    reset_token = db.Column(db.String(64), nullable=True)

    # Expiry time for the reset token.
    reset_token_expiry = db.Column(db.DateTime, nullable=True)


class Recipe(db.Model):
    # Primary key for each pizza recipe.
    id = db.Column(db.Integer, primary_key=True)

    # Recipe title shown on cards and detail pages.
    title = db.Column(db.String(120), nullable=False)

    # Recipe category such as Classic or Meat.
    pizza_type = db.Column(db.String(50), nullable=False, default="Classic")

    # Difficulty label shown on the site.
    difficulty = db.Column(db.String(20), nullable=False, default="Easy")

    # Cooking time in minutes.
    cook_time = db.Column(db.Integer, nullable=False, default=20)

    # Short introduction to the recipe.
    description = db.Column(db.Text, nullable=False)

    # Ingredients stored as a multiline text block.
    ingredients = db.Column(db.Text, nullable=False)

    # Method stored as a multiline text block.
    steps = db.Column(db.Text, nullable=False)

    # Image filename that points to static/images.
    image_filename = db.Column(db.String(150), nullable=False, default="default_pizza.jpg")

    # Timestamp used for sorting or reporting.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # All comments linked to this recipe.
    comments = db.relationship("Comment", backref="recipe", lazy=True, cascade="all, delete-orphan")


class Comment(db.Model):
    # Primary key for each comment.
    id = db.Column(db.Integer, primary_key=True)

    # Recipe foreign key.
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)

    # Name shown next to the comment.
    author_name = db.Column(db.String(80), nullable=False)

    # Comment text.
    body = db.Column(db.Text, nullable=False)

    # Timestamp for the comment.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def get_current_user():
    # Return None if the browser is not logged in.
    if not session.get("user_id"):
        return None

    # Load the current user from the database.
    return User.query.get(session["user_id"])


def allowed_image(filename):
    # Reject missing filenames quickly.
    if not filename or "." not in filename:
        return False

    # Check the extension against allowed image types.
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in app.config["ALLOWED_IMAGE_EXTENSIONS"]


def save_profile_image(file_storage):
    # Return None if nothing was uploaded.
    if not file_storage or not file_storage.filename:
        return None

    # Validate the file type before saving.
    if not allowed_image(file_storage.filename):
        return None

    # Build a safe random filename to avoid conflicts.
    extension = file_storage.filename.rsplit(".", 1)[1].lower()
    new_filename = f"profile_{secrets.token_hex(8)}.{extension}"

    # Save to the upload folder.
    full_path = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
    file_storage.save(full_path)
    return new_filename


def generate_email_code():
    # Create a 6 digit code for email verification.
    return f"{secrets.randbelow(1000000):06d}"


def send_email_code(user, purpose):
    # Generate a fresh code each time the user requests one.
    code = generate_email_code()

    # Store the code and a short expiry time.
    user.email_verification_code = code
    user.email_code_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    # Build a simple email body.
    subject = f"Bonnyrigg Pizza Blog verification code for {purpose}"
    body = (
        f"Hello {user.username},\n\n"
        f"Your 6 digit verification code is: {code}\n\n"
        f"This code will expire in 10 minutes.\n"
        f"If you did not request this, please ignore this email."
    )

    # Read Gmail SMTP details from environment variables.
    gmail_user = os.getenv("GMAIL_ADDRESS")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")

    # If Gmail credentials are configured, send the code by email.
    if gmail_user and gmail_pass:
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = gmail_user
            msg["To"] = user.email

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(gmail_user, gmail_pass)
                server.sendmail(gmail_user, [user.email], msg.as_string())

            return True, "Verification code sent to your email."
        except Exception:
            # Fall through to the debug notice below if email fails.
            pass

    # Honest fallback for local testing without SMTP configuration.
    print("=" * 60)
    print(f"EMAIL VERIFICATION CODE FOR {user.email}: {code}")
    print("=" * 60)
    return True, "Email sending is not configured, so the code was printed in the terminal for testing."


def verify_email_code(user, code):
    # Reject empty codes.
    if not code:
        return False

    # Reject if no code is stored.
    if not user.email_verification_code or not user.email_code_expiry:
        return False

    # Reject expired codes.
    if datetime.utcnow() > user.email_code_expiry:
        return False

    # Check the provided code.
    return user.email_verification_code == code.strip()


def clear_email_code(user):
    # Remove old codes after successful use.
    user.email_verification_code = None
    user.email_code_expiry = None
    db.session.commit()


def build_totp_uri(user):
    # Ensure a secret exists before generating the QR/manual key.
    if not user.two_factor_secret:
        user.two_factor_secret = pyotp.random_base32()
        db.session.commit()

    # Create an otpauth URI that authenticator apps can use.
    return pyotp.TOTP(user.two_factor_secret).provisioning_uri(
        name=user.email,
        issuer_name="Bonnyrigg Pizza Blog"
    )


def create_reset_token(user):
    # Create a secure reset token with an expiry time.
    user.reset_token = secrets.token_urlsafe(32)
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=20)
    db.session.commit()
    return user.reset_token


def verify_reset_token(token):
    # Find a matching user by reset token.
    user = User.query.filter_by(reset_token=token).first()

    # Reject invalid tokens.
    if not user:
        return None

    # Reject expired tokens.
    if not user.reset_token_expiry or datetime.utcnow() > user.reset_token_expiry:
        return None

    return user


def seed_data():
    # Create the admin account if it does not exist already.
    if not User.query.filter_by(email="admin@bonnyriggpizza.local").first():
        admin_secret = pyotp.random_base32()
        db.session.add(
            User(
                username="admin",
                email="admin@bonnyriggpizza.local",
                password_hash=generate_password_hash("PizzaPass123"),
                is_admin=True,
                two_factor_enabled=False,
                two_factor_secret=admin_secret,
            )
        )

    # Add starter recipes so the website looks complete.
    if Recipe.query.count() == 0:
        db.session.add_all([
            Recipe(
                title="Classic Margherita Pizza",
                pizza_type="Classic",
                difficulty="Easy",
                cook_time=20,
                description="A simple pizza with tomato sauce, mozzarella and basil that is ideal for a clean, traditional flavour.",
                ingredients="2 pizza dough bases\n1 cup tomato pizza sauce\n250g mozzarella cheese, grated\n8 basil leaves\n1 tablespoon olive oil\nPinch of salt",
                steps="Preheat the oven to 220°C.\nPlace the pizza bases on trays or a pizza stone.\nSpread tomato sauce evenly over each base.\nSprinkle mozzarella across the top.\nAdd basil leaves and drizzle lightly with olive oil.\nBake for 10 to 12 minutes until the crust is golden.\nSlice and serve hot.",
                image_filename="margherita.jpg",
            ),
            Recipe(
                title="Pepperoni Feast Pizza",
                pizza_type="Meat",
                difficulty="Easy",
                cook_time=22,
                description="A bold pizza topped with pepperoni, rich tomato sauce and bubbling cheese for a classic takeaway-style result.",
                ingredients="2 pizza dough bases\n1 cup tomato pizza sauce\n300g mozzarella cheese, grated\n24 slices pepperoni\n1 teaspoon dried oregano\n1 tablespoon olive oil",
                steps="Preheat the oven to 220°C.\nPlace the dough bases onto trays.\nSpread tomato sauce over both bases.\nAdd mozzarella evenly over the sauce.\nLayer the pepperoni on top and sprinkle with oregano.\nBake for 12 minutes or until the cheese is melted and lightly browned.\nRest for 2 minutes before slicing.",
                image_filename="pepperoni.jpg",
            ),
            Recipe(
                title="BBQ Chicken Pizza",
                pizza_type="Specialty",
                difficulty="Medium",
                cook_time=25,
                description="This pizza combines smoky barbecue sauce, chicken, red onion and melted cheese for a richer flavour profile.",
                ingredients="2 pizza dough bases\n3/4 cup barbecue sauce\n250g cooked chicken, shredded\n250g mozzarella cheese, grated\n1/2 red onion, thinly sliced\n1 tablespoon parsley",
                steps="Preheat the oven to 220°C.\nSpread barbecue sauce over the pizza bases.\nScatter mozzarella over the sauce.\nAdd shredded chicken and red onion slices.\nBake for 12 to 14 minutes until cooked through.\nTop with parsley and serve.",
                image_filename="bbq_chicken.jpg",
            ),
        ])

    # Add starter comments if the site has none.
    if Comment.query.count() == 0:
        db.session.add_all([
            Comment(recipe_id=1, author_name="Peter", body="The basil on this one makes it taste really fresh."),
            Comment(recipe_id=2, author_name="Henry", body="This pepperoni pizza feels like a proper takeaway style pizza."),
            Comment(recipe_id=3, author_name="An", body="The barbecue sauce gives it a really strong flavour."),
        ])

    db.session.commit()


# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------
@app.route("/")
def home():
    # Begin with all recipes.
    query = Recipe.query

    # Read filter values from the search bar.
    search = request.args.get("q", "").strip()
    pizza_type = request.args.get("pizza_type", "").strip()
    difficulty = request.args.get("difficulty", "").strip()

    # Search key recipe fields if a query exists.
    if search:
        query = query.filter(
            Recipe.title.ilike(f"%{search}%")
            | Recipe.description.ilike(f"%{search}%")
            | Recipe.ingredients.ilike(f"%{search}%")
        )

    # Apply optional filters.
    if pizza_type:
        query = query.filter_by(pizza_type=pizza_type)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    recipes = query.order_by(Recipe.title.asc()).all()
    return render_template("home.html", recipes=recipes, current_user=get_current_user())


@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def recipe_detail(recipe_id):
    # Load the recipe requested by the user.
    recipe = Recipe.query.get_or_404(recipe_id)

    # Process a new comment if the form was submitted.
    if request.method == "POST":
        author_name = request.form.get("author_name", "").strip()
        body = request.form.get("body", "").strip()

        # Reject empty comments.
        if not author_name or not body:
            flash("Please complete both comment fields.", "danger")
            return redirect(url_for("recipe_detail", recipe_id=recipe.id))

        # Save the new comment.
        db.session.add(Comment(recipe_id=recipe.id, author_name=author_name, body=body))
        db.session.commit()

        flash("Comment added successfully.", "success")
        return redirect(url_for("recipe_detail", recipe_id=recipe.id))

    # Split ingredients and steps into lists for cleaner display.
    ingredients_list = [line.strip() for line in recipe.ingredients.splitlines() if line.strip()]
    steps_list = [line.strip() for line in recipe.steps.splitlines() if line.strip()]

    return render_template(
        "recipe_detail.html",
        recipe=recipe,
        ingredients_list=ingredients_list,
        steps_list=steps_list,
        current_user=get_current_user(),
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    # Register a new normal user account.
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validate required fields.
        if not username or not email or not password:
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for("register"))

        # Block duplicate emails.
        if User.query.filter_by(email=email).first():
            flash("That email is already registered.", "danger")
            return redirect(url_for("register"))

        # Create a new user with a fresh authenticator secret.
        db.session.add(
            User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                two_factor_secret=pyotp.random_base32(),
            )
        )
        db.session.commit()

        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", current_user=get_current_user())


@app.route("/login", methods=["GET", "POST"])
def login():
    # Start the sign-in flow.
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Find the user by email.
        user = User.query.filter_by(email=email).first()

        # Reject bad credentials early.
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid login details.", "danger")
            return redirect(url_for("login"))

        # If 2FA is not enabled for this user, log them in immediately.
        if not user.two_factor_enabled:
            session["user_id"] = user.id
            session["is_admin"] = user.is_admin
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin_dashboard") if user.is_admin else url_for("home"))

        # Store a temporary pending user until second factor succeeds.
        session["pending_user_id"] = user.id

        # Choose the verification method requested by the user.
        method = request.form.get("verification_method", "authenticator")

        # If the user chose authenticator but has no secret yet, fall back to email.
        if method == "authenticator" and not user.two_factor_secret:
            method = "email"

        if method == "email":
            success, message = send_email_code(user, "login")
            flash(message, "success" if success else "danger")
            session["pending_verification_method"] = "email"
            return redirect(url_for("verify_login"))

        # Use authenticator verification only for users who enabled it.
        session["pending_verification_method"] = "authenticator"
        return redirect(url_for("verify_login"))

    return render_template("login.html", current_user=get_current_user())


@app.route("/verify-login", methods=["GET", "POST"])
def verify_login():
    # Ensure a login is currently waiting for second factor verification.
    pending_user_id = session.get("pending_user_id")
    if not pending_user_id:
        flash("Please log in first.", "danger")
        return redirect(url_for("login"))

    user = User.query.get_or_404(pending_user_id)
    method = session.get("pending_verification_method", "authenticator")

    # Process the 6 digit code.
    if request.method == "POST":
        code = request.form.get("code", "").strip()

        if method == "email":
            if not verify_email_code(user, code):
                flash("That email verification code is invalid or expired.", "danger")
                return redirect(url_for("verify_login"))
            clear_email_code(user)
        else:
            # Authenticator codes come from the user's TOTP secret.
            if not user.two_factor_secret:
                user.two_factor_secret = pyotp.random_base32()
                db.session.commit()

            totp = pyotp.TOTP(user.two_factor_secret)
            if not totp.verify(code, valid_window=1):
                flash("That authenticator code is invalid.", "danger")
                return redirect(url_for("verify_login"))

        # Finalise the login only after 2FA succeeds.
        session.pop("pending_user_id", None)
        session.pop("pending_verification_method", None)
        session["user_id"] = user.id
        session["is_admin"] = user.is_admin

        flash("Logged in successfully.", "success")
        return redirect(url_for("admin_dashboard") if user.is_admin else url_for("home"))

    # Provide a manual key if authenticator setup is needed.
    manual_key = user.two_factor_secret if method == "authenticator" else None
    return render_template(
        "verify_login.html",
        current_user=get_current_user(),
        verification_method=method,
        manual_key=manual_key,
        user=user,
    )


@app.route("/logout")
def logout():
    # Clear all session values safely.
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    # Users must be logged in to edit their profile.
    user = get_current_user()
    if not user:
        flash("Please log in first.", "danger")
        return redirect(url_for("login"))

    # Handle profile changes.
    if request.method == "POST":
        # Update the username if a new one was supplied.
        new_username = request.form.get("username", "").strip()
        if new_username:
            user.username = new_username

        # Optionally update the password.
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        if new_password or confirm_password:
            if new_password != confirm_password:
                flash("New password and confirmation do not match.", "danger")
                return redirect(url_for("profile"))
            user.password_hash = generate_password_hash(new_password)

        # Optionally replace the profile picture.
        uploaded_file = request.files.get("profile_image")
        new_image_name = save_profile_image(uploaded_file)
        if uploaded_file and uploaded_file.filename and not new_image_name:
            flash("Please upload a valid image file.", "danger")
            return redirect(url_for("profile"))
        if new_image_name:
            user.profile_image = new_image_name

        # Let the user enable or disable authenticator-based 2FA.
        enable_authenticator = request.form.get("enable_authenticator") == "on"
        user.two_factor_enabled = enable_authenticator

        # Ensure a secret exists when authenticator 2FA is enabled.
        if user.two_factor_enabled and not user.two_factor_secret:
            user.two_factor_secret = pyotp.random_base32()

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile"))

    # Show the manual key on the profile page for authenticator setup.
    manual_key = None
    if user.two_factor_secret:
        manual_key = user.two_factor_secret
    elif user.two_factor_enabled:
        user.two_factor_secret = pyotp.random_base32()
        db.session.commit()
        manual_key = user.two_factor_secret

    return render_template(
        "profile.html",
        current_user=user,
        manual_key=manual_key,
    )


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    # Step 1: request a password reset.
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        method = request.form.get("verification_method", "email")

        # Look up the user account.
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("No account was found with that email address.", "danger")
            return redirect(url_for("forgot_password"))

        # Create a reset token to identify this reset attempt.
        create_reset_token(user)

        # Store the token in the session during the verification stage.
        session["reset_token"] = user.reset_token

        # If authenticator is requested but not enabled, automatically use email.
        if method == "authenticator" and not (user.two_factor_enabled and user.two_factor_secret):
            method = "email"

        session["reset_verification_method"] = method

        if method == "email":
            success, message = send_email_code(user, "password reset")
            flash(message, "success" if success else "danger")
            return redirect(url_for("verify_reset"))
        else:
            flash("Enter your authenticator app code to continue resetting your password.", "success")
            return redirect(url_for("verify_reset"))

    return render_template("forgot_password.html", current_user=get_current_user())


@app.route("/verify-reset", methods=["GET", "POST"])
def verify_reset():
    # Step 2: verify the reset using email or authenticator.
    token = session.get("reset_token")
    if not token:
        flash("Please start the password reset process first.", "danger")
        return redirect(url_for("forgot_password"))

    user = verify_reset_token(token)
    if not user:
        flash("Your reset session has expired. Please start again.", "danger")
        session.pop("reset_token", None)
        session.pop("reset_verification_method", None)
        return redirect(url_for("forgot_password"))

    method = session.get("reset_verification_method", "email")

    if request.method == "POST":
        code = request.form.get("code", "").strip()

        if method == "email":
            if not verify_email_code(user, code):
                flash("That email verification code is invalid or expired.", "danger")
                return redirect(url_for("verify_reset"))
            clear_email_code(user)
        else:
            totp = pyotp.TOTP(user.two_factor_secret)
            if not totp.verify(code, valid_window=1):
                flash("That authenticator code is invalid.", "danger")
                return redirect(url_for("verify_reset"))

        # Mark verification as passed and send the user to set a new password.
        session["reset_verified"] = True
        flash("Verification successful. You can now set a new password.", "success")
        return redirect(url_for("reset_password"))

    manual_key = user.two_factor_secret if method == "authenticator" else None
    return render_template(
        "verify_reset.html",
        current_user=get_current_user(),
        verification_method=method,
        manual_key=manual_key,
        user=user,
    )


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    # Step 3: set a new password after 2FA verification.
    token = session.get("reset_token")
    if not token or not session.get("reset_verified"):
        flash("Please complete verification first.", "danger")
        return redirect(url_for("forgot_password"))

    user = verify_reset_token(token)
    if not user:
        flash("Your reset session has expired. Please start again.", "danger")
        session.pop("reset_token", None)
        session.pop("reset_verification_method", None)
        session.pop("reset_verified", None)
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        # Validate the new password fields.
        if not password or not confirm_password:
            flash("Please complete both password fields.", "danger")
            return redirect(url_for("reset_password"))
        if password != confirm_password:
            flash("The passwords do not match.", "danger")
            return redirect(url_for("reset_password"))

        # Save the new password and clear the reset data.
        user.password_hash = generate_password_hash(password)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        session.pop("reset_token", None)
        session.pop("reset_verification_method", None)
        session.pop("reset_verified", None)

        flash("Your password has been reset successfully.", "success")
        return redirect(url_for("login"))

    return render_template("reset_password.html", current_user=get_current_user())


@app.route("/admin")
def admin_dashboard():
    # Only admins should be able to manage site content.
    if not session.get("is_admin"):
        flash("Admin access required.", "danger")
        return redirect(url_for("login"))

    return render_template(
        "admin.html",
        recipes=Recipe.query.order_by(Recipe.id.desc()).all(),
        users_count=User.query.count(),
        comments_count=Comment.query.count(),
        current_user=get_current_user(),
    )


@app.route("/admin/add", methods=["POST"])
def add_recipe():
    # Only admins can add recipes.
    if not session.get("is_admin"):
        flash("Admin access required.", "danger")
        return redirect(url_for("login"))

    # Read all fields from the form.
    title = request.form.get("title", "").strip()
    pizza_type = request.form.get("pizza_type", "").strip()
    difficulty = request.form.get("difficulty", "").strip()
    description = request.form.get("description", "").strip()
    ingredients = request.form.get("ingredients", "").strip()
    steps = request.form.get("steps", "").strip()
    image_filename = request.form.get("image_filename", "").strip()

    # Validate the numeric field safely.
    try:
        cook_time = int(request.form.get("cook_time", "0"))
    except ValueError:
        cook_time = 0

    # Ensure all required recipe fields are complete.
    if not title or not pizza_type or not difficulty or not description or not ingredients or not steps or cook_time <= 0:
        flash("Please complete all recipe fields correctly.", "danger")
        return redirect(url_for("admin_dashboard"))

    # Use a default image if nothing was entered.
    if not image_filename:
        image_filename = "default_pizza.jpg"

    # Save the new recipe.
    db.session.add(
        Recipe(
            title=title,
            pizza_type=pizza_type,
            difficulty=difficulty,
            cook_time=cook_time,
            description=description,
            ingredients=ingredients,
            steps=steps,
            image_filename=image_filename,
        )
    )
    db.session.commit()

    flash("Pizza recipe added successfully.", "success")
    return redirect(url_for("admin_dashboard"))


# ------------------------------------------------------------
# Main entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    # Ensure the upload folder exists before the app starts.
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Create tables and seed starter data.
    with app.app_context():
        db.create_all()
        seed_data()

    # Run the development server locally.
    app.run(debug=True)
