# Markov simulaton of covid cases
import json
import matplotlib.pylab as plt
import requests
import random
from math import cos, asin, sqrt
import csv
import numpy as np

ADOPTABILITY_INDEX  = 0.92
TIME_STEPS = 100  #days
SPREAD_INDEX = 0.05


week_shopping_probability = 0.23

def t(a,m):
    '''simply test the pareto dist'''
    X = (np.random.pareto(a, 2000) + 1) * m
    Y = (np.random.pareto(a, 2000) + 1) * m
    for x in range(len(X)):
        plt.plot(X[x],Y[x],'ko')



def getStats(county_name,debug=False):            
    '''if not in memory then queries the data'''
    
    with open('memory.json','r') as file:
        try: data = json.loads(file.read())
        except: data = json.loads('{}')

        try: return data[county_name]        
        except:
            if debug: return 'Not found, here it would search but debug=True'
            with open('memory.json','w+') as file:            
                template = 'https://api.wolframalpha.com/v2/query?input={}+county&format=image,plaintext&output=json&appid=HG29J8-V92PJXR62L'.format(county_name)
                print('Requesting: ',template)
                response = requests.get(template).json()                
                data[county_name] = response    
                file.write(json.dumps(data))
        
 
class county(object):
    def __init__(self,name,lat,lon,poly):
        def getPopulation(dict_list):
            for el in dict_list['queryresult']['pods']:
                try:
                    if el['title'] == 'Population':                    
                        el = el['subpods'][0]['plaintext']                    
                        number = [int(s) for s in el.split() if s.isdigit()][0]
                        return int(number)
                except:
                    return None
            return None
        def getArea(dict_list):
            for el in dict_list['queryresult']['pods']:
                try:
                    if el['title'] == 'Geographic properties':                    
                        el = el['subpods'][0]['plaintext']     
                        number = [int(s) for s in el.split() if s.isdigit()][0]
                        return int(number)
                except:
                    return None
            return None

        self.lat = lat
        self.lon = lon
        self.name = name
        self.polygon = poly
        self.stats = getStats(self.name)
        self.population = getPopulation(self.stats)
        self.area = getArea(self.stats)
        if self.area == None:print('Area not found in: '+self.name)
        else:self.area_in_gcs = self.area//111.3
#        self.agents = populate(self,self.stats['']) #returns a list of agent objects generated over the estimated probability of the place
        
#        self.stats = {"yadiya":"yado"}
    def __str__(self):
        try:ispoly = self.polygon != {}
        except:ispoly = False
        try:isstats = self.stats != {}
        except:isstats = False
        return 'Poly: {}, Stats:{} CENTER OF {} at lon,lat: {},{}'.format(ispoly,isstats,self.name,self.lat,self.lon)
    def __repr__(self):
        try:ispoly = self.polygon != {}
        except:ispoly = False
        try:isstats = self.stats != {}
        except:isstats = False
        return 'Poly: {}, Stats:{} CENTER OF {} at lon,lat: {},{}'.format(ispoly,isstats,self.name,self.lat,self.lon)

def generate_counties(show=False):
    '''returns a list of bin objects that describe the whole place'''
    
    def centroid(vertexes):
         _x_list = [vertex [0] for vertex in vertexes]
         _y_list = [vertex [1] for vertex in vertexes]
         _len = len(vertexes)
         _x = sum(_x_list) / _len
         _y = sum(_y_list) / _len
         return(_x, _y)
    def print_json(J):
        print(json.dumps(J,indent=2))

    with open('mn_plus_wn.json') as file:
    	sub = json.load(file)
    	for n in range(len(sub['features'])):
    
    			sub_at_n_geo = sub['features'][n]['geometry']['coordinates']
    			try:
    				sub_name = sub['features'][n]['properties']['MCD_NAME']
    			except:
    				sub_name = sub['features'][n]['properties']['Precinct']
    
    			try:
    				
    				poly_tuples = [tuple(x) for x in sub_at_n_geo[0]]
    				center_point = centroid(poly_tuples) #index zero because the list is empty
    				print(sub_name,type(sub_at_n_geo[0]))
    			except Exception as e:
    				print(sub_name,sub_at_n_geo[0],'            ------  Error  ------')
    				# pass
        
        
#    with open('MN_counties.geojson','r') as counties:
#        result = []
#        
#        counties = json.loads(counties.read())
#        # counties_polygon_list = counties['features'][0]['geometry']['coordinates']        
#        for n in range(len(counties['features'])):
#            county_at_n = counties['features'][n]['geometry']['coordinates']
#            county_name = counties['features'][n]['properties']['NAME']
#            poly_tuples = [tuple(x) for x in county_at_n[0]]
#            center_point = centroid(poly_tuples) #index zero because the list is empty
#            result.append(county(county_name,center_point[0],center_point[1],poly_tuples)) #takes name, lon and lan
            
    if show:
        for x in result:print(x,end='\n')
    return result

counties = generate_counties()


def populate(parent,population):
    for county in parent.counties:
        def calculate_closest(lat,lan):
            pass
        
        '''returns a list of agents'''
        total = []
        for x in range(population):            
            county_lat = county.lat
            county_lon = county.long
            
            local_agent = agent(parent)
            local_agent.closest = calculate_closest(county_lat,county_lon) #returns the 3 closest stores regardless of if they are t/w
            total.append(local_agent)            
        return total
            
def preprocess_files():
    csv_walmarts = open('walmarts.csv',newline='')
    csv_walmart = csv.DictReader(csv_walmarts)
    output_walmarts = open('walmarts_ourput.csv','w+',newline='')
    for row in csv_walmart:
        if row['state'] == 'MN':            
            writer = csv.DictWriter(output_walmarts,fieldnames = list(row))
            writer.writerow(row)            
            
    
    csv_targets = open('targets.csv',newline='')
    csv_target = csv.DictReader(csv_targets)
    output_targets = open('targets_ourput.csv','w+',newline='')
    for row in csv_target:
        if row['Address.Subdivision'] == 'MN':
            writer = csv.DictWriter(output_targets ,fieldnames = list(row))
            writer.writerow(row)            
            
    csv_walmarts.close()
    output_walmarts.close()
    csv_targets.close()
    output_targets.close()
    
preprocess_files()
    
def calculate_closest(lat,lan):
#    
#    def distance(lat1, lon1, lat2, lon2):
#        p = 0.017453292519943295
#        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
#        return 12742 * asin(sqrt(a))
#    
#    def closest(data, v):
#        return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))
#    
    csv_walmarts = open('walmarts.csv',newline='')
    csv_walmarts = csv.DictReader(csv_walmarts)
    output_walmarts = open('walmarts_ourput.csv','w+')
    for row in csv_walmarts:
        if row['state'] == 'MN':
            output_walmarts.write(row['state'])
            
    
    csv_targets = open('targets.csv',newline='')
    csv_targets = csv.DictReader(csv_targets)
    output_targets = open('targets_ourput.csv','w+')
    for row in csv_targets:
        if row['Address.Subdivision'] == 'MN':
            output_walmarts.write(row['Address.Subdivision'])
        
    
    print(csv_walmarts)
        
    
        
        
class environment(object):
    def __init__(self,name,lat,lon,root_probability_states):
        global ADOPTABILITY_INDEX 
        self.adoptability = ADOPTABILITY_INDEX + (ADOPTABILITY_INDEX*random.random()/20)
        self.name = name        
        

        self.counties = generate_counties() #returns a list of county objects
    def step(self):
        pass

class transition_node(object):
    def __init__(self,name,initial,secondary,spread = SPREAD_INDEX):
        self.name = name
        self.initial = initial #Probability of happening any day
        self.secondary = secondary  #Dict of subevent  
        self.spread = spread 


class store(transition_node):
    def __init__(self,lon,lat,name):
        super().__init__(self)
        self.longitude = lon
        self.latitude = lat

class state(object):
    def __init__(self):
        pass
        
class agent(object):
    def __init__(self,parent):
        self.parent = parent
        
        #has to be pareto
        self.lat = parent.lat + (parent.lat*random.random()/20)
        self.lon = parent.lon + (parent.lon*random.random()/20)
        
        self.closest = []
        self.state_list = []
    def __repr__(self):
        return 'Agent> Parent:'+self.parent+' State: '+self.state_list
    
    def genAction():
        '''randomly picks what's to be done this day'''        
        if random.random() > week_shopping_probability:
            pass
        
        
def simulate():
    for iteration in range(TIME_STEPS):
        pass
        
if __name__ == '__main__':
    simulate()