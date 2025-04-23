from data_io.node_heatmap_data import node_visit_count

def get_summary():
    # Step 1: Sort the node visit counts
    sorted_bridges = sorted(node_visit_count.items(), key=lambda x: x[1], reverse=True)

    # Step 2: Best bridge node
    best_node, best_count = sorted_bridges[0] 

    # Step 3: Build summary dictionary
    return {
        "title": "Bridge Node Ranking",
        "main_result": best_node,
        "top_entries": sorted_bridges[:10],
        "markdown": f"**{best_node}** is the most frequently used *bridge node*, appearing in **{best_count} paths** (excluding start/end)."
    }