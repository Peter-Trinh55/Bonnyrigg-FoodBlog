# seed.py
from flaskblog import create_app, db, bcrypt
from flaskblog.models import User, Recipe, Tag

app = create_app()

SAMPLE_RECIPES = [
    {
        "title": "Chicken Shawarma Wraps",
        "summary": "Quick, school-friendly wraps with garlic sauce.",
        "cuisine": "Lebanese",
        "difficulty": "Easy",
        "cook_time_mins": 25,
        "ingredients": "500g chicken thigh\n2 tbsp yogurt\n2 tsp paprika\n1 tsp cumin\n2 cloves garlic\nSalt + pepper\nWraps\nLettuce\nTomato\nGarlic sauce",
        "instructions": "Mix yogurt + spices + garlic.\nMarinate chicken 10 mins.\nPan-fry until cooked.\nSlice and assemble in wraps.\nServe with salad and sauce.",
        "tags": ["halal", "quick", "lunch"]
    },
    {
        "title": "Pasta Primavera",
        "summary": "Colourful veggies + pasta in a light sauce.",
        "cuisine": "Italian",
        "difficulty": "Easy",
        "cook_time_mins": 20,
        "ingredients": "Pasta\nBroccoli\nCapsicum\nZucchini\nOlive oil\nGarlic\nParmesan (optional)\nSalt + pepper",
        "instructions": "Boil pasta.\nSauté garlic + veggies.\nToss with pasta.\nSeason and serve.",
        "tags": ["vegetarian", "quick", "dinner"]
    },
        {
        "title": "Honey Soy Chicken Rice Bowl",
        "summary": "Sweet-savoury chicken with rice and salad.",
        "cuisine": "Asian",
        "difficulty": "Easy",
        "cook_time_mins": 25,
        "ingredients": "Chicken\nSoy sauce\nHoney\nGarlic\nRice\nCucumber\nCarrot\nSpring onion",
        "instructions": "Cook rice.\nPan-fry chicken.\nAdd soy+honey+garlic.\nAssemble bowl with salad.\nServe.",
        "tags": ["quick", "lunch", "featured"]
    },
    {
        "title": "Vegetable Fried Rice",
        "summary": "Great way to use leftover rice.",
        "cuisine": "Asian",
        "difficulty": "Easy",
        "cook_time_mins": 15,
        "ingredients": "Cooked rice\nEggs\nPeas\nCarrot\nSoy sauce\nOil\nSpring onion",
        "instructions": "Scramble eggs.\nStir-fry veg.\nAdd rice + soy.\nMix in egg.\nServe.",
        "tags": ["quick", "vegetarian"]
    },
    {
        "title": "Beef Tacos",
        "summary": "Classic tacos with salad and salsa.",
        "cuisine": "Mexican",
        "difficulty": "Easy",
        "cook_time_mins": 20,
        "ingredients": "Minced beef\nTaco seasoning\nTaco shells\nLettuce\nTomato\nCheese\nSalsa",
        "instructions": "Cook beef with seasoning.\nPrepare toppings.\nFill shells.\nServe.",
        "tags": ["dinner", "popular", "featured"]
    },
    {
        "title": "Margherita Pizza Toast",
        "summary": "Budget-friendly pizza flavour on toast.",
        "cuisine": "Italian",
        "difficulty": "Easy",
        "cook_time_mins": 10,
        "ingredients": "Bread\nTomato paste\nCheese\nOregano\nBasil (optional)",
        "instructions": "Spread paste.\nAdd cheese.\nGrill until melted.\nTop with herbs.",
        "tags": ["quick", "snack"]
    },
    {
        "title": "Butter Chicken (Simple)",
        "summary": "Creamy curry that’s mild and family-friendly.",
        "cuisine": "Indian",
        "difficulty": "Medium",
        "cook_time_mins": 40,
        "ingredients": "Chicken\nButter\nTomato puree\nCream\nGaram masala\nGarlic\nRice",
        "instructions": "Cook chicken.\nMake sauce with tomato+spices.\nAdd cream.\nCombine.\nServe with rice.",
        "tags": ["dinner", "halal"]
    },
    {
        "title": "Greek Salad Wrap",
        "summary": "Fresh wrap with feta and crunchy veg.",
        "cuisine": "Greek",
        "difficulty": "Easy",
        "cook_time_mins": 10,
        "ingredients": "Wraps\nCucumber\nTomato\nOlives\nFeta\nLemon\nOlive oil",
        "instructions": "Chop veg.\nMix dressing.\nAssemble wrap.\nServe.",
        "tags": ["vegetarian", "lunch", "quick"]
    },
    {
        "title": "Banana Pancakes",
        "summary": "Simple pancakes with banana sweetness.",
        "cuisine": "Dessert",
        "difficulty": "Easy",
        "cook_time_mins": 15,
        "ingredients": "Flour\nMilk\nEgg\nBanana\nBaking powder\nHoney (optional)",
        "instructions": "Mix batter.\nCook on pan.\nTop with banana/honey.\nServe.",
        "tags": ["breakfast", "sweet", "featured"]
    },
    {
        "title": "Chocolate Mug Cake",
        "summary": "Fast dessert in a mug (microwave).",
        "cuisine": "Dessert",
        "difficulty": "Easy",
        "cook_time_mins": 5,
        "ingredients": "Flour\nCocoa\nSugar\nMilk\nOil\nBaking powder",
        "instructions": "Mix in mug.\nMicrowave 60–90s.\nCool.\nEat.",
        "tags": ["quick", "sweet"]
    },
    {
        "title": "Chicken Caesar Salad",
        "summary": "Salad with chicken, croutons, and dressing.",
        "cuisine": "Western",
        "difficulty": "Easy",
        "cook_time_mins": 20,
        "ingredients": "Chicken\nLettuce\nCroutons\nParmesan\nCaesar dressing",
        "instructions": "Cook chicken.\nAssemble salad.\nAdd dressing.\nTop with cheese.",
        "tags": ["lunch", "healthy"]
    },
    {
        "title": "Spaghetti Bolognese",
        "summary": "A school classic, perfect for families.",
        "cuisine": "Italian",
        "difficulty": "Easy",
        "cook_time_mins": 35,
        "ingredients": "Spaghetti\nMinced beef\nOnion\nGarlic\nTomato sauce\nSalt + pepper",
        "instructions": "Cook pasta.\nCook beef + onion + garlic.\nAdd sauce.\nSimmer.\nServe.",
        "tags": ["dinner", "popular"]
    },
        # ======================
    # ITALIAN
    # ======================
    {
        "title": "Spaghetti Bolognese (Family Style)",
        "summary": "Rich tomato mince sauce with garlic and herbs — a school favourite.",
        "cuisine": "Italian",
        "difficulty": "Easy",
        "cook_time_mins": 35,
        "image_file": "spaghetti_bolognese.jpg",
        "ingredients": (
            "400g spaghetti\n"
            "500g minced beef\n"
            "1 onion, diced\n"
            "2 cloves garlic, crushed\n"
            "2 tbsp olive oil\n"
            "700g passata (tomato puree)\n"
            "2 tbsp tomato paste\n"
            "1 tsp dried oregano\n"
            "1 tsp dried basil\n"
            "Salt + pepper\n"
            "Optional: parmesan + chopped parsley"
        ),
        "instructions": (
            "1) Boil spaghetti in salted water until al dente. Drain.\n"
            "2) Heat oil in a pan, cook onion 3–4 mins until soft.\n"
            "3) Add garlic 30 seconds, then add mince. Brown it fully.\n"
            "4) Stir in tomato paste, then add passata + herbs.\n"
            "5) Simmer 12–15 mins. Season.\n"
            "6) Serve sauce over spaghetti. Add parmesan if you want."
        ),
        "tags": ["italian", "dinner", "popular", "easy"]
    },
    {
        "title": "Pesto Chicken Penne",
        "summary": "Creamy pesto pasta with chicken and spinach.",
        "cuisine": "Italian",
        "difficulty": "Easy",
        "cook_time_mins": 25,
        "image_file": "pesto_chicken_penne.jpg",
        "ingredients": (
            "350g penne pasta\n"
            "2 chicken breasts, sliced\n"
            "2 tbsp olive oil\n"
            "2 cloves garlic, crushed\n"
            "3 tbsp pesto\n"
            "150ml cream (or evaporated milk)\n"
            "2 cups baby spinach\n"
            "Salt + pepper\n"
            "Optional: parmesan"
        ),
        "instructions": (
            "1) Cook pasta and drain.\n"
            "2) Cook chicken in oil 6–8 mins until done.\n"
            "3) Add garlic 30 seconds.\n"
            "4) Stir in pesto + cream.\n"
            "5) Add spinach until wilted.\n"
            "6) Toss through pasta. Season and serve."
        ),
        "tags": ["italian", "quick", "under30", "easy", "featured"]
    },

    # ======================
    # ASIAN
    # ======================
    {
        "title": "Vegetable Fried Rice (Leftover Rice)",
        "summary": "Fast fried rice with egg, veg, and soy sauce — perfect for lunch.",
        "cuisine": "Asian",
        "difficulty": "Easy",
        "cook_time_mins": 15,
        "image_file": "veg_fried_rice.jpg",
        "ingredients": (
            "3 cups cooked cold rice (best day-old)\n"
            "2 eggs\n"
            "1 carrot, diced\n"
            "1/2 cup peas\n"
            "2 tbsp oil\n"
            "2 tbsp soy sauce\n"
            "1 tsp sesame oil (optional)\n"
            "2 spring onions, sliced\n"
            "Salt + pepper"
        ),
        "instructions": (
            "1) Scramble eggs in a hot pan, remove.\n"
            "2) Stir-fry carrot + peas in oil 3 mins.\n"
            "3) Add rice and break it up.\n"
            "4) Add soy sauce + sesame oil.\n"
            "5) Stir egg back in.\n"
            "6) Top with spring onion and serve."
        ),
        "tags": ["asian", "quick", "under30", "vegetarian", "easy"]
    },
    {
        "title": "Honey Soy Chicken Rice Bowls",
        "summary": "Sweet-savoury chicken bowls with crunchy salad.",
        "cuisine": "Asian",
        "difficulty": "Easy",
        "cook_time_mins": 25,
        "image_file": "honey_soy_chicken_bowl.jpg",
        "ingredients": (
            "500g chicken thigh, sliced\n"
            "2 tbsp soy sauce\n"
            "1.5 tbsp honey\n"
            "2 cloves garlic, crushed\n"
            "1 tsp ginger (optional)\n"
            "2 tbsp oil\n"
            "Cooked rice\n"
            "Cucumber + carrot (sliced)\n"
            "Optional: mayo/sriracha"
        ),
        "instructions": (
            "1) Mix soy, honey, garlic, ginger.\n"
            "2) Cook chicken in oil 6–8 mins.\n"
            "3) Pour sauce in, bubble 2 mins until sticky.\n"
            "4) Serve on rice with cucumber/carrot.\n"
            "5) Add sauce drizzle if you like."
        ),
        "tags": ["asian", "under30", "lunch", "easy", "featured"]
    },

    # ======================
    # MEXICAN
    # ======================
    {
        "title": "Beef Tacos (School Classic)",
        "summary": "Crunchy tacos with seasoned beef, salad, and salsa.",
        "cuisine": "Mexican",
        "difficulty": "Easy",
        "cook_time_mins": 20,
        "image_file": "beef_tacos.jpg",
        "ingredients": (
            "500g minced beef\n"
            "1 onion, diced\n"
            "2 tbsp taco seasoning\n"
            "1/3 cup water\n"
            "Taco shells\n"
            "Lettuce + tomato\n"
            "Cheese\n"
            "Salsa\n"
            "Optional: avocado"
        ),
        "instructions": (
            "1) Cook onion, add beef and brown.\n"
            "2) Add taco seasoning + water. Simmer 3–4 mins.\n"
            "3) Warm taco shells.\n"
            "4) Build tacos with beef + salad + cheese + salsa.\n"
            "5) Serve immediately."
        ),
        "tags": ["mexican", "under30", "dinner", "easy", "featured"]
    },
    {
        "title": "Chicken Quesadillas",
        "summary": "Cheesy tortillas with chicken and capsicum — quick and filling.",
        "cuisine": "Mexican",
        "difficulty": "Easy",
        "cook_time_mins": 15,
        "image_file": "chicken_quesadillas.jpg",
        "ingredients": (
            "2 cooked chicken breasts, shredded (or rotisserie)\n"
            "4 tortillas\n"
            "2 cups shredded cheese\n"
            "1 capsicum, sliced\n"
            "1 tsp paprika\n"
            "Oil or butter for pan\n"
            "Optional: salsa + sour cream"
        ),
        "instructions": (
            "1) Mix chicken with paprika.\n"
            "2) Add cheese + chicken + capsicum onto a tortilla.\n"
            "3) Top with another tortilla.\n"
            "4) Pan-toast 2–3 mins each side until golden.\n"
            "5) Slice and serve with salsa."
        ),
        "tags": ["mexican", "quick", "under30", "easy"]
    },

    # ======================
    # DESSERT
    # ======================
    {
        "title": "Banana Pancakes",
        "summary": "Fluffy pancakes with banana sweetness — perfect breakfast/dessert.",
        "cuisine": "Dessert",
        "difficulty": "Easy",
        "cook_time_mins": 15,
        "image_file": "banana_pancakes.jpg",
        "ingredients": (
            "1 cup flour\n"
            "2 tsp baking powder\n"
            "1 tbsp sugar\n"
            "1 egg\n"
            "1 cup milk\n"
            "1 banana (mashed) + extra slices\n"
            "Pinch of salt\n"
            "Butter/oil for pan\n"
            "Optional: honey or maple syrup"
        ),
        "instructions": (
            "1) Mix flour, baking powder, sugar, salt.\n"
            "2) Whisk egg + milk + mashed banana.\n"
            "3) Combine wet + dry (don’t overmix).\n"
            "4) Cook small pancakes 2 mins each side.\n"
            "5) Serve with banana slices and syrup."
        ),
        "tags": ["dessert", "breakfast", "under30", "easy", "featured"]
    },
    {
        "title": "Chocolate Mug Cake (Microwave)",
        "summary": "Fast chocolate cake in a mug — ready in minutes.",
        "cuisine": "Dessert",
        "difficulty": "Easy",
        "cook_time_mins": 5,
        "image_file": "chocolate_mug_cake.jpg",
        "ingredients": (
            "4 tbsp flour\n"
            "2 tbsp cocoa\n"
            "2 tbsp sugar\n"
            "1/4 tsp baking powder\n"
            "3 tbsp milk\n"
            "2 tbsp oil\n"
            "Optional: choc chips"
        ),
        "instructions": (
            "1) Mix dry ingredients in a mug.\n"
            "2) Add milk + oil and stir smooth.\n"
            "3) Microwave 60–90 seconds.\n"
            "4) Cool 1 minute.\n"
            "5) Eat straight from mug."
        ),
        "tags": ["dessert", "quick", "under30", "easy"]
    },

    # ======================
    # EXTRA “EASY” + “UNDER 30”
    # ======================
    {
        "title": "Chicken Caesar Salad",
        "summary": "Fresh salad with chicken, croutons, and creamy dressing.",
        "cuisine": "Western",
        "difficulty": "Easy",
        "cook_time_mins": 20,
        "image_file": "chicken_caesar_salad.jpg",
        "ingredients": (
            "2 chicken breasts\n"
            "Lettuce (cos)\n"
            "Croutons\n"
            "Parmesan (optional)\n"
            "Caesar dressing\n"
            "Salt + pepper"
        ),
        "instructions": (
            "1) Season and cook chicken 6–8 mins each side.\n"
            "2) Slice chicken.\n"
            "3) Toss lettuce with dressing.\n"
            "4) Add croutons + chicken.\n"
            "5) Top with parmesan."
        ),
        "tags": ["healthy", "under30", "easy", "lunch"]
    },
    {
        "title": "Avocado Toast (Student Breakfast)",
        "summary": "Quick breakfast with avocado and optional egg.",
        "cuisine": "Western",
        "difficulty": "Easy",
        "cook_time_mins": 10,
        "image_file": "avocado_toast.jpg",
        "ingredients": (
            "Bread\n"
            "1 avocado\n"
            "Salt + pepper\n"
            "Lemon juice\n"
            "Optional: tomato slices\n"
            "Optional: fried egg"
        ),
        "instructions": (
            "1) Toast bread.\n"
            "2) Mash avocado with salt, pepper, lemon.\n"
            "3) Spread on toast.\n"
            "4) Add tomato/egg if you want."
        ),
        "tags": ["breakfast", "under30", "easy", "quick"]
    },
]


with app.app_context():
    db.create_all()

    # Create admin if not exists
    admin_email = "admin@bonnyrigg.local"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        pw = bcrypt.generate_password_hash("Admin123!").decode("utf-8")
        admin = User(username="Admin", email=admin_email, password=pw, is_admin=True)
        db.session.add(admin)
        db.session.commit()

    # Create tags + recipes
    for r in SAMPLE_RECIPES:
        existing = Recipe.query.filter_by(title=r["title"]).first()
        if existing:
            continue

        recipe = Recipe(
            title=r["title"],
            summary=r["summary"],
            cuisine=r["cuisine"],
            difficulty=r["difficulty"],
            cook_time_mins=r["cook_time_mins"],
            ingredients=r["ingredients"],
            instructions=r["instructions"],
            author=admin,
            image_file="default_recipe.jpg"
        )

        for tag_name in r["tags"]:
            tag_name = tag_name.strip().lower()
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            recipe.tags.append(tag)

        db.session.add(recipe)

    db.session.commit()
    print("Seed complete! Admin login: admin@bonnyrigg.local / Admin123!")
