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

#this function helps avoid repetitive scaling calls by wrapping scale_coords for a node
def scaled_coords_for(node, coords, original_shape, new_shape, pad_x, pad_y):
    return scale_coords(*coords[node], original_shape, new_shape, pad_x, pad_y)

#this function draws the pathfinding legend (explored paths, shortest path, start/end points)
def draw_legend(display_map, target_size):
    # since the legend box should be top-left of the window
    legend_x, legend_y = target_size[0] - 250, 30 # 250 from right, 30 from top
    spacing = 30 #instead of manually defining spacing everytime
     
    cv2.rectangle(display_map, (legend_x - 20, legend_y - 20), (target_size[0] - 10, legend_y + spacing * 5), (255, 255, 255), -1)
    cv2.putText(display_map, "Legend:", (legend_x, legend_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.line(display_map, (legend_x, legend_y + spacing), (legend_x + 20, legend_y + spacing), (0, 255, 255), 3, cv2.LINE_AA)
    cv2.putText(display_map, "Explored path", (legend_x + 30, legend_y + spacing + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.circle(display_map, (legend_x + 10, legend_y + spacing * 2), 6, (0, 255, 255), -1)
    cv2.putText(display_map, "Explored node", (legend_x + 30, legend_y + spacing * 2 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.line(display_map, (legend_x, legend_y + spacing * 3), (legend_x + 20, legend_y + spacing * 3), (0, 0, 255), 3, cv2.LINE_AA)
    cv2.putText(display_map, "Shortest path", (legend_x + 30, legend_y + spacing * 3 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.circle(display_map, (legend_x + 10, legend_y + spacing * 4), 6, (0, 255, 0), -1)
    cv2.putText(display_map, "Start point", (legend_x + 30, legend_y + spacing * 4 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.circle(display_map, (legend_x + 10, legend_y + spacing * 5), 6, (255, 0, 0), -1)
    cv2.putText(display_map, "End point", (legend_x + 30, legend_y + spacing * 5 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

#this function draws the summary box with total distance and node count on the bottom of the map
def draw_summary_box(display_map, start, end, total_distance, shortest_path, target_size):
    from_node = start.upper()
    to_node = end.upper()
    lines = [
        f"From: {from_node}",
        f"To: {to_node}",
        f"Distance: {total_distance} m",
        f"Nodes crossed: {max(len(shortest_path) - 2, 0)}"
    ]
    font_scale = 0.8
    thickness = 2
    line_height = 30
    box_height = line_height * len(lines) + 20
    longest_line = max(lines, key=len)
    (text_width, _), _ = cv2.getTextSize(longest_line, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    box_width = text_width + 40
    box_x = 10
    box_y = target_size[1] - box_height - 10
    cv2.rectangle(display_map, (box_x, box_y), (box_x + box_width, box_y + box_height), (255, 255, 255), -1)
    for i, line in enumerate(lines):
        text_y = box_y + 30 + i * line_height
        cv2.putText(display_map, line, (box_x + 10, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness)


#this function take the image and resizes it without distorion , since distorting has been noticed a lot while debugging.
def resize_with_padding(img, target_size): 
    #img is again a numpy image array 
    #target size (a tuple) is set to 720p 
    original_h, original_w = img.shape[:2]
    target_w, target_h = target_size

    scale = min(target_w / original_w, target_h / original_h)
    #the smallest ratio so that neither width nor height exceeds Live Pathfinding window dimensions
    new_w = int(original_w * scale)
    new_h = int(original_h * scale)

    resized_img = cv2.resize(img, (new_w, new_h)) 
    #find the difference between target image size layout size, and new scaled down image size
    #both height wise and width wise.
    pad_x = (target_w - new_w) // 2 
    pad_y = (target_h - new_h) // 2 

    padded_img = np.full((target_h, target_w, 3), 255, dtype=np.uint8) 
    #dtype=np.uint8 sets the datatype of each pixel to unsigned 8 bit integers, standard procedure
    padded_img[pad_y:pad_y+new_h, pad_x:pad_x+new_w] = resized_img
    #now the above line replaces padding in the place of where the map image is to come.
    return padded_img, (new_h, new_w), pad_x, pad_y
    #returns the new image, which is scaled, and has padding to fill for the target size.
    #newly formed image dimensions and padding dimensions as well

# Main function for the visualizwer
def visualize_path(map_file_path, start, end, output_path="visualized_path.png", target_size=(1280, 720)):

    map_img = cv2.imread(map_file_path) #reads the image as a numpy array now.

    if map_img is None: #if image is not found
        raise FileNotFoundError(f"Could not load image at path: {map_file_path}")

    if target_size is None:
        target_size = (map_img.shape[1], map_img.shape[0]) 
        #map_img.shape returns a tuple of 3 dimension, width - rows, height - columns, number of colour channels

    original_shape = map_img.shape[:2] #to store the dimensions and not the colour channels
    display_map, new_shape, pad_x, pad_y = resize_with_padding(map_img, target_size)
    #now the resized image with padding has been created, we also have the dimensions for padding and the resized image
    #we can begin with starting the visualization.
    cv2.startWindowThread() # starts a opencv thread, actually can be removed, but safe to keep 
    cv2.namedWindow("Live Pathfinding", cv2.WINDOW_NORMAL) # with inclusion for manual window resizing
    cv2.resizeWindow("Live Pathfinding", target_size[0], target_size[1]) #sizes it defaulty for current traget dimensions
    cv2.imshow("Live Pathfinding", display_map)
    cv2.waitKey(2000) # waits 2 seconds 

    draw_legend(display_map, target_size)  #map's legend

    if start in coords and end in coords:
        sx, sy = scaled_coords_for(start, coords, original_shape, new_shape, pad_x, pad_y)
        ex, ey = scaled_coords_for(end, coords, original_shape, new_shape, pad_x, pad_y)
        cv2.circle(display_map, (sx, sy), 10, (0, 255, 0), -1) #mark start as green
        cv2.circle(display_map, (ex, ey), 10, (255, 0, 0), -1) #mark end as blue
        cv2.imshow("Live Pathfinding", display_map) #updates the live pathfindng window
        cv2.waitKey(2000) #so user can see the start and end point being marked 

    result = dijkstra(start, end, graph)
    explored_order = result["explored_order"]
    shortest_path = result["path"]
    total_distance = result["distance"]

    total_map_nodes = len(coords) #gets the total count of nodes.
    explored_count = 0 #intitally we have explored through 0 nodes of the path


    #handles all yellow lines , drawn for exploration
    for node in explored_order:
        if node not in graph or node not in coords: #accounts for corner case
            continue
        #scales down a coordinate of a node on the map
        x1, y1 = scaled_coords_for(node, coords, original_shape, new_shape, pad_x, pad_y)

        for neighbor in graph[node]:
            if neighbor in coords:
                x2, y2 = scaled_coords_for(neighbor, coords, original_shape, new_shape, pad_x, pad_y)
                # draw yellow line to visualize exploration.
                cv2.line(display_map, (x1, y1), (x2, y2), (0, 255, 255), 3, cv2.LINE_AA) 

        cv2.circle(display_map, (x1, y1), 6, (0, 255, 255), -1)
        explored_count += 1 #increment explored count by 1, so we know how much we have explored
        explored_percent = (explored_count / total_map_nodes) * 100
        label_lines = ["Explored", f"{explored_percent:.1f}% | {explored_count}/{total_map_nodes} nodes"]

        #draws the explored path composotion wrt the whole map
        box_width, line_height = 260, 25
        box_height = line_height * len(label_lines) + 20
        x, y = target_size[0] - box_width - 10, 10
        cv2.rectangle(display_map, (x, y), (x + box_width, y + box_height), (255, 255, 255), -1)
        for i, line in enumerate(label_lines):
            cv2.putText(display_map, line, (x + 10, y + 30 + i * line_height),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        cv2.imshow("Live Pathfinding", display_map)
        cv2.waitKey(700)

    for i in range(len(shortest_path) - 1):
        n1, n2 = shortest_path[i], shortest_path[i + 1]
        if n1 in coords and n2 in coords:
            x1, y1 = scaled_coords_for(n1, coords, original_shape, new_shape, pad_x, pad_y)
            x2, y2 = scaled_coords_for(n2, coords, original_shape, new_shape, pad_x, pad_y)
            cv2.line(display_map, (x1, y1), (x2, y2), (0, 0, 255), 4, cv2.LINE_AA)
            cv2.imshow("Live Pathfinding", display_map)
            cv2.waitKey(120)

    draw_summary_box(display_map, start, end, total_distance, shortest_path, target_size)

    cv2.imshow("Live Pathfinding", display_map)
    cv2.imwrite(output_path, display_map)
    print(f"Visualization saved to {output_path}")
    print("Press any key in the window to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
