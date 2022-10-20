#!/bin/bash
# Description: This script will install all the dependencies and run the frontend app

# change directory to the ./frontend
cd ./frontend

# check if node is installed
if ! [ -x "$(command -v node)" ]; then
    echo 'Error: node is not installed.' >&2

    # install node
    sudo apt-get install node -y
fi

# check if yarn is installed
if ! [ -x "$(command -v yarn)" ]; then
    echo 'Error: yarn is not installed.' >&2

    # install yarn
    sudo apt-get install yarn -y
fi

# install dependencies
yarn install

# build the app
yarn build

# preview the app
yarn preview
