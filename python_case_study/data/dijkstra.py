import heapq # to implement a priority queue order
from graph import graph

def dijkstra(start, end):
    queue = [(0, start, [])]  # (distance, current_node, path)
    visited = set() #keeps a trakc of whats visited, so we wont check them again and it is a set to remove redundancy
    explored_order = [] #for visualizer later on to draw the routes
    shortest_paths = {} #stores shortest path to each node

    while queue: #as long as there is something in queue
        (cost, node, path) = heapq.heappop(queue) #removes the smallest item
        #cost is weight, or distance
        if node in visited: #skips any node that was already visited
            continue

        visited.add(node) #adds to the visisted set
        explored_order.append(node) #adds to explored list
        path = path + [node] #this extends the path by adding each node 
        shortest_paths[node] = (cost, path) #shortest distance to each node 

        if node == end: #once it reaches end
            return { #returns disatcne, the path formed so far, whats been visited and in which order has it been visited.
                "distance": cost, 
                "path": path,
                "visited": list(visited),
                "explored_order": explored_order
            }
        #provided the current node is not the end point, this continues to examine the neighbouring nodes
        for neighbor, weight in graph.get(node, {}).items(): #gets a neighbouring node if it exists, and none if it does not 
            if neighbor not in visited: #if a neighbour node is not visidted
                heapq.heappush(queue, (cost + weight, neighbor, path)) #it gets added into the priority queue

    return { 
        "distance": float('inf'),
        "path": [],
        "visited": list(visited),
        "explored_order": explored_order
    }

# Example usage
if __name__ == "__main__":
    result = dijkstra("VS", "GB")
    print("Shortest Distance:", result["distance"])
    print("Path:", " -> ".join(result["path"]))
