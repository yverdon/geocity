import re

from unidecode import unidecode


def convert_string_to_api_key(string):
    # Convert to lower and remove accents
    string = unidecode(string.lower())
    # Delete special characters and spaces
    string = re.sub("[^a-z0-9_ ]", "", string)
    string = string.replace(" ", "_")
    return string
