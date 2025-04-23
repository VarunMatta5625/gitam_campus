# analytics_visualizer/main.py

from data_io.generate_all_paths import generate_all_paths
from stats.run_all import run_all as run_all_statistics  # make sure function name matches

def main():
    print("Starting Analytics Visualizer\n")

    print("Generating All Path Pairs...")
    generate_all_paths()

    print("\nAll paths generated \nRunning Statistical Reports")
    run_all_statistics()

    print("\nAll tasks completed successfully.")

if __name__ == "__main__":
    main()
