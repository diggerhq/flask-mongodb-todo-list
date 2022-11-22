from os import environ

from flask import Flask, render_template, request, url_for, redirect, Response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

MONGO_URI = environ.get(
    "MONGO_URI",
    "mongodb://admin:password@localhost:27017/admin?retryWrites=true&w=majority",
)

app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)
client = mongo.cx
if mongo.db is None:
    db = client["db"]
    todos = db['todos']
else:
    todos = mongo.db.todos

@app.route("/")
def index():
    saved_todos = todos.find()
    return render_template("index.html", todos=saved_todos)


@app.route("/healthcheck")
def healthcheck():
    return Response(status=204)


@app.route("/add", methods=["POST"])
def add_todo():
    new_todo = request.form.get("new-todo")
    todos.insert_one({"text": new_todo, "complete": False})
    return redirect(url_for("index"))


@app.route("/complete/<oid>")
def complete(oid):
    todo_item = todos.find_one({"_id": ObjectId(oid)})
    todo_item["complete"] = not todo_item["complete"]
    print("updated")
    todos.update_one({"_id": ObjectId(oid)}, {"$set": todo_item}, upsert=False)
    return redirect(url_for("index"))


@app.route("/delete_completed")
def delete_completed():
    todos.delete_many({"complete": True})
    return redirect(url_for("index"))


@app.route("/delete_all")
def delete_all():
    todos.delete_many({})
    return redirect(url_for("index"))
