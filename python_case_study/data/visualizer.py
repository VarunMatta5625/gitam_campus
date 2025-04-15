import cv2
import numpy as np
from coords import coords
from dijkstra import dijkstra
from graph import graph

#to find proportion of coords on the rescaled image in pathfinding window
#x and y are original coords #original spare and new shape are about orignal and new scaled image
def scale_coords(x, y, original_shape, new_shape, pad_x, pad_y):  
    scale_x = new_shape[1] / original_shape[1] #finds ratios for x 
    scale_y = new_shape[0] / original_shape[0] #finds ratios for y 
    return int(x * scale_x + pad_x), int(y * scale_y + pad_y) #returns after taking padding into account.


#this function take the image and resizes it without distorion , since distorting has been noticed a lot while debugging.
def resize_with_padding(img, target_size): 
    #img is loaded as an array with help of numpy  
    #target size (a tuple) is set to HD 
    original_h, original_w = img.shape[:2]
    # since numpy img array has height, width and then color channels, we slice and take the first two only , that is height and width
    target_w, target_h = target_size #unpacking the tuple

    # here we compute the scale factor

    scale = min(target_w / original_w, target_h / original_h)
    new_w = int(original_w * scale)
    new_h = int(original_h * scale)

    # with the new height and width, image is scaled accordingly and resized. 

    resized_img = cv2.resize(img, (new_w, new_h))
    # find the amount of difference in image dimensions
    #carries it out and fills a padding , equally on both sides
    pad_x = (target_w - new_w) // 2  #floor div obviously 
    pad_y = (target_h - new_h) // 2 

    # creating a new image (numpy array ofc) with padding (and no map image yet) , based on previous calculations 

    padded_img = np.full((target_h, target_w, 3), 255, dtype=np.uint8)

    #since padded image is an array, the map pic has to be placed yet with proper alignment.
    padded_img[pad_y:pad_y+new_h, pad_x:pad_x+new_w] = resized_img  #earlier resized map pic is placed accoringly 

    return padded_img, (new_h, new_w), pad_x, pad_y  #everything is returned properly 


# Main function for the visualizwer
def visualize_path(map_path, start, end, output_path="visualized_path.png", target_size=(1280, 720)):

    #loading the map, passing from `main.py`
    map_img = cv2.imread(map_path) #imread is used to load map image from disc
    #imread return none when image isnt found or loaded

    if map_img is None: #sometimes file name is wrongly given, so to include a corner case , this is needed
        raise FileNotFoundError(f"Could not load image at path: {map_path}") #exception handling 😊

    if target_size is None: #unless specified from main, visualize_path doesnt mess with image scaling 
        target_size = (map_img.shape[1], map_img.shape[0])  # Use original image resolution

    original_shape = map_img.shape[:2] #grabs the original map image (gitam_map.png file) dimensions 
    #the following line calls the function near ln 15, to resize the image, since main calls visualizer and that calls resizer!

    #grabs the resized image, dimensions of new resized image, and the padding that needs to be added
    display_map, new_shape, pad_x, pad_y = resize_with_padding(map_img, target_size) 


    #not sure, but this is for the internal gui calling for opencv. Begins a thread inside the OS
    cv2.startWindowThread()
    # creates a window named "Liv Pathdfinding" where images are shown
    cv2.namedWindow("Live Pathfinding", cv2.WINDOW_NORMAL)  
    # in above line, update: WINDOW NORMAL is added so i can later resize it if and when casting to an extrernal display

    #defaulty resizes the window for now with the settings we have caluclated earlier, but i can change later
    cv2.resizeWindow("Live Pathfinding", target_size[0], target_size[1]) 
    cv2.imshow("Live Pathfinding", display_map) #display the image map

    cv2.waitKey(1000) #1000 delay is added so that every key event change may be observed by the faculty easily
    #since imshow doesn’t actually update the window immediately; it queues the image to be shown.
    #So calling waitKey not only waits, but also serves to process the event that draws the display_map

    # Draw legend
    legend_x, legend_y = target_size[0] - 250, 30  #starting at top-left corner for looks perspect.
    spacing = 30 #for indiviual gap

    #draws a whtie rectangeel as the background of the legned.
    cv2.rectangle(display_map, (legend_x - 20, legend_y - 20), (target_size[0] - 10, legend_y + spacing * 5), (255, 255, 255), -1)

    #legend title
    cv2.putText(display_map, "Legend:", (legend_x, legend_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    #to show yellow lines mean the explored paths.
    #draws a yellow line
    cv2.line(display_map, (legend_x, legend_y + spacing), (legend_x + 20, legend_y + spacing), (0, 255, 255), 3, cv2.LINE_AA)
    #labels it as a explored path inside the legend
    cv2.putText(display_map, "Explored path", (legend_x + 30, legend_y + spacing + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    #to show yellow dots mean explored nodes
    #draws a yellow dot
    cv2.circle(display_map, (legend_x + 10, legend_y + spacing * 2), 6, (0, 255, 255), -1)
    #labels it as a explored node inside the legend
    cv2.putText(display_map, "Explored node", (legend_x + 30, legend_y + spacing * 2 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    #to show red lines mean shortest path 
    #draws a yellow dot
    cv2.line(display_map, (legend_x, legend_y + spacing * 3), (legend_x + 20, legend_y + spacing * 3), (0, 0, 255), 3, cv2.LINE_AA)
    #labels it as shortest padth
    cv2.putText(display_map, "Shortest path", (legend_x + 30, legend_y + spacing * 3 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    #shows the starting point and ending point with color schema
    cv2.circle(display_map, (legend_x + 10, legend_y + spacing * 4), 6, (0, 255, 0), -1)
    cv2.putText(display_map, f"Start point - {start}", (legend_x + 30, legend_y + spacing * 4 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.circle(display_map, (legend_x + 10, legend_y + spacing * 5), 6, (255, 0, 0), -1)
    cv2.putText(display_map, f"End point - {end}", (legend_x + 30, legend_y + spacing * 5 + 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


    result = dijkstra(start, end) #dijkstra is imporeted ofc at the top of this file 
    #dijkstra returns a dictionarity, so result here is a dictionary
    #this dictionaoryy consists of explored order, the shortest path , and also total distance for the shortest patgh
    explored_order = result["explored_order"]
    shortest_path = result["path"]
    total_distance = result["distance"]

    total_map_nodes = len(coords) #calcuated so that it can also be displayed at the end and also for coverage % calc
    explored_count = 0 #intially zero obviosuly 

    for node in explored_order: #takes each nodes from the explored path 
        if node not in graph or node not in coords: #safety measure for corner cases if any , recommened by jack
            continue

        #we have a coords file as well, storing all pixel coroords for eahc node
        #mind u we need to keep every alignment w.r.t to the new scaled image, complicated but works!! 😊
        x1, y1 = scale_coords(*coords[node], original_shape, new_shape, pad_x, pad_y)  # * for unpacking


        for neighbor in graph[node]: #sinch graph is a dict with all edges fed into it.
            if neighbor in coords: #coz we'd rahther have a misplaneted illustartion a program breakdown due to an error
                x2, y2 = scale_coords(*coords[neighbor], original_shape, new_shape, pad_x, pad_y) #for neighbour scale co-ordinate
                #daws a line from current node to nieghbouring node
                #x1,y1 to x2,y2
                cv2.line(display_map, (x1, y1), (x2, y2), (0, 255, 255), 3, cv2.LINE_AA)
        #draws a filled yellow circle to makr the explored node 
        cv2.circle(display_map, (x1, y1), 6, (0, 255, 255), -1)

        explored_count += 1 #counter for explored nodes
        explored_percent = (explored_count / total_map_nodes) * 100 #percentage calculation
        #to show the 'explored' data
        label_lines = [ 
            "Explored",
            f"{explored_percent:.1f}% | {explored_count}/{total_map_nodes} nodes"
        ] #can be expanded if time permits

        #the white box dims
        box_width, line_height = 260, 25 
        box_height = line_height * len(label_lines) + 20

        #where to draw the box 
        x, y = target_size[0] - box_width - 10, 10 

        #drawing that box using opencv
        cv2.rectangle(display_map, (x, y), (x + box_width, y + box_height), (255, 255, 255), -1)
        for i, line in enumerate(label_lines): #Loop to write each line of text
            cv2.putText(display_map, line, (x + 10, y + 30 + i * line_height),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        cv2.imshow("Live Pathfinding", display_map)
        cv2.waitKey(700) #To show the updated frame & wiat then briefly

    #Final Shortest path animation with red lines
    #loop to iteratrate through each node of the shortest path 
    for i in range(len(shortest_path) - 1):
        n1, n2 = shortest_path[i], shortest_path[i + 1] #take a node in the shortest and its forward neighbour
        if n1 in coords and n2 in coords: #to avoid corner cases
            #gets scaled coords for the nordes.
            x1, y1 = scale_coords(*coords[n1], original_shape, new_shape, pad_x, pad_y)
            x2, y2 = scale_coords(*coords[n2], original_shape, new_shape, pad_x, pad_y)
            cv2.line(display_map, (x1, y1), (x2, y2), (0, 0, 255), 4, cv2.LINE_AA) #draw a red line between adjoining
            cv2.imshow("Live Pathfinding", display_map)
            cv2.waitKey(120) #waits 120 ms to draw each edges in the shortest path 


    #and to finally marek the start and end points with green and blue
    if shortest_path: #again to avoid corner case, only if there is a shortest path (starting is not same as ending )
        sx, sy = scale_coords(*coords[shortest_path[0]], original_shape, new_shape, pad_x, pad_y) #for startt
        ex, ey = scale_coords(*coords[shortest_path[-1]], original_shape, new_shape, pad_x, pad_y) # for ending 
        cv2.circle(display_map, (sx, sy), 10, (0, 255, 0), -1) #draws ciecles
        cv2.circle(display_map, (ex, ey), 10, (255, 0, 0), -1) #draws circles


    # To summarize the total distance travlled and nodes covered
    text_line1 = f"Distance: {total_distance} m"
    text_line2 = f"Nodes crossed: {max(len(shortest_path) - 2, 0)}" #excludes the start and end node 
    
    #draws up a rectangle and puts the text in there.
    cv2.rectangle(display_map, (10, target_size[1] - 85), (450, target_size[1] - 25), (255, 255, 255), -1)
    cv2.putText(display_map, text_line1, (20, target_size[1] - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(display_map, text_line2, (20, target_size[1] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.imshow("Live Pathfinding", display_map)
    cv2.imwrite(output_path, display_map) #to save the final map as 'visualized_path.png
    print(f"Visualization saved to {output_path}")
    print("Press any key in the window to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
