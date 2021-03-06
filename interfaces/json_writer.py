import json #imports json library
class JSONHelper(): #creates an object
    def __init__(self, filename): #each object is a file
        self.filename = filename #saves the filename
        with open(self.filename) as self.json_file: #opens the file as self.json_file
            self.json_data = json.load(self.json_file) #converts the data to dictionary
        return

    def reload_data(self): #gets the new data
        with open(self.filename) as self.json_file: #same process as __init__()
            self.json_data = json.load(self.json_file)
        return self.json_data #returns the new data
    
    def write_data(self, data): #update JSON data
        json_string = json.dumps(data) #converts to string
        with open(self.filename, 'w') as f:
            f.write(json_string) #writes the provided data to file

#usage