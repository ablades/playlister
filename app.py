from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
#Points to mongo daemon URI if it exisits
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Playlister')
#Creates Mongo Client that connects to default host
client = MongoClient(host=host)
#Gets the database from client called Playlister (creates it if it doesnt exist)
db = client.get_default_database()
#Retrieves the collection(group of documents)
playlists = db.playlists
#comments collection added to database
comments = db.comments

app = Flask(__name__)

#Show all playlist
@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', playlists=playlists.find())

#Gets the post request from the form routed to /playlists
#Redirects
@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    #Creates new playlist dictionary object from form
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos' : request.form.get('videos').split(),
        'rating' : request.form.get('rating')
    }

    #inserts into playlists and stores the new id in playlist_id
    playlist_id = playlists.insert_one(playlist).inserted_id
    #returns url given by playlistshow function with playlist_id parameter
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

#Create new playlist
@app.route('/playlists/new')
def playlists_new():
    """Create a new playlist."""
    return render_template('playlists_new.html', playlist={}, title='New Playlist')

#Route to single playlist. Playlist_id is added to route
@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)

#Edit playlist
@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """Show the edit form for a playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist)

@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split(),
        'rating': request.form.get('rating')
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

#Deletes the object from the playlist and then redirects the user to playlist index
@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """Delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))

#Handles comments
@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'playlist_id': ObjectId(request.form.get('playlist_id')),
        'rating': request.form.get('rating')
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))

if __name__ == "__main__":
    #Change port to allow running on heroku
     app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
    