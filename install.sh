# set install location
cd ~

# automation hat mini setup
curl https://get.pimoroni.com/automationhat | bash

# st7735 install to run display
curl https://get.pimoroni.com/st7735 | bash

# install git
apt-get install git

# install python modules
pip3 install --pre azure-cosmos
pip3 install pyowm

# collect code from git
git clone https://github.com/sambennett04/Ent.git

# set open weather map conf
export OWM_KEY=$1
export LONG=$2
export LAT=$3

# set cosmos db conf
export CDB_URI=$4
export CDB_KEY=$5
export CDB_DATABASE=$6
export CDB_CONTAINER=$7
export CDB_PKEY=$8

# set decision making conf
export RAIN=$9
export WATER_CONTENT=$10
export FERTILIZER_DAY_ONE_NAME=$11
export FERTILIZER_DAY_TWO_NAME=$12

# configure cron job
crontab ~/Ent/crontab

# reboot to materialize configuration
reboot
