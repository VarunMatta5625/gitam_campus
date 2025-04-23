from graph import graph

def dijkstra(start, end, graph):
    queue = [(0, start, [])]  # (distance, current_node, path)
    visited = set()
    explored_order = []

    while queue:
        # Sort queue ascedningly since we need the lowest cost neighbour first
        queue.sort(key=lambda x: x[0]) 
        cost, node, path = queue.pop(0)  # pop the first item (lowest cost coz its sorted) and unpack it respectivdely 

        if node in visited: #since visited nodes need not be revisited. 
            continue

        visited.add(node) #if not visited already, it needs to be marked as visited
        explored_order.append(node)
        path = path + [node]

        if node == end: #break point for the function
            return {
                "distance": cost,
                "path": path,
                "visited": list(visited),
                "explored_order": explored_order
            }

        for neighbor, weight in graph.get(node, {}).items(): 
            if neighbor not in visited:
                queue.append((cost + weight, neighbor, path))  # add the neighbour to the queue 

    return { #when the end point is not found , or like when a valid path isnt found 
        "distance": float('inf'), #infinte distance 
        "path": [],
        "visited": list(visited),
        "explored_order": explored_order
    }
