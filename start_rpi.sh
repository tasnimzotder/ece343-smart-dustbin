# Description: This script will install all the dependencies and run the app

# change directory to the ./rpi
cd ./rpi

# check if python3 is installed
if ! [ -x "$(command -v python3)" ]; then
    echo 'Error: python3 is not installed.' >&2

    # install python3
    sudo apt-get install python3 -y
fi

# check if pip3 is installed
if ! [ -x "$(command -v pip3)" ]; then
    echo 'Error: pip3 is not installed.' >&2

    # install pip3
    sudo apt-get install python3-pip -y
fi

# check if virtualenv is installed
if ! [ -x "$(command -v virtualenv)" ]; then
    echo 'Error: virtualenv is not installed.' >&2

    # install virtualenv
    sudo pip3 install virtualenv
fi

# create virtual environment
virtualenv venv

# activate virtual environment
source venv/bin/activate

# install requirements
pip3 install -r requirements.txt

# run the app
python3 main.py
