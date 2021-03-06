from json import loads
import requests
from time import time
class spotifyMusicHandler:
    def __init__(self, API_key): 
        """Create handler for spotify api

        Args:
            API_key (string): API key for spoitfy
        """        
        self.get_from_search_options = ['albums', 'artists', 'episodes', 'genres', 'playlists', 'podcasts', 'tracks', 'users', 'multi']
        self.url = "https://spotify23.p.rapidapi.com" #base url
        self.headers = { #creates headers param
            "X-RapidAPI-Host": "spotify23.p.rapidapi.com", 
            "X-RapidAPI-Key": API_key
        }
        return

    def get_info(self, url, HTTPmethod, parameters):
        """A general function to connect to the spotify API

        Args:
            url (str): ending url of the spotify api target
            HTTPmethod (str): HTTP method to send to server 'GET' OR 'POST ETC.
            parameters (dict): Parameters to pass along to API

        Returns:
            dict: {results, duration}
        """            
        init_time = time() #starts initial time
        response = requests.request(HTTPmethod, str(self.url + url), headers=self.headers, params=parameters)
        duration = time() - init_time #calculates the duration      
        return {'results':loads(response.text), 'duration': duration} #returns a dict of duration and results

    def get_tracks(self, tracksID):
        """Get tracks, can do multiple tracks if tracksID entered like id1,id2,id3

        Args:
            tracksID (str): ids of tracks data to be retrieved

        Returns:
            dict: returned data and duration
        """        
        if not isinstance(tracksID, str): #makes sure it is a string
            return False #otherwise exit function and say no results
        tracksID = tracksID.replace(' ', '') #removes all white spaces
        return self.get_info('/tracks/', 'GET', {"ids":tracksID}) #returns the dict generated by self.get_info()

    def get_track_credits(self, trackID):
        """Gets the track credits from the id

        Args:
            tracksID (str): single id for a song

        Returns:
            dict: Dictionary of results and duration
        """        
        if not isinstance(trackID, str): #same as get_tracks
            return False
        return self.get_info('/track_credits/', 'GET', {"id":trackID})

    def get_track_lyrics(self, trackID):
        """Gets the track lyrics from the id

        Args:
            tracksID (str): single id for a song

        Returns:
            dict: Dictionary of results and duration
        """        
        if not isinstance(trackID, str): #same as get_tracks
            return False
        return self.get_info('/track_lyrics/', 'GET', {"id":trackID})
    
    def get_all_track_data(self, trackID):
        """Get all available trackdata from the trackID

        Args:
            trackID (str): Specific and single trackID

        Returns:
            dict: dictionary of all results
        """        
        if not isinstance(trackID, str): #ensures trackID is string
            return False #otherwise return no data
        init_time = time() #create start time
        track_data = self.get_info('/tracks/', 'GET', {"ids":trackID} ) #generate basic track data
        track_credits = self.get_info('/track_credits/', 'GET', {"id":trackID}) #generate track credits
        track_lyrics = self.get_info('/track_lyrics/', 'GET', {"id":trackID}) #generates track lyrics
        track_data['results']['tracks'][0]['credits'] = track_credits['results']['credits'] #inserts data into main dict
        track_data['results']['tracks'][0]['lyrics'] = track_lyrics['results']['lyrics'] #inserts data into main dict
        track_data['duration'] = (time()-init_time) #updates duration
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
        return self.get_info('/search', 'GET', querystring)
    
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
        init_time = time()
        track_list = self.get_from_search(query_type, query_type, offset, limit,num_top_results)['results']['tracks']['items']
        id_list = [] #creates blank list

        for item in track_list: #adds all id to a list
            id_list.append(item['data']['id'])
        ids_str = ','.join(id_list) #uses join to make a single string of ids
        tracks = self.get_tracks(ids_str) #gets all track data
        tracks['duration'] = str(init_time - time()) #updates duration
        return tracks #returns the data

if __name__ == '__main__':    
    SPOTIFY = spotifyMusicHandler('badc7baeeamsh7de16dfafae2bf6p1b8019jsn3188359ba6cf')
    results = SPOTIFY.get_from_search_with_preview('hello', 'tracks')
