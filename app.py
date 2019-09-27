from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Playliter
playlists = db.playlists

app = Flask(__name__)

@app.route('/')
def playlists_index():
    """Show all playlists."""
    #playlists = [
    #{ 'title': 'Cat Videos', 'description': 'Cats acting weird' },
    #{ 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
    #]
    return render_template('playlists_index.html', playlists=playlists.find())

if __name__ == "__main__":
    app.run(debug=True)
    