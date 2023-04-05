from setuptools import setup, find_packages

setup(
    name="simple_view",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1'],
    entry_points={
        'core.extendable_visualizer':
            ['view_simple=visualizer.simple_view_visualizer:SimpleViewVisualizer'],
    },
    zip_safe=True
)
