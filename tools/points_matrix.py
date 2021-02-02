#TODO Modify this file to be CLI usable

import xml.etree.ElementTree as ET
from collections import namedtuple
from xml.dom import minidom

FILE_NAME = 'points_matrix.xml'
ELEMENT_NODE_NAME = 'element'

WRITE_XML = False  # TODO This should be driven by a CLI argument
READ_XML = True  # TODO This should be driven by a CLI argument


Structure = namedtuple('Structure', ['index', 'win', 'loss', 'accept_higher_index'])

structures = (
    Structure(index=0, win=20, loss=-10, accept_higher_index=False),
    Structure(index=1, win=21, loss=-9, accept_higher_index=False),
    Structure(index=2, win=22, loss=-8, accept_higher_index=False),
    Structure(index=3, win=23, loss=-7, accept_higher_index=False),
    Structure(index=4, win=24, loss=-6, accept_higher_index=False),
    Structure(index=5, win=25, loss=-5, accept_higher_index=False),
    Structure(index=6, win=26, loss=-4, accept_higher_index=False),
    Structure(index=7, win=27, loss=-3, accept_higher_index=False),
    Structure(index=8, win=28, loss=-2, accept_higher_index=False),
    Structure(index=9, win=29, loss=-1, accept_higher_index=False),
    Structure(index=10, win=30, loss=0, accept_higher_index=True),
)

def write_xml():
    # create the file structure
    matrix = ET.Element('matrix')
    # import ipdb; ipdb.set_trace()
    for struct in structures:
        element = ET.SubElement(matrix, ELEMENT_NODE_NAME)
        attributes = {'accept_higher': str(int(struct.accept_higher_index))}
        ET.SubElement(element, 'match_index', attrib=attributes).text = str(struct.index)
        # match_index.set('accept_higher', str(int(struct.accept_higher_index)))
        # match_index.text = str(struct.index)
        ET.SubElement(element, 'points_win').text = str(struct.win)
        ET.SubElement(element, 'points_loss').text = str(struct.loss)

    # create a new XML file with the results
    # matrix_xml = prettify(matrix)
    data = ET.tostring(matrix, encoding='unicode')
    # rough_string = ET.tostring(elem)
    data_pretty = minidom.parseString(data).toprettyxml(indent='  ')

    # f = open("items2.xml", "w")
    # f.write(matrix_xml)
    with open(FILE_NAME, 'w') as f:
        f.write(data_pretty)

def _get_child(element, tag_name, raise_if_not_found=True):
    child_element = element.find(tag_name)
    if child_element is None:
        if raise_if_not_found:
            # raise ValueError(f'Child tag {tag_name!r} not found in element {element.tag!r}.')
            raise ValueError(f'Error while parsing file {FILE_NAME!r}: node {tag_name!r} not found in parent node {element.tag!r}.')
        return None
    return child_element

def get_points_matrix():
    matrix = []
    # Part 2: reading data
    tree = ET.parse(FILE_NAME)
    root = tree.getroot()
    print(root.tag)
    print(root.attrib)
    print(root[0][1].text)
    # for struct in root.findall(ELEMENT_NODE_NAME):
    for struct in root.iter(ELEMENT_NODE_NAME):
        match_index_el = _get_child(struct, 'match_index')
        matrix.append(Structure(
            index=int(match_index_el.text),
            win=int(_get_child(struct, 'points_win').text),
            loss=int(_get_child(struct, 'points_loss').text),
            accept_higher_index=bool(int(match_index_el.attrib.get('accept_higher', False))),
            # index=_get_child_value(struct, 'match_index', int),
            # win=_get_child_value(struct, 'points_win', int),
            # loss=_get_child_value(struct, 'points_loss', int),
            # accept_higher_index=_get_child_value(struct, ''),
        ))
        # for x in struct:
        #     import ipdb; ipdb.set_trace()
        #     print(x.tag, x.attrib, x.text)
    return matrix
# ipdb> struct.find('points_winZ').text
# *** AttributeError: 'NoneType' object has no attribute 'text'

def get_points_dict():
    # TODO Manage 'accept_higher_index' attribute
    return {
        struct.index: struct
        for struct in get_points_matrix()
    }

if __name__ == '__main__':
    if WRITE_XML:
        write_xml()
    if READ_XML:
        from pprint import pprint as pp
        pp(get_points_matrix())
