def parse_string_list(string):
    """
    Parse a string like "[a, b, c]" and return a list of strings like ["a", "b", "c"]

    Parameters
    ----------
    string : str
        String to parse.

    Returns
    -------
    list
        List of strings.
    """
    # Remove the brackets from the string
    string = string[1:-1]

    # Split the string by commas
    string_list = string.split(", ")

    # Trim whitespace from each string
    string_list = [s.strip() for s in string_list]

    return string_list
