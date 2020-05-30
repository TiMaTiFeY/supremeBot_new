import sqlite3
from sqlite3 import Error


class _DataBase:
    def __init__(self, path):
        self.connection = None
        try:
            self.connection = sqlite3.connect(path)
            # print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            # print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred:\n"+query)

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred:\n"+query)


class VkBotDataBase:
    def __init__(self):
        # Connect
        self._db = _DataBase('db.sqlite')

        # Creating tables
        query = """
                   CREATE TABLE IF NOT EXISTS respect_table (
                   user_id TEXT,
                   score INTEGER
                   );
                """
        self._db.execute_query(query)
        query = """
                   CREATE TABLE IF NOT EXISTS votekick_table (
                   user_id TEXT,
                   count INTEGER
                   );
                """
        self._db.execute_query(query)
        query = """
                   CREATE TABLE IF NOT EXISTS users_table (
                   user_id TEXT,
                   permission TEXT
                   );
                """
        self._db.execute_query(query)

    # Add
    def add_user_permission(self, user_id, permission):
        query = """
           INSERT INTO
             users_table (user_id, permission)
           VALUES
             ('{}', '{}');
           """.format(user_id, permission)
        self._db.execute_query(query)

    def add_user_respect(self, user_id, score):
        query = """
                   INSERT INTO
                     respect_table (user_id, score)
                   VALUES
                     ('{}', {});
                   """.format(user_id, score)
        self._db.execute_query(query)

    def add_user_votekick(self, user_id, count):
        query = """
                  INSERT INTO
                    votekick_table (user_id, count)
                  VALUES
                    ('{}', {});
                  """.format(user_id, count)
        self._db.execute_query(query)

    # Update by user
    def update_user_permission(self, user_id, new_permission):
        query = """
                UPDATE
                    users_table
                SET
                    permission = '{}'
                WHERE
                    user_id = '{}'
                """.format(new_permission, user_id)
        self._db.execute_query(query)

    def update_user_respect(self, user_id, new_score):
        query = """
                UPDATE
                    respect_table
                SET
                    score = {}
                WHERE
                    user_id = '{}'
                """.format(new_score, user_id)
        self._db.execute_query(query)

    def update_user_votekick(self, user_id, new_count):
        query = """
                   UPDATE
                       votekick_table
                   SET
                       count = {}
                   WHERE
                       user_id = '{}'
                   """.format(new_count, user_id)
        self._db.execute_query(query)

    # Get by user/all
    def get_user_permission(self, user_id):
        select_users = "SELECT permission FROM users_table WHERE user_id = '{}'".format(user_id)
        return self._db.execute_read_query(select_users)

    def get_user_respect(self, user_id):
        select_users = "SELECT score FROM respect_table WHERE user_id = '{}'".format(user_id)
        return self._db.execute_read_query(select_users)

    def get_all_user_respect(self):
        select_users = "SELECT * FROM respect_table"
        return self._db.execute_read_query(select_users)

    def get_user_votekick(self, user_id):
        select_users = "SELECT count FROM votekick_table WHERE user_id = '{}'".format(user_id)
        return self._db.execute_read_query(select_users)

    # Delete by user
    def delete_user_permission(self, user_id):
        query = """
                   DELETE FROM
                     users_table
                   WHERE
                     user_id = '{}'
                   """.format(user_id)
        self._db.execute_query(query)

    def delete_user_respect(self, user_id):
        query = """
                   DELETE FROM
                     respect_table
                   WHERE
                     user_id = '{}'
                   """.format(user_id)
        self._db.execute_query(query)

    def delete_user_votekick(self, user_id):
        query = """
                   DELETE FROM
                     votekick_table
                   WHERE
                     user_id = '{}'
                   """.format(user_id)
        self._db.execute_query(query)

    # Clear
    def clear_users_table(self):
        self._db.execute_query("DELETE FROM users_table")

    def clear_respect_table(self):
        self._db.execute_query("DELETE FROM respect_table")

    def clear_votekick_table(self):
        self._db.execute_query("DELETE FROM votekick_table")
