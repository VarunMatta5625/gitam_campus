from nodes import locations  
from visualizer import visualize_path

def main():
    print("Here are the Available nodes:")
    print(", ".join(sorted(locations)))

    start = input("\nEnter START node: ").strip()
    end = input("Enter END node: ").strip()

    if start not in locations:
        print(f"Start Node {start} does not exist")
        return
    if end not in locations:
        print(f"End Node {end} does not exist")
        return

    print(f"\n🚀 Finding shortest path from {start} to {end}...\n")
    visualize_path("data/gitam_map.png", start, end)


if __name__ == "__main__":
    main()
