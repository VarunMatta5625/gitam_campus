from stats.centrality_rank import get_summary as get_centrality
from stats.bridge_node_rank import get_summary as get_bridge
from stats.most_used_segments import get_summary as get_segments

def run_all():
    for title, get_data in [
        ("Centrality & Accessibility Ranking", get_centrality),
        ("Bridge Node Ranking", get_bridge),
        ("Most Frequently Used Path Segments", get_segments),
    ]:
        print(f"\n🔷🔷🔷 {title} 🔷🔷🔷")
        data = get_data()

        print(f"\n🏆 Main Result: {data['main_result']}")
        print("\n📊 Top Entries:")

        # Special unpacking for path segments
        if title == "Most Frequently Used Path Segments":
            for rank, entry in enumerate(data["top_entries"], 1):
                label = entry[0]
                value = entry[1]
                print(f"{rank}. [Used {value} times] {label}")
        else:
            for rank, (label, value) in enumerate(data["top_entries"], 1):
                print(f"{rank}. {label} – {value}")

        print("\n📝 Markdown Summary:")
        print(data["markdown"])
