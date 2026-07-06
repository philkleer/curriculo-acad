import argparse
import os
import xml.etree.ElementTree as ET

import toml


def xml_to_dict(element):
    """
    Recursively convert an XML element and its children into a dictionary.
    """
    result = {}
    # Add attributes as key-value pairs
    for key, value in element.attrib.items():
        result[key] = value

    # Add child elements
    for child in element:
        child_dict = xml_to_dict(child)
        # Handle multiple children with the same tag
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_dict)
        else:
            result[child.tag] = child_dict

    # Add text content if it exists
    if element.text and element.text.strip():
        result["_text"] = element.text.strip()

    return result


def save_dict_as_toml(data, output_file):
    """
    Save a dictionary as a TOML file.
    """
    with open(output_file, "w") as f:
        toml.dump(data, f)


def main():
    parser = argparse.ArgumentParser(
        description="Convert an XML file to a TOML file."
    )
    parser.add_argument("input_file", help="Path to the input XML file.")
    args = parser.parse_args()

    input_file = args.input_file
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        return

    # Ensure the parser uses ISO-8859-1 encoding
    parser = ET.XMLParser(encoding="ISO-8859-1")
    tree = ET.parse(input_file, parser=parser)
    root = tree.getroot()

    # Convert XML to dictionary
    data_dict = xml_to_dict(root)

    # Generate output filename
    output_file = os.path.splitext(input_file)[0] + ".toml"

    # Save the dictionary as a TOML file
    save_dict_as_toml(data_dict, output_file)

    print(f"TOML file saved as: {output_file}")


if __name__ == "__main__":
    main()
