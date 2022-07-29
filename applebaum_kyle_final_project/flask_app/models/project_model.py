from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Project:
    db_name = 'projex'

    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO projects (name, description, user_id) VALUES (%(name)s,%(description)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM projects;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_projects = []
        for row in results:
            all_projects.append(cls(row))
        return all_projects

    # @classmethod
    # def get_all_with_user(cls):
    #     query = "select concat(first_name,' ', last_name) as artist, paintings.* from users join paintings on users.id=paintings.user_id;"
    #     results = connectToMySQL(cls.db_name).query_db(query)
    #     all_paintings_with_artist = []
    #     for row in results:
    #         all_paintings_with_artist.append(cls(row))
    #     return all_paintings_with_artist

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM projects WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE projects SET name=%(name)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM projects WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_project(project):
        is_valid = True
        if len(project['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters", "project")
        if len(project['description']) < 10:
            is_valid = False
            flash("Description must be at least 10 characters", "project")
        return is_valid
