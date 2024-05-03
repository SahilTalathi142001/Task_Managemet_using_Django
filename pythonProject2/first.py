from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector as mysql

app = Flask(__name__)

# Establish a connection to the MySQL database
mydatabase = mysql.connect(
    host="localhost",
    user="root",
    password="jaybhagat18@",
    database="pythondb2"
)

# Route for creating a new recipe
@app.route('/', methods=['GET', 'POST'])
def new_recipe():
    if request.method == 'POST':
        name = request.form['name']
        # Assuming the form contains input fields for ingredients, instructions, and categories
        ingredients = request.form.getlist('ingredients')
        instructions = request.form.getlist('instructions')
        categories = request.form.getlist('categories')

        # Insert the new recipe into the database
        cur = mydatabase.cursor()
        cur.execute("INSERT INTO recipes (name) VALUES (%s)", (name,))
        recipe_id = cur.lastrowid

        # Insert ingredients
        for ingredient in ingredients:
            cur.execute("INSERT INTO ingredients (recipe_id, name) VALUES (%s, %s)", (recipe_id, ingredient))

        # Insert instructions
        for idx, instruction in enumerate(instructions, start=1):
            cur.execute("INSERT INTO instructions (recipe_id, step, instruction) VALUES (%s, %s, %s)", (recipe_id, idx, instruction))

        # Insert categories
        for category in categories:
            cur.execute("INSERT INTO recipe_categories (recipe_id, category) VALUES (%s, %s)", (recipe_id, category))

        mydatabase.commit()
        cur.close()

        return redirect(url_for('recipe'))
    else:
        return render_template('create_recipe.html')

# Route for viewing all recipes
@app.route('/recipes', methods=['GET'])
def recipe():
    cur = mydatabase.cursor()
    cur.execute("SELECT * FROM recipes")
    recipes = cur.fetchall()
    cur.close()
    return render_template('view_all_recipes.html', recipes=recipes)

# Route for viewing a specific recipe
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    cur = mydatabase.cursor()
    query = "SELECT * FROM recipes WHERE id = %s"
    cur.execute(query, (recipe_id,))
    recipe = cur.fetchone()

    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404

    cur.execute("SELECT name FROM ingredients WHERE recipe_id = %s", (recipe_id,))
    ingredients = [ingredient[0] for ingredient in cur.fetchall()]

    cur.execute("SELECT instruction FROM instructions WHERE recipe_id = %s", (recipe_id,))
    instructions = [instruction[0] for instruction in cur.fetchall()]


    cur.execute("SELECT category FROM recipe_categories WHERE recipe_id = %s", (recipe_id,))
    categories = [category[0] for category in cur.fetchall()]

    cur.close()

    return render_template('view_specific_recipe.html', recipe={"name": recipe[1], "ingredients": ingredients, "instructions": instructions, "categories": categories})

# Route for updating a recipe
@app.route('/recipes/<int:recipe_id>/edit', methods=['GET','POST'])
def edit_recipe(recipe_id):
    if request.method == 'POST':
        name = request.form['name']
        # Assuming the form contains input fields for ingredients, instructions, and categories
        ingredients = request.form.getlist('ingredients')
        instructions = request.form.getlist('instructions')
        categories = request.form.getlist('categories')

        # Update the recipe in the database
        cur = mydatabase.cursor()
        cur.execute("UPDATE recipes SET name = %s WHERE id = %s", (name, recipe_id))

        # Delete existing ingredients, instructions, and categories
        cur.execute("DELETE FROM ingredients WHERE recipe_id = %s", (recipe_id,))
        cur.execute("DELETE FROM instructions WHERE recipe_id = %s", (recipe_id,))
        cur.execute("DELETE FROM recipe_categories WHERE recipe_id = %s", (recipe_id,))

        # Insert ingredients
        for ingredient in ingredients:
            cur.execute("INSERT INTO ingredients (recipe_id, name) VALUES (%s, %s)", (recipe_id, ingredient))

        # Insert instructions
        for idx, instruction in enumerate(instructions, start=1):
            cur.execute("INSERT INTO instructions (recipe_id, step, instruction) VALUES (%s, %s, %s)", (recipe_id, idx, instruction))

        # Insert categories
        for category in categories:
            cur.execute("INSERT INTO recipe_categories (recipe_id, category) VALUES (%s, %s)", (recipe_id, category))

        mydatabase.commit()
        cur.close()

        return redirect(url_for('recipe'))
    else:
        cur = mydatabase.cursor()
        query = "SELECT * FROM recipes WHERE id = %s"
        cur.execute(query, (recipe_id,))
        recipe = cur.fetchone()

        if not recipe:
            return jsonify({"message": "Recipe not found"}), 404

        cur.execute("SELECT name FROM ingredients WHERE recipe_id = %s", (recipe_id,))
        ingredients = [ingredient[0] for ingredient in cur.fetchall()]

        cur.execute("SELECT instruction FROM instructions WHERE recipe_id = %s", (recipe_id,))
        instructions = [instruction[0] for instruction in cur.fetchall()]

        cur.execute("SELECT category FROM recipe_categories WHERE recipe_id = %s", (recipe_id,))
        categories = [category[0] for category in cur.fetchall()]

        cur.close()

        return render_template('edit_recipe.html', recipe={"id": recipe_id, "name": recipe[1], "ingredients": ingredients, "instructions": instructions, "categories": categories})

# Route for deleting a recipe
@app.route('/recipes/<int:recipe_id>/delete', methods=['POST', 'DELETE'])
def delete_recipe(recipe_id):
    if request.method in ['POST', 'DELETE']:
        try:
            cur = mydatabase.cursor()

            # Delete associated ingredients
            cur.execute("DELETE FROM ingredients WHERE recipe_id = %s", (recipe_id,))

            # Delete associated instructions
            cur.execute("DELETE FROM instructions WHERE recipe_id = %s", (recipe_id,))

            # Delete associated categories
            cur.execute("DELETE FROM recipe_categories WHERE recipe_id = %s", (recipe_id,))

            # Finally, delete the recipe
            cur.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))

            mydatabase.commit()
            cur.close()

            return redirect(url_for('recipe'))
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return "Method Not Allowed", 405


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
