from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re
# model the class after the user table from our database

DATABASE = 'login_and_reg'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('first_flask').query_db(query)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users with cls.
        for user in results:
            users.append( cls(user) )
        return users
# used to save a users info
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validate_user(user):
        #assuming the user puts in the correct amount of charcters return true.
        is_valid=True
        #checking the length of user is at least 2 charcters if not it will return false.
        if len(user['first_name']) < 2:
            flash("Need at least 3 characters in first name!")
            is_valid=False
        if len(user['last_name']) < 2:
            flash("Need at least 3 characters in last name!")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address try again!")
            is_valid=False
        if len(user['password']) < 8:
            flash("Need at least 8 characters in password!")
            is_valid=False
        if user['confirm_password'] != user['password']:
            flash("Need to match your password!")
            is_valid=False
        return is_valid
    @classmethod
    def get_email(cls,data):
        #looking to see if user has an email in our database.
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_and_reg").query_db(query,data)
        # if the users email didnt match or exist in our database return false.
        if len(result) < 1:
            return False
        # returning the first instance.
        return cls(result[0])