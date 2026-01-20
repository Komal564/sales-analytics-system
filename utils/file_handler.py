#========================
## Part 1 :
# File handler module for reading sales data

#=========================
# Data file Handler & Preprocessing

# Task 1.1: Read sales data with Encoding Handling

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """

    supported_encodings = ["utf-8", "latin-1", "cp1252"]
    lines = []

    for enc in supported_encodings:
        try:
            file = open(filename, "r", encoding=enc)
            lines = file.readlines()
            file.close()
            return lines

        except UnicodeDecodeError:
            # Try next encoding
            continue

        except FileNotFoundError:
            print("Error: File not found")
            return []

    print("Error: Unable to read file with supported encodings")
    return []