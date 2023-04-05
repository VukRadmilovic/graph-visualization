#!/bin/bash

# This script is used to clean unnecessary generated files/folders.

remove_eggs() {
  # The directory path is sent as the first argument
  cd $1
  rm -rf build
  rm -rf *.egg-info
  rm -rf dist
  cd ..
}

# remove build files from components
remove_eggs core
remove_eggs xml_parser
remove_eggs simple_view
remove_eggs complex_view

# remove db
cd django_project
rm *.sqlite3
cd ..
