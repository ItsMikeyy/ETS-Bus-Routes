import pickle
from graphics import *
import sys
from math import radians, sin, cos, sqrt, asin

def main():
    '''
    Asks user for menu option and error checks to see if choice is allowed
    Parameters : None
    Returns : None
    '''
    has_quit = False
    shape_ids = {}
    shapes = {}
    stops = {}

    while has_quit == False:
        print("Edmonton Transit System\t")
        print("--------------------------------")
        print("(1) Load shape IDs from GTFS file")
        print("(2) Load shapes from GTFS file")
        print("(3) Load stops from GTFS file")
        print()
        print("(4) Print shape IDs for a route")
        print("(5) Print points for a shape ID")
        print("(6) Print stops for a location")
        print()
        print("(7) Save shapes, shape IDs, and stops in a pickle")
        print("(8) Load shapes, shape IDs, and stops from a pickle")
        print()
        print("(9) Display interactive map")
        print()
        print("(0) Quit")
        user_choice = get_choice()
        if(user_choice == 1):
            shape_ids = load_trips(shape_ids)
        elif(user_choice == 2):
            shapes = load_shapes(shapes)
        elif(user_choice == 3):
            stops = load_stops(stops)
        elif(user_choice == 4):
            find_shapes(shape_ids)
        elif(user_choice == 5):
            find_points(shapes)
        elif(user_choice == 6):
            find_stops(stops)
        elif(user_choice == 7):
            save_to_pickle(shapes, shape_ids, stops)
        elif(user_choice == 8):
            #Makes sure the return value has the tuple and if so
            #split them into the three dictionaries otherwise return
            #if false pass
            structs = load_from_pickle(shapes, shape_ids, stops)
            if (structs != None):
                shape_ids = structs[0]
                shapes = structs[1]
                stops = structs[2]
        elif (user_choice == 9):
            load_map(shape_ids, shapes, stops)

        elif(user_choice == 0):
            has_quit = True
               
def load_trips(ids):
    '''
   Loads the file if the correct file is loaded and extracts the data
   into a ditionary with the key being the route_id and the shape_ids being a list   
   Parameters ids: Dict
   Returns ids: Dict
    '''   
    try:
        file_name = input("Enter a file name [data/trips.txt]:")
        if(file_name == ""):
            file = open("data/trips.txt")
        else:
            file = open(file_name)            
    except:
       print("File not found")
       return
    #create list and loop through file
    values = []
    for line in file.readlines():
        line = line.replace("\n", "")
        sep_data = line.split(",")
        if(sep_data[0] not in ids.keys()):
            values = []
            values.append(sep_data[6])
        elif sep_data[0] in ids.keys() and sep_data[6] not in values:
            values.append(sep_data[6])
        ids[sep_data[0]] = values
    ids.pop("route_id")
    return ids

def load_shapes(shape):  
    '''
    Loads the file if the correct file is loaded and extracts the data
    into a ditionary with the key being the shape_id and the cords being a list in a list  
    Parameters shape: Dict
    Returns shape: Dict
    '''
    try:
        file_name = input("Enter a file name [data/shapes.txt]:")
        if(file_name == ""):
            file = open("data/shapes.txt")
        else:
            file = open(file_name)            
    except:
        print("File not found")
        return
    shape_list = []  
    for line in file.readlines():
        line = line.replace("\n", "")
        sep_data = line.split(",")
        cord_list = []
        if(sep_data[0] not in shape):
            shape_list = []
            cord_list = []
            cord_list.append(sep_data[1])
            cord_list.append(sep_data[2])
            shape_list.append(cord_list)
        elif(sep_data[0] in shape):
            cord_list.append(sep_data[1])
            cord_list.append(sep_data[2])
            shape_list.append(cord_list)
        shape[sep_data[0]] = shape_list
    shape.pop("shape_id")
    return shape

def load_stops(stops):
    '''
    Loads the file if the correct file is loaded and extracts the data
    into a ditionary with the key being a tupple of coordinates and the bus stop id and name being the value  
    Parameters stops: Dict
    Returns stops: Dict
    '''
    try:
        file_name = input("Enter a file name [data/stops.txt]:")
        if(file_name == ""):
            file = open("data/stops.txt")
        else:
            file = open(file_name)            
    except:
       print("File not found")
       return
    for line in file.readlines():
        line = line.replace("\n", "")
        sep_data = line.split(",")
        sep_data
        cords = (sep_data[4].strip(), sep_data[5])
        value_string = sep_data[0] + " "*4 + sep_data[2]
        value_string = value_string.replace('"', "")
        stops[cords] = value_string
    stops.pop(("stop_lat", "stop_lon"))
    return stops

def find_shapes(ids):
    '''
    This Program asks for a user input and displays the 
    the shape_ids of the route
    Parameters ids: Dict
    returns None 
    '''
    correct_choice = False
    while correct_choice == False:
        user_input = input("Route ? ")
        if(user_input in ids.keys()):
            print("Shape IDs for", user_input + ":")
            for value in range(len(ids[user_input])):
                print("\t" + ids[user_input][value])
            return
        else:
            print("Shape IDs for", user_input + ":")
            print("** NOT FOUND **")
            return

def find_points(shape):
    '''
    This Program asks for a user input and displays the 
    the cords of the shape_id
    Parameters shape: dict
    returns None  
    '''
    correct_choice = False
    while correct_choice == False:
        user_input = input("Shape ID? ")
        if(user_input in shape.keys()):
            #correct_choice = True
            print("Shape for ", user_input + ":")
            for shape_value in range(len(shape[user_input])):
                for cord_value in range(len(shape[user_input][shape_value]) - 1):
                    print("(" + shape[user_input][shape_value][cord_value] + "," + shape[user_input][shape_value][cord_value + 1] + ")")
            return
        else:
            print(f"Shape for {user_input}:")
            print("** NOT FOUND **")
            return

def find_stops(stops):
    '''
    Allows the user to input coordinates (with or without brackets)
    and displays the stop id and name. If coordinate is not found returns back to main
    and says no stop found

    parameters: stops Dict
    Returns None
    '''
    #Formating spaces and brackets, decimals and splits the two values into a tuple
    #so it can search for the tuple key in stops dict
    user_input = input("Location as 'lat,lon'? ")
    org_string = user_input
    user_input = user_input.replace(" ", "")
    if(user_input[0] == "(" and user_input[-1] != ""):
        user_input = user_input.replace("(", "")
        user_input = user_input.replace(")", "")
        tmp_list = user_input.split(",")    
    else:
        tmp_list = user_input.split(",")
        cords = tmp_list[0], tmp_list[1]
    if "." not in user_input:
        org_string = ""
        for i in range(len(tmp_list)):
            if "." not in tmp_list[i]:
                tmp_list[i] = tmp_list[i] + ".0"
                org_string += tmp_list[i]
            if i == 0:
                org_string += ", "
         
    cords = tmp_list[0], tmp_list[1]
    if(org_string[0] == "(" and org_string[-1] != ""):
        org_string = org_string.replace("(", "")
        org_string = org_string.replace(")", "")
    #Looks for the bus stop
    if(cords in stops.keys()):
        for key in stops.keys():
            if cords == key:
                print("Stops for (" + org_string + "):")
                print(stops[key])
    else:
        print("Stops for (" + org_string + "):")
        print("** NOT FOUND **")
    return
        
def get_choice():
    '''
    To make sure a user only inputs a number 1 2,4,5, 0
    and ask them to fix their answer if they enterd the wrong
    thing
    '''
    choice_accepted = False
    accepted_numbers = ["1","2","3","4","5","6","7","8","9","0"]
    
    user_input = input("Enter command: ")
    if(user_input in accepted_numbers):
        choice_accepted = True
    else:
        while choice_accepted == False:
            user_input = input("Enter a valid number: ")
            if(user_input in accepted_numbers):
                choice_accepted = True            
            
    return int(user_input)

def save_to_pickle(shape_ids, shapes, stops):
    '''
    This function trys to create a file in "wb" mode where it will dump shapes, shape_ids and stops
    dictionaries to save time from loading from the other files if it fails
    it returns to main

    Parameters: shapes_ids, shapes, stops
    Returns: None
    '''
    try:
       file_name = input("Enter a file name [etsdata.p]:")
       if(file_name == ""):
           file = open("etsdata.p", "wb")
       else:
           file = open(file_name, "wb")            
    except:
       print("File not found")
       return
    pickle.dump((shapes, shape_ids, stops), file)
    file.close()

def load_from_pickle(shape_ids, shapes, stops):
    '''
    This function trys to load the pickled file in "rb" mode and assign the temporary tuple value to a 
    variable called data which is returned if it fails to load the file it returns none and 
    goes back to main

    Parameters: shapes_ids, shapes, stops
    Returns: None if failed to create the file if sucessful returns data (tuple)
    '''
    try:
       file_name = input("Enter a file name [etsdata.p]:")
       if(file_name == ""):
           file = open("etsdata.p", "rb")
       else:
           file = open(file_name, "rb")            
    except:
       print("File not found")
       return None
    data = pickle.load(file)
    return data

def load_map(shape_ids, shapes, stops):
    '''
    This function creates the windo and calls other helper functions to draw things to this windo
    It also sets the coordinates for the window

    Parameters: shapes_ids, shapes
    Returns: None
    '''
    win = GraphWin("City",630,768)
    win.setCoords(-113.7136, 53.39576, -113.2714, 53.71605)
    bg_loaded = draw_bg(win)
    if bg_loaded == False:
        win.close()
        return
    draw_btn(win)
    entry_box = draw_input_box(win)
    #Check if the user clicked in the window if user clicks the x then it simply returns to main
    while True: 
        try:
            point_mouse = win.getMouse()    
            sys.stdin.flush()  
        except:
            win.close()
            return
        btn_clicked, route_num = check_button(entry_box, point_mouse, win)
        #Checks if check_button returned true
        if (btn_clicked == False):
            print_cords(point_mouse, win)
            get_stop_distances(stops, point_mouse, win)
        else:
            path, value_found = get_route_info(route_num, shape_ids, shapes)
            #if the function returned true use value_found in the next function 
            #else pass
            if value_found == True:
                draw_route(path, shapes, win)

def print_cords(point, wind):
    '''
    prints the location of where the user clicks on the screen in both Geographic and Pixel
    coordinates
    
    Parametres: point Point, wind Window
    Returns none
    '''
    x = point.getX()
    y = point.getY()
    print(f"Geographic: (lat, lon): ({y}, {x})")
    x, y = wind.toScreen(x,y)
    print(f"Pixel (x, y): ({x}, {y})")

def get_stop_distances(stops, point, wind):
    '''
    takes in the users click and calculates and displays the distance between the click 
    and the bus stops. Shows the 5 closest stops to the click
    
    Parametres: point Point, wind Window, Stops dict
    Returns none
    '''
    #Initialize dictionary which will keep track of bus stop locations and 
    #distances between them and the click
    dist_dict = {}

    #Loops through every bus stop and calls the haversine algorithm to calculate the distances
    for item in stops.keys():
        #getting points one and two to be used in harversine
        pt1y = point.getX()
        pt1x = point.getY()

        pt2x = float(item[0])
        pt2y = float(item[1])
        #Converts distance to meters
        dist = haversine(pt1x, pt1y, pt2x, pt2y) * 1000
        dist = round(dist, 1)
        #Adds values to dict key being a tuple of the bus stop cords and value being distance from click 
        dist_dict[item] = dist
    #Functions that sort and show the bus stops 
    locations = sort_dists(dist_dict)
    print_stops(locations, dist_dict, stops)
    draw_stops(wind, dist_dict, locations)

def draw_stops(wind, dist_dict, locations):
    '''
    Loops through all key value pairs for each value in the 5 shortest locations
    list and draws circles at the coordinates of the bus stop

    Parameters: wind Window, dist_dict dict, locations list
    Returns: None
    '''
    for key in dist_dict.keys():
        for i in range(len(locations)):
            if dist_dict[key] == locations[i]:
                stop_location = Circle(Point(float(key[1]), float(key[0])), 0.001)
                stop_location.setFill(color_rgb(255,0,0))
                stop_location.draw(wind)

def check_button(entry, point, wind):
    '''
    Takes the users click location converts to pixels and checks if its in the range of the 
    button if it is grab the text thats in the entry box and returns
    
    Parametres: entry Entrybox, point Point, wind Window
    Returns if true: True, route_num (int)
            if false: False, None
    '''
    x = point.getX()
    y = point.getY()
    x,y = wind.toScreen(x,y)
    route_num = entry.getText()
    if x <= 70 and x >= 20 and y >= 20 and y <= 40:
        return True, route_num
    else:
        return False, None

def get_route_info(route_num, shape_ids, shapes):
    '''
    Checks if the given route_number is a valid number if so loops through all the shape_ids and find which one has 
    the most coordinates saves it as final_path and retruns it
    
    Parametres: route_num, shape_ids, shapes
    Returns: if true: final_path (string), True
            if false: None, False 
    '''
    if route_num in shape_ids.keys():
        #saves the largest path lenght
        path_length = 0
        for value in range(len(shape_ids[route_num])):
            #saves the current shape_id
            current_path = shape_ids[route_num][value]
            if len(shapes[current_path]) > path_length: 
                path_length = len(shapes[current_path])
                final_path = shape_ids[route_num][value]
        return final_path, True
    else:
        return None, False

def draw_route(path, shapes, wind):
    ''''
    Draws the path of the bus route by looping through every bus stop coordinate

    Parameters: path string, shapes dict, wind Window
    Returns: none
    '''
    for i in range (len(shapes[path]) - 1):
        line = Line(Point(float(shapes[path][i][1]), float(shapes[path][i][0])), Point(float(shapes[path][i + 1][1]), float(shapes[path][i + 1][0])))
        line.setWidth(3)
        line.draw(wind)

def draw_bg(wind):
    '''
    Takes the screen size and divides it by 2 and converts the current coordinates
    (Lat, Lon) to pixels then draws it to the screen
    
    Parametres: wind Window
    Returns none
    '''
    x1, y1 = wind.toWorld(630/2, 768/2)
    try:
        bg = Image(Point(x1,y1),"citymap.gif")
    except:
        return False
    bg.draw(wind)

def draw_btn(wind):
    '''
    Takes two points and a text and converts their location to pixels
    Then draws it to the screen
    
    Parametres: wind Window
    Returns none
    '''
    x1, y1 = wind.toWorld(20,20)
    x2, y2 = wind.toWorld(70,40) 
    rect = Rectangle(Point(x1,y1), Point(x2,y2))
    rect.setFill(color_rgb(0,50,250))
    rect.draw(wind)
    x1, y1 = wind.toWorld(45,30)
    txt = Text(Point(x1,y1), "Plot")
    txt.draw(wind)
  
def draw_input_box(wind):
    '''
    Takes a point to conver to pixels then draws the input box to screen
    
    
    Parametres: wind Window
    Returns entrybox object to get its value in a later function
    '''
    x1, y1 = wind.toWorld(130,30)
    entry = Entry(Point(x1,y1), 8)
    entry.draw(wind)
    return entry

#CITED FROM https://rosettacode.org/wiki/Haversine_formula#Python
def haversine(lat1, lon1, lat2, lon2):
    '''
    Takes two points (4 paramterts being the x and y location of both points) one being the position of the mouse click the other being the bus stop positions
    and calculates the distance between them in kilometers

    Parameters: lat1, lon1, lat2, lon2: all floats
    Returns: float
    '''
    R = 6372.8  # Earth radius in kilometers
 
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
 
    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))
 
    return R * c    

def sort_dists(dist_dict):
    '''
    put the distances from the dist_dict into a list then calls .sort() and grabs the first five lowest values
    and appends them to a new list
    
    Parameters: dist_dict dict
    Returns five_dists list
    '''
    distances = list(dist_dict.values())
    distances.sort()
    five_dists = []
    for i in range(0,5):
        five_dists.append(distances[i])
    return five_dists

def print_stops(locations, dist_dict, stops):
    '''
    Prints the 5 closest bus stops names, id, and distance from click

    Parameters: locations list, dist_dict dict, stops dict
    Returns: None
    '''
    print("Nearest stops:")
    print("\t\tDistance \tStop \t\tDescription")
    #Loops through dist_dict and checks for bus stop matching coordinates of the 5 
    #smallest locations
    for key in dist_dict.keys():
        for i in range(len(locations)):
            if dist_dict[key] == locations[i]:
                print(f"\t\t{locations[i]} \t\t{stops[key]}")
main()