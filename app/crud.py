from sqlalchemy.orm import Session
from app.models import User, Todo

# ---------------- USERS ---------------- #

def create_user(db: Session, user, password_hash):
    # check if user exists
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        return None

    db_user = User(
        username=user.username,
        age=user.age,
        email=user.email,
        password=password_hash
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def update_user(db: Session, username: str, user_update):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    user.age = user_update.age
    user.email = user_update.email

    db.commit()
    db.refresh(user)
    return user


def login(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    return user.password


def delete_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    db.delete(user)
    db.commit()
    return True


# ---------------- TODOS ---------------- #

def create_todos(db: Session, username: str, title: str):
    todo = Todo(
        title=title,
        owner=username,
        completed=False
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(db: Session, username: str):
    return db.query(Todo).filter(Todo.owner == username).all()


def update_todo(db: Session, id: int, username: str, todo_update):
    todo = (
        db.query(Todo)
        .filter(Todo.id == id, Todo.owner == username)
        .first()
    )

    if not todo:
        return None

    todo.title = todo_update.title
    todo.completed = todo_update.completed

    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, username: str, id: int):
    todo = (
        db.query(Todo)
        .filter(Todo.id == id, Todo.owner == username)
        .first()
    )

    if not todo:
        return None

    db.delete(todo)
    db.commit()
    return True
