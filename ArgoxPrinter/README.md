Code to setup thermal printer on Raspbian OS

first, we need to enable serial port on Raspbian OS (Raspberry pi Configuration)
second, connect USB termal printer to Raspbian OS. Type ls /dev/*
third, sudo chmod 666 /dev/usb/lp0 to set permission
fourth, try echo -e "This is a test message.\n\n" > /dev/usb/lp0 to first time print
fifth, install library sudo pip3 install python-escpos
