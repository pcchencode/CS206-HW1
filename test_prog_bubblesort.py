import sys
import json
import coverage

def main():
    # Check if the input file is provided
    if len(sys.argv) != 2:
        print("Usage: python test_prog_bubblesort.py <test_input>")
        sys.exit(1)

    test_input = sys.argv[1]

    # Check if the input file exists
    try:
        with open(test_input, 'r') as file:
            inputs = file.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{test_input}' not found.")
        sys.exit(1)

    # # Initialize and start the coverage tool
    # cov = coverage.Coverage(source=["bubblesort_recursive"])
    # cov.start()

    from bubblesort_recursive import bubble_sort_recursive  # Import the bubble_sort_recursive function
    # Initialize and start the coverage tool
    cov = coverage.Coverage(source=["bubblesort_recursive"])
    cov.start()

    # Process each line from the input file
    for line in inputs:
        # print("====================================================")
        try:
            collection = json.loads(line.strip())  # Parse JSON into Python list
            if not isinstance(collection, list):
                raise ValueError("Input is not a valid list")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format: {line.strip()}")
            continue
        input_collections = collection.copy()
        result = bubble_sort_recursive(collection)  # Call the bubble_sort_recursive function
        # print(f"Input: {input_collections} -> Output: {result}")
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        # Analyze coverage data for bubblesort_recursive.py
        data = cov.get_data()
        for file_path in data.measured_files():
            if "bubblesort_recursive.py" in file_path:
                with open(file_path, "r") as f:
                    lines = f.readlines()

                executed_lines = data.lines(file_path)

                # Print all lines with execution markers
                for i, content in enumerate(lines, start=1):
                    marker = " " if executed_lines and i in executed_lines else "#"
                    print(f"{marker} {i:2d} {content.strip()}")
        # print("====================================================")

    # Stop and save the coverage data
    cov.stop()
    cov.save()


if __name__ == "__main__":
    main()