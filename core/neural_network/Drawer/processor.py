from copy import deepcopy
import xml.etree.ElementTree as etree


class ReglamentProcessor:
    @staticmethod
    def add_to_query(tree, text):
        root = tree.getroot()
        namespace = str(root.tag).partition('}')[0] + '}'

        for child in root.iter(namespace + 'Query'):
            command_element = child.find(namespace + 'CommandText')

            p = str(command_element.text).rpartition(') } DIMENSION')
            final_text = p[0] + text + p[1] + p[2]
            command_element.text = final_text

    @staticmethod
    def add_item(tree):
        root = tree.getroot()
        namespace = str(root.tag).partition('}')[0] + '}'
        items = etree.Element()
        for child in root.find(namespace + 'DataSets').find(namespace + 'DataSet').iter(namespace + 'QueryDefinition'):
            namespace = str(child.tag).partition('}')[0] + '}'
            for i in child.iter(namespace + 'Items'):
                items = i
            break
        item = deepcopy(items.find(namespace + 'Item'))

    @staticmethod
    def add_field(tree):
        root = tree.getroot()
        namespace = str(root.tag).partition('}')[0] + '}'
        fields = root.find(namespace + 'DataSets').find(namespace + 'DataSet').find(namespace + 'Fields')

        field = deepcopy(fields.find(namespace + 'Field'))
        field.set('Name', 'Nas_Vozr')
        data_field = field.find(namespace + 'DataField')
        data_field.text = """<?xml version="1.0" encoding="utf-8"?&gt;&lt;Field xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xsi:type="Level" UniqueName="[Fact].[Nas Vozr].[Nas Vozr]" />"""

        type_name = field.find('{http://schemas.microsoft.com/SQLServer/reporting/reportdesigner}TypeName')
        type_name.text = "System.String"
        fields.append(field)
        # print_all(fields)

    @staticmethod
    def add_nas_vozr_filter(tree, filter_value):
        root = tree.getroot()
        namespace = str(root.tag).partition('}')[0] + '}'

        dataset = root.find(namespace + 'DataSets').find(namespace + 'DataSet')
        f = etree.SubElement(dataset, namespace + 'Filters')
        f.text = '\n'
        f.tail = '\n'
        f = etree.SubElement(f, namespace + 'Filter')
        f.text = '\n'
        f.tail = '\n'
        e = etree.SubElement(f, namespace + 'FilterExpression')
        e.text = '=Fields!Nas_Vozr.Value'
        e.tail = '\n'
        e = etree.SubElement(f, namespace + 'Operator')
        e.text = 'LessThanOrEqual'
        e.tail = '\n'
        e = etree.SubElement(etree.SubElement(f, namespace + 'FilterValues'), namespace + 'FilterValue').text = str(
            filter_value)

    @staticmethod
    def change_text(tree, value):
        root = tree.getroot()
        namespace = str(root.tag).partition('}')[0] + '}'

        for elem in root.iter():
            if elem.text:
                elem.text = elem.text.replace('15 лет и старше', '15-' + str(value) + ' лет')
