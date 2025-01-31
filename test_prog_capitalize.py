import sys
import coverage

def main():
    # Check if the input file is provided
    if len(sys.argv) != 2:
        print("Usage: python test_prog.py <test_input>")
        sys.exit(1)

    test_input = sys.argv[1]

    # Check if the input file exists
    try:
        with open(test_input, 'r') as file:
            inputs = file.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{test_input}' not found.")
        sys.exit(1)

    from capitalize import capitalize
    # Initialize and start the coverage tool
    cov = coverage.Coverage(source=["capitalize"])
    cov.start()

    # Process each line from the input file
    for line in inputs:
        # print("====================================================")
        sentence = line.strip()  # Remove any surrounding whitespace
        result = capitalize(sentence)  # Call the capitalize function
        # print(f"Input: {sentence} -> Output: {result}")
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # Analyze coverage data for capitalize.py
        # print("\nCoverage analysis for capitalize.py:")
        data = cov.get_data()
        for file_path in data.measured_files():
            if "capitalize.py" in file_path:
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