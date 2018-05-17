import xml.etree.ElementTree as etree


class XmlUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_namespace_prefix(namespace):
        return str(namespace).split(':')

    @staticmethod
    def get_full_namespace(elem):
        return str(elem.tag).partition('}')[0] + '}'

    @staticmethod
    def print_all(nodes):
        for node in nodes.iter():
            print(node.tag)
            print(node.attrib)
            print(node.text)
            print()

    @staticmethod
    def parse_map(file):

        events = "start", "start-ns", "end-ns"

        root = None
        ns_map = []

        for event, elem in etree.iterparse(file, events):
            if event == "start-ns":
                ns_map.append(elem)
            elif event == "start":
                if root is None:
                    root = elem

        return {'tree': etree.ElementTree(root), 'ns_map': ns_map}

    @staticmethod
    def parse_xmlns(file):

        events = "start", "start-ns"

        root = None
        ns_map = []

        for event, elem in etree.iterparse(file, events):

            if event == "start-ns":
                ns_map.append(elem)

            elif event == "start":
                if root is None:
                    root = elem
                for prefix, uri in ns_map:
                    if prefix=="":
                        elem.set("xmlns",uri)
                    else:
                        elem.set("xmlns:" + prefix, uri)
                ns_map = []

        return etree.ElementTree(root)

    @staticmethod
    def fixup_xmlns(elem, maps=None):

        if maps is None:
            maps = [{}]

        # check for local overrides
        xmlns = {}
        for key, value in elem.items():
            if key[:6] == "xmlns:":
                xmlns[value] = key[6:]
        if xmlns:
            uri_map = maps[-1].copy()
            uri_map.update(xmlns)
        else:
            uri_map = maps[-1]

        # fixup this element
        fixup_element_prefixes(elem, uri_map, {})

        # process elements
        maps.append(uri_map)
        for elem in elem:
            XmlUtils.fixup_xmlns(elem, maps)
        maps.pop()

    @staticmethod
    def write_xmlns(elem, file):

        if not etree.iselement(elem):
            elem = elem.getroot()

        XmlUtils.fixup_xmlns(elem)

        etree.ElementTree(elem).write(file, encoding='utf-8')


def fixup_element_prefixes(elem, uri_map, memo):
    def fixup(name):
        try:
            return memo[name]
        except KeyError:
            if name[0] != "{":
                return
            uri, tag = name[1:].split("}")
            if uri in uri_map:
                if uri_map[uri] == '':
                    new_name = tag
                else:
                    new_name = uri_map[uri] + ":" + tag
                memo[name] = new_name
                return new_name

    # fix element name
    name = fixup(elem.tag)
    if name:
        elem.tag = name
    # fix attribute names
    for key, value in elem.items():
        name = fixup(key)
        if name:
            elem.set(name, value)
            del elem.attrib[key]
