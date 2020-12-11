# If we're on windows we can run the flask project with set FLASK_APP=flashcards.py and for macOS and Linux export FLASK_APP=flashcards.py then export/set FLASK_ENV=developement then flask run // we use this method to run the project on the flask server only on developement mode and not production because it's not secure
# if we run the flask project through the flask server and set it to development mode, it will show us the occuring error in the view however if we run it with python server the way won't respond and no error appears

# The Model-template-view pattern : MTV pattern

from flask import Flask, render_template, abort, jsonify, request, redirect, url_for
from model import db, save_db

app = Flask(__name__) # Flask constructor which will create a Flask application object, we pass the application's name which is a special                                       variable containing the name of the current module
app.config["DEBUG"] = True


@app.route("/") # .route is an attribute of the app we made before / We're assigning a URL to our function 
# This is called view function
def welcome():
    return render_template("welcome.html", cards=db)

@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template("card.html", card = card, index=index, max_index = len(db)-1)
    except IndexError:
        abort(404)

@app.route("/api/card/")
def api_card_list():
    return jsonify(db)

@app.route("/api/card/<int:index>")
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)

@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        # form has been submitted, process data
        card = {"question" : request.form["question"],
                "answer": request.form["answer"]}
        db.append(card)
        return redirect(url_for('card_view', index= len(db)-1 ))
    else:
        return render_template("add_card.html")

@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return(redirect(url_for('welcome')))
        else:
            return render_template("remove_card.html", card=db[index])
    except IndexError:
        abort(404)

# Count how many time we visited the page
#counter = 0
#@app.route("/count_views")
#def count_views():
   # global counter
   # counter +=1
    #return "This page was viewed "+str(counter) +" Times !"
    
if __name__ =="__main__":
    app.run()