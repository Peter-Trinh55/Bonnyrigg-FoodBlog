from flaskblog import create_app, db, bcrypt
from flaskblog.models import User, Recipe, Comment

app = create_app()

FAKE_USERS = [
    ("Aisha", "aisha@student.local"),
    ("Omar", "omar@student.local"),
    ("Layla", "layla@student.local"),
    ("Zain", "zain@student.local"),
    ("Noah", "noah@student.local"),
    ("Mia", "mia@student.local"),
]

FAKE_COMMENTS = [
    "Made this for lunch — super easy and tasty!",
    "The steps were clear. I added extra garlic and it was amazing.",
    "This would be perfect for a school fundraiser stall.",
    "I tried it with less salt and it still worked great.",
    "Loved it. Next time I’ll add chili flakes for spice.",
    "10/10. The cook time estimate was accurate.",
]

def get_or_create_user(username, email, password="Student123!"):
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return user

with app.app_context():
    db.create_all()

    recipes = Recipe.query.all()
    if not recipes:
        print("No recipes found. Run seed.py first.")
        raise SystemExit(1)

    users = [get_or_create_user(name, email) for name, email in FAKE_USERS]

    created = 0
    for i, recipe in enumerate(recipes):
        u1 = users[i % len(users)]
        u2 = users[(i + 1) % len(users)]

        c1 = Comment(body=FAKE_COMMENTS[(i * 2) % len(FAKE_COMMENTS)], recipe_id=recipe.id, user_id=u1.id)
        c2 = Comment(body=FAKE_COMMENTS[(i * 2 + 1) % len(FAKE_COMMENTS)], recipe_id=recipe.id, user_id=u2.id)

        db.session.add(c1)
        db.session.add(c2)
        created += 2

    db.session.commit()
    print(f"Done! Added {len(users)} users and {created} comments.")
    print("Fake user password = Student123!")
