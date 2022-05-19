import http.client
from json import loads
import requests

class spotifyMusicHandler:
    def __init__(self, API_key): 
        """Create handler for spotify api

        Args:
            API_key (string): API key for spoitfy
        """        
        self.current_track = {'track_id':'25FTMokYEbEWHEdss5JLZS'}
        self.get_from_search_options = ['albums', 'artists', 'episodes', 'genres', 'playlists', 'podcasts', 'tracks', 'users', 'multi']
        self.url = "https://spotify23.p.rapidapi.com/search/"
        self.headers = {
            "X-RapidAPI-Host": "spotify23.p.rapidapi.com",
            "X-RapidAPI-Key": API_key
        }
        
        return
    def get_current_track(self, track = None):
        if self.current_track == None:
            return False
        if track == None:
            track = self.current_track
        else:
            querystring = {"ids":self.track}
            requests.request("GET", self.url, headers=self.headers, params=querystring)
            response = self.connection.getresponse()
            data = response.read()
            
            print(data.decode("utf-8"))
            return loads(data.decode("utf-8"))
    
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
        querystring = {"q":final_query,"type":query_type,"offset":offset,"limit":limit,"numberOfTopResults":num_top_results}

        response = requests.request("GET", self.url, headers=self.headers, params=querystring)
        data = response.text
                
        return loads(data.decode("utf-8"))

if __name__ == '__main__':
    SPOTIFY = spotifyMusicHandler('badc7baeeamsh7de16dfafae2bf6p1b8019jsn3188359ba6cf')