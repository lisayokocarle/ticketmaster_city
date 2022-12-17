###API function

###importing necessary packages
import requests
import pandas as pd


def apiget(password, city, keyword = ""):
        """
        This function pulls a get request to TicketMaster, and returns
        information about concerts and music events in a city.

        Parameters
        ----------
        password: string
            Personal TicketMaster API key
        ***kwargs: key, value string argument
            Any of the parameters that user is interested in seeing

        Returns
        -------
        pandas.dataframe
            A dataframe containing information about music events happening
            in specific city

        Examples
        --------
        >>> from lisas_little_package import apiget
        >>> apiget(city = "New York", password = "API_KEY")
        returns dataframe
        """

        url = 'https://app.ticketmaster.com/discovery/v2/events.json?city={c}&keyword={kw}&classificationName=music&apikey={api}'
        r= requests.get(url.format(c = city, kw = keyword, api=password))
        
        assert r.status_code == 200, "Uh oh, there was an issue with the server. Please doublecheck your input."
        test_json=r.json()
        try:
                objectids= test_json['_embedded']
                return pd.DataFrame(objectids['events'])
        except KeyError:
                print("No concerts with those parameters!")
                
        
    

###Created class
class City():
    """
        Holds all of the data pulled from the TicketMaster API for
        specified city. This way user only needs to type in city name once,
        and can see all the information TicketMaster API has to offer about
        that city.

        Attributes:
            genre(): Dictionary of all the genres of music being performed
                and count of each.
            subgenre(): Dictionary of all the subgenres of music being performed
                and count of each.
            events(): Dictionary of events and event ID happening in city.
            """
    def __init__(self, cityname="", password=""):
        """Inits City with city name, and dataframe saved from API get request"""
        if type(cityname)!= str:
            raise ValueError('Please only input string for city name.')
        if cityname == "":
            raise ValueError('Please input a city name')
        if password == "":
            raise ValueError('Please input API Key')
        self.city_name = cityname
        self.password = password
        self.df = apiget(city = self.city_name, password = self.password)
        
    def __str__(self):
        """This function is what the City() class will actually return when it is
        called on its own."""
        return self.city_name
    
    def genres(self):
        """This returns a dictionary of the genres of concerts happening in city,
            and their counts"""
    
        df1 = (self.df['classifications'])
        genre_list = []
        
        for rows in df1:
            for x in rows:
                genre_list.append(x['genre'])
        
        genredf = pd.DataFrame(genre_list)
        
        genre_dic = {}
        for key in genredf['name']:
            if key in genre_dic:
                genre_dic[key]+=1
            else:
                genre_dic[key]=1
        return genre_dic

    
    def subgenres(self):
        """This returns a dictionary of the subgenres of concerts happening in city,
            and how many of each"""
        df2 = self.df['classifications']
        subgenre_list = []
        
        for rows in df2:
            for x in rows:
                subgenre_list.append(x['subGenre'])
        
        subgenredf = pd.DataFrame(subgenre_list)
            
        subgenre_dic = {}
        for key in subgenredf['name']:
            if key in subgenre_dic:
                subgenre_dic[key]+= 1
            else:
                subgenre_dic[key]= 1
        return subgenre_dic
    
    def events(self):
        """This returns a dictionary of events happening in city, and their
        event ID"""
        event_dict = dict(zip(self.df.name, self.df.id))
        return event_dict
