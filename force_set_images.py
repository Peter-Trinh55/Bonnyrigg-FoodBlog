from flaskblog import create_app, db
from flaskblog.models import Recipe

app = create_app()

# Hard-set images by exact title OR (if titles differ) by ID order.
TITLE_TO_IMAGE = {
    "Spaghetti Bolognese (Family Style)": "spaghetti_bolognese.jpg",
    "Pesto Chicken Penne": "pesto_chicken_penne.jpg",
    "Vegetable Fried Rice (Leftover Rice)": "veg_fried_rice.jpg",
    "Honey Soy Chicken Rice Bowls": "honey_soy_chicken_bowl.jpg",
    "Beef Tacos (School Classic)": "beef_tacos.jpg",
    "Chicken Quesadillas": "chicken_quesadillas.jpg",
    "Banana Pancakes": "banana_pancakes.jpg",
    "Chocolate Mug Cake (Microwave)": "chocolate_mug_cake.jpg",
    "Chicken Caesar Salad": "chicken_caesar_salad.jpg",
    "Avocado Toast (Student Breakfast)": "avocado_toast.jpg",
}

with app.app_context():
    updated = 0
    not_matched = []

    # Try exact-title mapping first
    for r in Recipe.query.all():
        if r.title in TITLE_TO_IMAGE:
            r.image_file = TITLE_TO_IMAGE[r.title]
            updated += 1
        else:
            not_matched.append(r.title)

    db.session.commit()

    print("UPDATED:", updated)
    print("NOT MATCHED TITLES:")
    for t in not_matched:
        print("-", repr(t))
