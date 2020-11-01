:'
    description
    -----------
    - install script for the Ent project and all of its dependencies

    instructions
    ------------
    - run as root with the following command: sudo bash install.sh
'

# install git
apt-get install git

# install python dependencies
pip3 install --pre azure-cosmos
pip3 install wiringpi
pip3 install darksky_weather

# make download directory
mkdir ent
cd ent

# install ent
git clone https://github.com/sambennett04/Ent.git

# install megaio dependencies
git clone https://github.com/SequentMicrosystems/megaio-rpi.git 
cd ./megaio-rpi
sudo make install 
cd ./python/megaio
python3 setup.py install