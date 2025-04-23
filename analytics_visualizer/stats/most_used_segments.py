from data_io.edge_heatmap_data import edge_usage

def get_summary():
    # Step 1: Sort edge usage data
    sorted_edges = sorted(edge_usage.items(), key=lambda x: x[1], reverse=True)
    top_edges = sorted_edges[:30]

    # Step 2: Format results as (label, count)
    formatted_top = [
        (f"{a} → {b}", count)
        for (a, b), count in top_edges
    ]

    return {
        "title": "Most Frequently Used Edges",
        "main_result": formatted_top[0][0],
        "top_entries": formatted_top,
        "markdown": f"The most frequently used edge is:\n\n**{formatted_top[0][0]}**\n\nIt was used **{formatted_top[0][1]} times** in shortest paths."
    }
