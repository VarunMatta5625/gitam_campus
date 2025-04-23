from nodes import locations  
from visualizer import visualize_path

def main():
    print("Pick a Start and End point from the below list of locations: ")
    print(", ".join(sorted(locations)))

    start = input("\nEnter START node: ").strip()
    end = input("Enter END node: ").strip()


    #to account for user input error / typos
    if start not in locations: 
        print(f"Start Node {start} does not exist")
        return
    if end not in locations:
        print(f"End Node {end} does not exist")
        return
    if start == end:
        print("Start and End nodes are the same. Which means you're already there!")
        return

    print(f"\n Finding shortest path from {start} to {end}...\n")
    print(f'\n\n Open the "Live pathfinding" window in the taskbar')
    visualize_path("data/gitam_map.png", start, end)

if __name__ == "__main__":
    main()
