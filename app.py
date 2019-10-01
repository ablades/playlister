from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

#Creates Mongo Client that connects to default host
client = MongoClient()
#Gets the database from client called Playlister (creates it if it doesnt exist)
db = client.Playlister
#Retrieves the collection(group of documents)
playlists = db.playlists

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
    return render_template('playlists_show.html',playlist=playlist)

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
        'videos': request.form.get('videos').split()
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

if __name__ == "__main__":
    app.run(debug=True)
    