#!/bin/bash

set -eux

# if [ "$EUID" -ne 0 ]
#   then echo "Please run as root"
#   exit
# fi

sudo apt-get install wine-stable

wine LTspice64.exe
rm LTspice64.exe

if ! [ -f LTspice64.exe ]; then
  wget https://ltspice.analog.com/software/LTspice64.exe
fi

wine LTspice64.exe
