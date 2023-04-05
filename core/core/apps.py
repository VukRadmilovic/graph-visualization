import pkg_resources
from django.apps import AppConfig
import os

from core.services.visualizer import Visualizer


class CoreConfig(AppConfig):
    name = 'core'
    parser_plugins = {}
    visualizer_plugins = {}

    unparsed_xml_files = {
        "books": "",
        "items": ""
    }
    parsed_xml_files = {
        "books": None,
        "items": None
    }
    visualized_data = ''
    bird_view = ''
    core_visualizer = None

    def ready(self):

        load_plugins("core.data_parser",self.parser_plugins)
        load_plugins("core.extendable_visualizer",self.visualizer_plugins)
        self.parsed_xml_files["books"] = self.get_parsed_data("books")
        self.parsed_xml_files["items"] = self.get_parsed_data("items")
        self.core_visualizer = Visualizer()

    def get_parsed_data(self, xml_name):
        path = os.path.dirname(__file__)
        path = path[:path.index('\\.venv')] + f'\\core\\core\\data\\{xml_name}.xml'
        with open(path, 'r') as f:
            xml_data = f.read()
        self.unparsed_xml_files[xml_name] = xml_data
        return self.parser_plugins['xml'].parse(xml_data)


def load_plugins(label,dict):
    for ep in pkg_resources.iter_entry_points(group=label):
        p = ep.load()
        plugin = p()
        dict[ep.name] = plugin
