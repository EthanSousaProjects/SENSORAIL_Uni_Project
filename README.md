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

1) Install the raspberry pi lite OS, setting up a strong password and user name and, activating SSH. Put this on the SD card

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