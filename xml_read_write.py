from xml.dom import minidom


path_to_xml_config = r"C:\RAEngineering\LED_detection_config.xml"
def write_coordinates_to_xml(list_of_roi):
    # Create the minidom document
    doc = minidom.Document()

    # Create the <coordinates> base element
    coordinates_element = doc.createElement('coordinates')
    doc.appendChild(coordinates_element)

    # Loop through each tuple in the list and create elements for them
    for index, ((x1, y1), (x2, y2)) in enumerate(list_of_roi):
        # Create the <coordinate> element for each tuple
        coordinate_element = doc.createElement('coordinate')

        # Set attribute 'id' to differentiate between coordinate pairs
        coordinate_element.setAttribute('id', str(index + 1))

        # Create individual elements for each coordinate
        x1_element = doc.createElement('x1')
        x1_text = doc.createTextNode(str(x1))
        x1_element.appendChild(x1_text)

        y1_element = doc.createElement('y1')
        y1_text = doc.createTextNode(str(y1))
        y1_element.appendChild(y1_text)

        x2_element = doc.createElement('x2')
        x2_text = doc.createTextNode(str(x2))
        x2_element.appendChild(x2_text)

        y2_element = doc.createElement('y2')
        y2_text = doc.createTextNode(str(y2))
        y2_element.appendChild(y2_text)

        # Append the coordinate elements to the <coordinate> element
        coordinate_element.appendChild(x1_element)
        coordinate_element.appendChild(y1_element)
        coordinate_element.appendChild(x2_element)
        coordinate_element.appendChild(y2_element)

        # Append the <coordinate> element to the <coordinates> base element
        coordinates_element.appendChild(coordinate_element)

    # Write the XML to a file
    xml_str = doc.toprettyxml(indent="  ")
    with open(path_to_xml_config, "w") as f:
        f.write(xml_str)

    print("XML file created successfully!")


def read_coordinates_from_xml(path_to_config_xml):
    """
    Reads coordinates from an XML file and returns a list of tuples.

    Returns:
        list: List of tuples representing coordinates.
    """
    # Parse the XML file
    doc = minidom.parse(path_to_config_xml)
    coordinates_list = []

    # Get all <coordinate> elements
    coordinate_elements = doc.getElementsByTagName("coordinate")

    # Extract the coordinates and add them to the list
    for coordinate_element in coordinate_elements:
        x1 = int(coordinate_element.getElementsByTagName("x1")[0].firstChild.data)
        y1 = int(coordinate_element.getElementsByTagName("y1")[0].firstChild.data)
        x2 = int(coordinate_element.getElementsByTagName("x2")[0].firstChild.data)
        y2 = int(coordinate_element.getElementsByTagName("y2")[0].firstChild.data)

        coordinates_list.append(((x1, y1), (x2, y2)))

    return coordinates_list


if __name__ == "__main__":
    # example_list_of_roi = [((90, 140), (109, 156)), ((201, 196), (218, 217))]
    example_list_of_roi = []
    write_coordinates_to_xml(example_list_of_roi)
    print(example_list_of_roi)
    print(read_coordinates_from_xml(path_to_xml_config))
