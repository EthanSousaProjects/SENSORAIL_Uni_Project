# SENSORAIL_Uni_Project

This repository stores all the code for the SENSORAil project taking part at Cardiff University.

## About the project

This project is about making a rail crack detection inspection robot. It will use Acoustic Emission (AE)sensors to send a signal through the rail and another AE sensor to pick up the signal. This will then be processed to find out if there is a crack on that specific portion of rail. The bot will then move a small way down the rail and do the same thing. The idea is that the robot would be left to travel down a rail attempting to find cracks. This data could then be collected by a user to see if any rail sections should be replaced.

## Content In repository

This project will store all of the code related to controlling the robot movement, telemetry collection, single generation and collection, signal processing and the user interface for viewing processed data.

## Developer Guide

We have created an `environment.yml` for our conda environment. Please create this environment and enble it for this project.

We have used the 2024.3 release for the redpitaya board OS and the 'redpitaya_scpi.py' file. This was the most recent versions when this project was started. I cannot see future versions causing conflicts but to mitigate that use the same version as us.

## Raspberry Pi Setup

1) Install the raspberry pi lite OS, setting up a host name, strong password, user name and, activating SSH. Put this on the SD card.

2) Once installed to SD card insert into Pi and connect Via SSH.

3) Make sure everything is up to date using `sudo apt update` and `sudo apt upgrade`.

4) Now install [mini forge](https://conda-forge.org/download/) using SSH. At the time of writing you have to install the installer via curl or wget then run the shell script.
   
   - The commands run were as follows:
   
   - `curl -L -O "https://github.com/condaforge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh"
     `
   
   - `bash Miniforge3-Linux-aarch64.sh`
   
   - Please go onto their page to see if install instructions have changed since writing of this.

5) Clone the main branch of the git repo. This can be done via https via the command `git clone https://github.com/EthanSousaProjects/SENSORAIL_Uni_Project.git`. Check the link is still correct as it may change.

6) Navigate to the environment files folder using `cd` and install the conda environment. [This cheat sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf) is helpful for all conda commands. As of writing if you are in the env folder you can use the command `conda env create -n <env name, typically use pi_conda_env> pi_conda_env --file pi_conda_env.yml`.

7) (the next few commands come from [this tutorial](https://pimylifeup.com/raspberry-pi-wireless-access-point/)).Find the list of WIFI capable devices on your pi (normally the built in one) using the command `iwconfig`. You will see a list of all the network devices available and which ones have wireless capabilities. `wlan0` is normally the built in WIFI chip which is what we will use but other chips you use could be connected.

8) next using the network device name found in step 7 we will run the following command to setup access point mode changing to following to what you want it to be `<DEVICE>` the name in step 7. `<SSID>` Name of the network to broadcast (eg SENSORAIL). `<PASSWORD>` password to connect to WIFI interface eg (V1SENSORAILbot). Command is `sudo nmcli d wifi hotspot ifname <DEVICE> ssid <SSID> password <PASSWORD>`. Eg. `sudo nmcli d wifi hotspot ifname wlan0 ssid SENSORAIL password V1SENSORAILbot`.
   
   - If you get an error relating to wlan0 not being available it is likely the WIFI chip is disabled currently. To enable it you can enter the command `sudo raspi-config`.
   
   - In the menu that appears go into system options
   
   - Then go into wireless LAN settings.
   
   - Select your region. You can connect to a WIFI if you like but it is unnecessary and you can cancel and close it out after you selected your region as the WIFI will now be enabled.
   
   - Rerun the command and it should work and you should see a success message.
   
   - verification can be done using the command `nmcli con show`
   
   - password can be shown via `nmcli dev wifi show-password`

9) (many commands to set this as on boot as well are from [this tutorial](https://www.raspberrypi.com/tutorials/host-a-hotel-wifi-hotspot/)). Get the network UUID using the command `nmcli connection`. In the table besides Hotspot you will see a UUID. Take note of this as you will need it later (eg. a666f4d9-9469-4dbf-a89e-29409e4cdb38).

10) You can see status of your connection through the command `nmcli connection show <UUID from step 9>`. It will give you a ton of properties but the ones we want to know are `connection.autoconnect:` and `connection.autoconnect-priority:` which should be no and 0. We want to change this.

11) To change this, run the command `sudo nmcli connection modify <UUID from step 9> connection.autoconnect yes connection.autoconnect-priority 100`. We have new set the hotspot to boot on launch. You can check the status in step 10 again and it should have changed to yes and 100.

12) Please note that by setting up this hotspot and making sure that it starts up on boot it sets a static IP address for the PI which can be used. Our one set it to `10.42.0.1`.

13) 