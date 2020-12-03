# Markov simulaton of covid cases
import json
import fiona
import topojson as tp



ADOPTABILITY_INDEX  = 0.92
TIME_STEPS = 100 #days
SPREAD_INDEX = 0.1


class county(object):
    def __init__(self,name,lat,lon,poly):
        self.lat = lat
        self.long = lon
        self.name = name
        self.polygon = poly
    def __str__(self):
        return 'Center of {} at lon,lat: {},{}'.format(self.name,self.lat,self.long)
    def __repr__(self):
        return 'Center of {} at lon,lat: {},{}'.format(self.name,self.lat,self.long)

def generate_counties(show=False):
    def centroid(vertexes):
         _x_list = [vertex [0] for vertex in vertexes]
         _y_list = [vertex [1] for vertex in vertexes]
         _len = len(vertexes)
         _x = sum(_x_list) / _len
         _y = sum(_y_list) / _len
         return(_x, _y)
    def print_json(J):
        print(json.dumps(J,indent=2))
    with open('MN_counties.geojson','r') as counties:
        result = []
        
        counties = json.loads(counties.read())
        # counties_polygon_list = counties['features'][0]['geometry']['coordinates']        
        for n in range(len(counties['features'])):
            county_at_n = counties['features'][n]['geometry']['coordinates']
            county_name = counties['features'][n]['properties']['NAME']
            poly_tuples = [tuple(x) for x in county_at_n[0]]
            center_point = centroid(poly_tuples) #index zero because the list is empty
            result.append(county(county_name,center_point[0],center_point[1],poly_tuples)) #takes name, lon and lan
            
    if show:
        for x in result:print(x,end='\n')
    return result

generate_counties(show=True)


        
class city(object):

    def __init__(self,name,lat,lon,age_density,profession_density):
        global ADOPTABILITY_INDEX 
        self.adoptability = ADOPTABILITY_INDEX 
        self.name = name        
        self.age_density  = age_density  
        self.profession_density = profession_density

        self.counties = center_counties() #returns a list of center objects
    def populate(self):
        pass
    def step(self):
        pass

class transition_node(object):
    def __init__(self,name,initial,secondary,spread = SPREAD_INDEX):
        self.name = name
        self.initial = initial
        self.secondary = secondary
        self.spread = spread

class location(transition_node):
    def __init__(self,lon,lat,name):
        super().__init__(self)
        self.longitude = lon
        self.latitude = lat

        
class agent(object):
    def __init__(self,parent):
        self.parent = parent
        self.state = []
        
        
        
def simulate():
    for iteration in range(TIME_STEPS):
        pass
        
if __name__ == '__main__':
    simulate()