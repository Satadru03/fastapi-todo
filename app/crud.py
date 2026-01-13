def create_user(db, user, password_hash):
    with db.cursor() as cursor:

        cursor.execute(
            "SELECT username FROM users WHERE username = %s",
            (user.username,)
        )
        if cursor.fetchone():
            return None
        
        cursor.execute(
            "INSERT INTO users (username, age, email, password_hash) VALUES (%s, %s, %s, %s)",
            (user.username, user.age, user.email, password_hash)
        )

    db.commit()
    return user

def get_all_users(db):
    with db.cursor() as cursor:
        cursor.execute("SELECT username, age, email FROM users")
        rows = cursor.fetchall()

    users = []
    for row in rows:
        users.append({
            "username": row[0],
            "age": row[1],
            "email": row[2]
        })
    return users

def get_user(db, username: str):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT username, age, email FROM users WHERE username = %s",
            (username,)
        )
        row = cursor.fetchone()

        if not row:
            return None
    return {
        "username": row[0],
        "age": row[1],
        "email": row[2]
    }

def update_user(db, username: str, user_update):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT username FROM users WHERE username = %s",
            (username,)
        )

        if not cursor.fetchone():
            return None
        
        cursor.execute(
            "UPDATE users SET age = %s, email = %s WHERE username = %s",
            (user_update.age, user_update.email, username)
        )

    db.commit()
    return {
        "username": username,
        "age": user_update.age,
        "email": user_update.email
    }

def login(db, username:str):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = %s",
            (username,)
        )
        row = cursor.fetchone()

        if not row:
            return None
        
        return row[0]

def delete_user(db, username: str):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT username FROM users WHERE username = %s",
            (username,)
        )

        if not cursor.fetchone():
            return None
        
        cursor.execute(
            "DELETE FROM users WHERE username = %s",
            (username,)
        )

    db.commit()
    return True

def create_todos(db, username: str, title: str):
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO todos (title, owner_username) VALUES (%s, %s)",
            (title, username)
        )
        row = cursor.fetchone()
    db.commit()
    return {
        "id": row[0],
        "title": title,
        "completed": row[1]
    }

def get_todos(db, username: str):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT id, title, completed FROM todos WHERE owner_username = %s",
            (username,)
        )
        rows = cursor.fetchall()
    
    todos = []
    for row in rows:
        todos.append({
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    })
    return todos

def update_todo(db, id: int, username:str, todo_update):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT id, title, completed FROM todos WHERE id = %s AND owner_username = %s",
            (id, username)
        )
        row = cursor.fetchone()

        if not row:
            return None
        
        cursor.execute(
                "UPDATE todos SET title = %s, completed = %s WHERE id = %s AND owner_username = %s",
                (todo_update.title, todo_update.completed, id, username)
            )

    db.commit()

    return {
        "id": id,
        "title": todo_update.title,
        "completed": todo_update.completed
    }

def delete_todo(db, username: str, id: int):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM todos WHERE id = %s AND  owner_username = %s",
            (id, username)
        )

        if not cursor.fetchone():
            return None
        
        cursor.execute(
            "DELETE FROM todos WHERE id = %s AND owner_username = %s",
            (id, username)
        )

    db.commit()
    return True