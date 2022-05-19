from json import loads
import requests
from time import time
class spotifyMusicHandler:
    def __init__(self, API_key): 
        """Create handler for spotify api

        Args:
            API_key (string): API key for spoitfy
        """        
        self.current_track = {'track_id':'25FTMokYEbEWHEdss5JLZS'}
        self.get_from_search_options = ['albums', 'artists', 'episodes', 'genres', 'playlists', 'podcasts', 'tracks', 'users', 'multi']
        self.url = "https://spotify23.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Host": "spotify23.p.rapidapi.com",
            "X-RapidAPI-Key": API_key
        }
        return

    def getInfo(self, url, HTTPmethod, parameters):
        """A general function to connect to the spotify API

        Args:
            url (str): ending url of the spotify api target
            HTTPmethod (str): HTTP method to send to server 'GET' OR 'POST ETC.
            parameters (dict): Parameters to pass along to API

        Returns:
            dict: {results, duration}
        """            
        init_time = time()
        temp_url = str(self.url + url)
        response = requests.request(HTTPmethod, temp_url, headers=self.headers, params=parameters)
        duration = time() - init_time         
        return {'results':loads(response.text), 'duration': duration}

    def getTracks(self, tracksID):
        """Get tracks, can do multiple tracks if tracksID entered like id1,id2,id3

        Args:
            tracksID (str): ids of tracks data to be retrieved

        Returns:
            dict: returned data and duration
        """        
        if not isinstance(tracksID, str):
            return False
        tracksID = tracksID.replace(' ', '') #removes all white spaces
        return self.getInfo('/tracks/', 'GET', {"ids":tracksID})

    def get_track_credits(self, trackID):
        """Gets the track credits from the id

        Args:
            tracksID (str): single id for a song

        Returns:
            dict: Dictionary of results and duration
        """        
        if not isinstance(trackID, str):
            return False
        return self.getInfo('/track_credits/', 'GET', {"id":trackID})

    def get_track_lyrics(self, trackID):
        """Gets the track lyrics from the id

        Args:
            tracksID (str): single id for a song

        Returns:
            dict: Dictionary of results and duration
        """        
        if not isinstance(trackID, str):
            return False
        return self.getInfo('/track_lyrics/', 'GET', {"id":trackID})
    
    def get_all_track_data(self, trackID):
        """Get all available trackdata from the trackID

        Args:
            trackID (str): Specific and single trackID

        Returns:
            dict: dictionary of all results
        """        
        if not isinstance(trackID, str):
            return False
        init_time = time()
        track_data = self.getInfo('/tracks/', 'GET', {"ids":trackID} )
        track_credits = self.getInfo('/track_credits/', 'GET', {"id":trackID})
        track_lyrics = self.getInfo('/track_lyrics/', 'GET', {"id":trackID})
        track_data['results']['tracks'][0]['credits'] = track_credits['results']['credits']
        track_data['results']['tracks'][0]['lyrics'] = track_lyrics['results']['lyrics']
        track_data['duration'] = (time()-init_time)
        return track_data

    def get_from_search(self, query, query_type = "multi",offset = 0, limit = 20, num_top_results = 5):
        """Gets data from search query

        Args:
            query (str): Search value
            query_type (str, optional): query type. Options: albums, artists, episodes, genres, playlists, podcasts, tracks, users or multi. Defaults to "multi".
            offset (int, optional): position search starts in. Defaults to 0 (first result).
            limit (int, optional): limit of results. Defaults to 20.
            num_top_results (int, optional): Number of top results to show. Defaults to 5.

        Returns:
            dict: dict of results and duration 
        """                
        #convert query string to url friendly format
        if not isinstance(query, str):
            return False
        sanitised_query = query.strip() #removes all trailing white space
        if query_type not in self.get_from_search_options:
            query_type = 'multi'  #reverts to default option
        
        querystring = {"q":sanitised_query,"type":query_type,"offset":offset,"limit":limit,"numberOfTopResults":num_top_results}
        return self.getInfo('/search', 'GET', querystring)
    
    def get_from_search_with_preview(self, query, query_type = "multi",offset = 0, limit = 20, num_top_results = 5):
        """Gets data from search query

        Args:
            query (str): Search value
            query_type (str, optional): query type. Options: albums, artists, episodes, genres, playlists, podcasts, tracks, users or multi. Defaults to "multi".
            offset (int, optional): position search starts in. Defaults to 0 (first result).
            limit (int, optional): limit of results. Defaults to 20.
            num_top_results (int, optional): Number of top results to show. Defaults to 5.

        Returns:
            dict: dict of results and duration 
        """                
        if not isinstance(query, str):
            return False         #ensure query is string

        sanitised_query = query.strip() #removes all trailing white space
        if query_type not in self.get_from_search_options:
            query_type = 'multi' #ensure query_type is valid, or resort to 'multi'
        querystring = {"q":sanitised_query,"type":query_type,"offset":offset,"limit":limit,"numberOfTopResults":num_top_results}
        init_time = time()
        search_results = self.getInfo('/search/', 'GET', querystring)
        track_list = search_results['results']['tracks']['items']
        id_list = [] #creates blank list

        for item in track_list: #adds all id to a list
            id_list.append(item['data']['id'])
        ids_str = ','.join(id_list) #uses join to make a single string of ids
        tracks = self.getTracks(ids_str) #gets all track data
        tracks['duration'] = str(init_time - time()) #updates duration
        return tracks #returns the data

if __name__ == '__main__':    
    SPOTIFY = spotifyMusicHandler('badc7baeeamsh7de16dfafae2bf6p1b8019jsn3188359ba6cf')
    results = SPOTIFY.get_from_search_with_preview('hello', 'tracks')
