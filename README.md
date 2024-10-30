# SENSORAIL_Uni_Project

This repository stores all the code for the SENSORAil project taking part at Cardiff University.

## About the project

This project is about making a rail crack detection inspection robot. It will use Acoustic Emission (AE)sensors to send a signal through the rail and another AE sensor to pick up the signal. This will then be processed to find out if there is a crack on that specific portion of rail. The bot will then move a small way down the rail and do the same thing. The idea is that the robot would be left to travel down a rail attempting to find cracks. This data could then be collected by a user to see if any rail sections should be replaced.

## Content In repository

This project will store all of the code related to controlling the robot movement, telemetry collection, single generation and collection, signal processing and the user interface for viewing processed data.

## Developer Guide

We have created an `environment.yml` for our conda environment. Please create this environment and enble it for this project.

We have used the 2024.3 release for the redpitaya board OS and the 'redpitaya_scpi.py' file. This was the most recent versions when this project was started. I cannot see future versions causing conflicts but to mitigate that use the same version as us.