import sys
import coverage
import json
import importlib.util

def load_module(module_path):
    """ Dynamically loads a module from a given file path. """
    module_name = module_path.replace(".py", "").replace("/", ".").replace("\\", ".")
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module

def parse_input(line):
    """Convert a single input line into the correct type (list, int, or string)."""
    line = line.strip()

    # Try parsing as JSON
    try:
        parsed = json.loads(line)  
        if isinstance(parsed, list):  # If it's a JSON list, return as list
            return parsed
        # elif isinstance(parsed, int):  # If it's an integer, return as int
        #     return parsed
        else:
            return str(parsed)  # Otherwise, return as string
    except json.JSONDecodeError:
        return line  # If not JSON, return original string

def main():
    # Check if the input file is provided
    if len(sys.argv) != 3:
        print("Usage: python <test_prog.py> <test_input>")
        sys.exit(1)

    test_prog = sys.argv[1]
    test_input = sys.argv[2]

    # Check if the input file exists
    try:
        with open(test_input, 'r') as file:
            inputs = file.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{test_input}' not found.")
        sys.exit(1)

    # from capitalize import capitalize
    # Dynamically load the test program
    module = load_module(test_prog)

    # Extract only user-defined functions from the loaded module
    functions = {
        name: obj for name, obj in vars(module).items()
        if callable(obj) and obj.__module__ == module.__name__
    }

    if not functions:
        print(f"Error: No callable functions found in '{test_prog}'")
        sys.exit(1)
    # Pick the first function found in the module for testing
    test_function = list(functions.values())[0]

    # Initialize and start the coverage tool
    cov = coverage.Coverage(source=[test_prog.replace(".py", "")])
    cov.start()

    # Process each line from the input file
    for line in inputs:
        input_data = parse_input(line)

        # print("====================================================")
        # sentence = line.strip()  # Remove any surrounding whitespace

        result = test_function(input_data)
        # result = test_function(sentence)
        # result = capitalize(sentence)  # Call the capitalize function
        
        # print(f"Input: {sentence} -> Output: {result}")
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # Analyze coverage data for capitalize.py
        # print("\nCoverage analysis for capitalize.py:")
        data = cov.get_data()
        for file_path in data.measured_files():
            if test_prog in file_path:
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