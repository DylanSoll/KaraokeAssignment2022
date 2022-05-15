from flask import Flask, render_template, url_for
import http.client
import re
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Here we do some funky stuff, and change the session'

tracks = {"tracks":[{"album":{"album_type":"album","artists":[{"external_urls":{"spotify":"https:\/\/open.spotify.com\/artist\/4mYFgEjpQT4IKOrjOUKyXu"},"id":"4mYFgEjpQT4IKOrjOUKyXu","name":"Wheatus","type":"artist","uri":"spotify:artist:4mYFgEjpQT4IKOrjOUKyXu"}],"external_urls":{"spotify":"https:\/\/open.spotify.com\/album\/3xmKWmqJFoXS22tePO3mgd"},"id":"3xmKWmqJFoXS22tePO3mgd","images":[{"height":640,"url":"https:\/\/i.scdn.co\/image\/ab67616d0000b2730a3740efa638f10f14fabc46","width":640},{"height":300,"url":"https:\/\/i.scdn.co\/image\/ab67616d00001e020a3740efa638f10f14fabc46","width":300},{"height":64,"url":"https:\/\/i.scdn.co\/image\/ab67616d000048510a3740efa638f10f14fabc46","width":64}],"name":"Wheatus","release_date":"1999-02-15","release_date_precision":"day","total_tracks":10,"type":"album","uri":"spotify:album:3xmKWmqJFoXS22tePO3mgd"},"artists":[{"external_urls":{"spotify":"https:\/\/open.spotify.com\/artist\/4mYFgEjpQT4IKOrjOUKyXu"},"id":"4mYFgEjpQT4IKOrjOUKyXu","name":"Wheatus","type":"artist","uri":"spotify:artist:4mYFgEjpQT4IKOrjOUKyXu"}],"disc_number":1,"duration_ms":241666,"explicit":True,"external_ids":{"isrc":"USSM10008431"},"external_urls":{"spotify":"https:\/\/open.spotify.com\/track\/25FTMokYEbEWHEdss5JLZS"},"id":"25FTMokYEbEWHEdss5JLZS","is_local":False,"is_playable":True,"name":"Teenage Dirtbag","popularity":69,"preview_url":"https:\/\/p.scdn.co\/mp3-preview\/c3d5cf3ff922ca2e2cb6f27c60ff88ba47580a59?cid=f6a40776580943a7bc5173125a1e8832","track_number":3,"type":"track","uri":"spotify:track:25FTMokYEbEWHEdss5JLZS"}]}

class spotifyMusicHandler:
    def __init__(self, API_key): 
        """Create handler for spotify api

        Args:
            API_key (string): API key for spoitfy
        """        
        self.current_track = {'track_id':'25FTMokYEbEWHEdss5JLZS'}
        self.get_from_search_options = ['albums', 'artists', 'episodes', 'genres', 'playlists', 'podcasts', 'tracks', 'users', 'multi']
        self.connection = http.client.HTTPSConnection("spotify23.p.rapidapi.com")
        self.headers = {
            'X-RapidAPI-Host': "spotify23.p.rapidapi.com",
            'X-RapidAPI-Key': API_key
            }
        
        return
    def get_current_track(self):
        if self.current_track == None:
            return False
        else:
            self.connection.request("GET", f"/tracks/?ids={self.current_track['track_id']}", headers=self.headers)
            response = self.connection.getresponse()
            data = response.read()
            
            print(data.decode("utf-8"))
            return data.decode("utf-8")
    
    def get_from_search(self, query, query_type = "multi",offset = 0, limit = 20, num_top_results = 5):
        """get details from string query

        Args:
            query (str): Search value
            query_type (str, optional): query type. Options: albums, artists, episodes, genres, playlists, podcasts, tracks, users or multi. Defaults to "multi".
            offset (int, optional): position search starts in. Defaults to 0 (first result).
            limit (int, optional): limit of results. Defaults to 20.
            num_top_results (int, optional): Number of top results to show. Defaults to 5.
        """        
        #convert query string to url friendly format
        sanitised_query = query.strip()
        final_query = sanitised_query.replace(" ", "%20")
        #ensures correct query type
        if query_type not in self.get_from_search_options:
            query_type = 'multi' 
        #checks to see if any non-digits are in limit
        
        print(final_query)
        self.connection.request("GET", f"/search/?q={final_query}&type={query_type}&offset={offset}&limit={limit}&numberOfTopResults={num_top_results}", headers=self.headers)  
        response = self.connection.getresponse()
        data = response.read()
        
        print(data.decode("utf-8"))
        return

@app.route('/')
def home():
    SPOTIFY = spotifyMusicHandler('badc7baeeamsh7de16dfafae2bf6p1b8019jsn3188359ba6cf')
    #SPOTIFY.get_from_search('Teenage Dirtbag', 'tracks')
    SPOTIFY.get_current_track()
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True) #runs a local server on port 5000