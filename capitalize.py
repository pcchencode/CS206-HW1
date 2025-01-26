def capitalize(sentence: str) -> str:
    """
    Capitalizes the first letter of a sentence or word.

    """
    from string import ascii_lowercase, ascii_uppercase

    if not sentence:
        return ""

    # Create a dictionary that maps lowercase letters to uppercase letters
    # Capitalize the first character if it's a lowercase letter
    # Concatenate the capitalized character with the rest of the string
    lower_to_upper = dict(zip(ascii_lowercase, ascii_uppercase))
    return lower_to_upper.get(sentence[0], sentence[0]) + sentence[1:]