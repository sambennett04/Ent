# usb off
echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind

# hdmi off
sudo /opt/vc/bin/tvservice -o
