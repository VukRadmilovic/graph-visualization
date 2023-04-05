from setuptools import setup, find_packages

setup(
    name="core",
    version="0.1",
    install_requires=['django>=4.0', 'pandas>=1.0'],
    packages=find_packages(),
    package_data={'core': ['static/*.css', 'static/*.js', 'templates/*.html']},
    zip_safe=False
)
