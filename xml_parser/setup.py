from setuptools import setup, find_packages

setup(
    name="xml_parser",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1'],
    entry_points={
        'core.data_parser':
            ['xml=parser.xml_parser:XMLParser'],
    },
    zip_safe=True
)
