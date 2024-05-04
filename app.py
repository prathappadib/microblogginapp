import datetime
from pymongo import MongoClient
from flask import Flask , render_template, request


def create_app():
    app = Flask(__name__)


    client =  MongoClient("mongodb://localhost:27017")
    app.db = client["microblogging"]
    collection = app.db['entries']


    @app.route('/', methods = ["GET","POST"])
    def home_page():
        """_summary_

        Returns:
            _type_: "HTML Form data"
        """
        if request.method == "POST":
            entered_content = request.form.get("content") # gettingthe data from the form
            if entered_content != "":
                formateddate = datetime.datetime.today().strftime("%Y-%m-%d")
                collection.insert_one({
                    'text': str(entered_content),
                    'date' : formateddate
                })
            
        entries_with_newdate = [
            (
                entry["text"], 
                entry["date"]  ,
                datetime.datetime.strptime(entry["date"] , "%Y-%m-%d").strftime("%b %d")
            )
            for entry in collection.find({})
        ]
        print(entries_with_newdate)
        return render_template("home.html", entries = entries_with_newdate)
    return app

if __name__ == "__main__":
    create_app.run(debug=True)
      
# End-of-file (EOF)