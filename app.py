from flask import Flask, render_template, session, request, redirect, jsonify, flash, url_for, Response, logging
from interfaces.spotify_interface import spotifyMusicHandler
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Here we do some funky stuff, and change the session'

tracks = {"tracks":[{"album":{"album_type":"album","artists":[{"external_urls":{"spotify":"https:\/\/open.spotify.com\/artist\/4mYFgEjpQT4IKOrjOUKyXu"},"id":"4mYFgEjpQT4IKOrjOUKyXu","name":"Wheatus","type":"artist","uri":"spotify:artist:4mYFgEjpQT4IKOrjOUKyXu"}],"external_urls":{"spotify":"https:\/\/open.spotify.com\/album\/3xmKWmqJFoXS22tePO3mgd"},"id":"3xmKWmqJFoXS22tePO3mgd","images":[{"height":640,"url":"https:\/\/i.scdn.co\/image\/ab67616d0000b2730a3740efa638f10f14fabc46","width":640},{"height":300,"url":"https:\/\/i.scdn.co\/image\/ab67616d00001e020a3740efa638f10f14fabc46","width":300},{"height":64,"url":"https:\/\/i.scdn.co\/image\/ab67616d000048510a3740efa638f10f14fabc46","width":64}],"name":"Wheatus","release_date":"1999-02-15","release_date_precision":"day","total_tracks":10,"type":"album","uri":"spotify:album:3xmKWmqJFoXS22tePO3mgd"},"artists":[{"external_urls":{"spotify":"https:\/\/open.spotify.com\/artist\/4mYFgEjpQT4IKOrjOUKyXu"},"id":"4mYFgEjpQT4IKOrjOUKyXu","name":"Wheatus","type":"artist","uri":"spotify:artist:4mYFgEjpQT4IKOrjOUKyXu"}],"disc_number":1,"duration_ms":241666,"explicit":True,"external_ids":{"isrc":"USSM10008431"},"external_urls":{"spotify":"https:\/\/open.spotify.com\/track\/25FTMokYEbEWHEdss5JLZS"},"id":"25FTMokYEbEWHEdss5JLZS","is_local":False,"is_playable":True,"name":"Teenage Dirtbag","popularity":69,"preview_url":"https:\/\/p.scdn.co\/mp3-preview\/c3d5cf3ff922ca2e2cb6f27c60ff88ba47580a59?cid=f6a40776580943a7bc5173125a1e8832","track_number":3,"type":"track","uri":"spotify:track:25FTMokYEbEWHEdss5JLZS"}]}
image = "https://i.scdn.co/image/ab67616d0000b2730a3740efa638f10f14fabc46"
SPOTIFY_API_KEY = 'badc7baeeamsh7de16dfafae2bf6p1b8019jsn3188359ba6cf'
SPOTIFY = spotifyMusicHandler(SPOTIFY_API_KEY)

@app.route('/')
def home():
    
    #SPOTIFY.get_from_search('Vivaldis Winter', 'multi')
    #SPOTIFY.get_current_track()
    return render_template('homepage.html')

@app.route('/search-results', methods = ['GET', 'POST'])
def search_results():
    if request.method != 'POST':
        return redirect('/')
    query = request.form.get('query')
    results = SPOTIFY.get_from_search(query, 'tracks')
    return jsonify(results)


@app.route('/get-song', methods = ['GET', 'POST'])
def get_song():
    if request.method != 'POST':
        return redirect('/')
    track_id = request.form.get('track_id')
    SPOTIFY.current_track['track_id'] = track_id
    results = SPOTIFY.get_current_track()
    print(results)
    return jsonify(results)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True) #runs a local server on port 5000