#!/bin/bash

# Define the required package versions
MECHANICALSOUP_VERSION="1.3.0"
PANDAS_VERSION="1.3.1"
NUMPY_VERSION="1.21.2"
SPACETRACK_VERSION="1.0.1"
SELENIUM_VERSION="4.13"

# Function to check if a package is installed
is_package_installed() {
  python -c "import $1" &>/dev/null
}

# Function to install a package with a specified version
install_package() {
  echo "Installing $1..."
  pip install "$1==$2"
}

# Check and install MechanicalSoup
if ! is_package_installed mechanicalsoup; then
  install_package mechanicalsoup "$MECHANICALSOUP_VERSION"
fi

# Check and install pandas
if ! is_package_installed pandas; then
  install_package pandas "$PANDAS_VERSION"
fi

# Check and install numpy
if ! is_package_installed numpy; then
  install_package numpy "$NUMPY_VERSION"
fi

# Check and install spacetrack
if ! is_package_installed spacetrack; then
  install_package spacetrack "$SPACETRACK_VERSION"
fi

# Check and install selenium
if ! is_package_installed selenium; then
  install_package spacetrack "$SELENIUM_VERSION"
fi

echo "Prerequisites installation completed."
