from flask_restx import Api, Resource, Namespace, fields
from flask import Flask, request, jsonify
from config import DevConfig
from models import Recipe, User
from exts import db
from flask_migrate import Migrate 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required

recipe_ns = Namespace('recipe', description = 'A namespacefor Recipes')


# model serializer (expose our db in terms of a json)
recipe_model = recipe_ns.model(
    "Recipe",
    {
        "id": fields.Integer(),
        "title": fields.String(),
        "description": fields.String()
    }
)


@recipe_ns.route('/recipes')
class RecipesResource(Resource):
    #returns a list 
    @recipe_ns.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes from DB"""
        resipes = Recipe.query.all()
        return resipes

    #returns 1 object
    @recipe_ns.marshal_with(recipe_model)
    @recipe_ns.expect(recipe_model)    
    def post(self):
        """Create a new recepie"""
        data = request.get_json()
        new_recipe = Recipe(
            title = data.get('title'),
            description = data.get('description')
        )
        print('We are creating a new recipe! ')
        new_recipe.save()
        #Sucsesful Create
        return new_recipe, 201

@recipe_ns.route('/recipe/<int:id>')
class RecipeResource(Resource):

    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def get(self,id):
        """Get a recipe by ID"""
        recipe = Recipe.query.get_or_404(id)
        return recipe

    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def put(self,id):
        """Update a recipe"""
        recipe_to_update = Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe_to_update.update(data.get("title"), data.get("description"))
        return recipe_to_update
    
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def delete(self,id):
        """Delete a recipe by ID"""
        recipe_to_delete = Recipe.query.get_or_404(id)
        recipe_to_delete.delete()
        return recipe_to_delete
        
