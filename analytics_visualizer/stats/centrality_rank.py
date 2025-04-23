from data_io.distance_matrix import distance_matrix

def get_summary():
    avg_distances = {}

    # Step 1: Calculate average distance from each node to all others
    for location, targets in distance_matrix.items():
        total = sum(targets.values())
        count = len(targets)
        avg = total / count if count else float('inf')
        avg_distances[location] = round(avg, 2)

    # Step 2: Sort the ranking
    sorted_ranks = sorted(avg_distances.items(), key=lambda x: x[1])
    best_location, best_avg = sorted_ranks[0] if sorted_ranks else (None, float('inf'))

    # Get top 5 and bottom 5
    top_entries = sorted_ranks[:5]
    bottom_entries = sorted_ranks[-5:]

    # Step 3: Return structured summary
    return {
        "title": "Centrality & Accessibility Ranking",
        "main_result": best_location,
        "top_entries": top_entries + bottom_entries,
        "markdown": f"""**{best_location}** is the most centrally accessible location with an average shortest path distance of **{best_avg:.2f} meters** to all other locations.

    _(Note: List shows top 5 most accessible and bottom 5 least accessible locations.)_"""
    }

