import http.client
from json import loads
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
        
        self.connection.request("GET", f"/search/?q={final_query}&type={query_type}&offset={offset}&limit={limit}&numberOfTopResults={num_top_results}", headers=self.headers)  
        response = self.connection.getresponse()
        data = response.read()
        
        return loads(data.decode("utf-8"))