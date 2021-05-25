
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
  * [Steps to install additional python libraries](#Steps-to-install-additional-python-libraries)
* [Usage](#usage)
* [Contributors](#contributors)

<!-- ABOUT THE PROJECT -->
## About The Project

This project is intended to build and deploy a human tracking application onto Qualcomm Robotics development Kit (RB5) that identifies the person by face recognition.

The application consists of 2 parts: A webserver and an MQTT client.
Web Server is responsible for storing the faces in RB5. It waits for POST Request from client. 

API Info:
Request Type: POST
Endpoint name: /add_face
Image can be included as multipart form data with field name as “image”
Eg. (HTML Form) <input type=”file” name=”image”>


MQTT Client subscribes to topic “track” and expects the name of the person as payload. You can test it using Mosquitto clients by entering the following command:
```sh
mosquitto_pub -m "<name of the person to track>" -t "track"
```

Once a name is published to “track” topic, RB5 will initiate the tracking process for a particular person. Once the person is identified, RB5 will publish the tracked information to the topic “tracked” with payload containing following information:
{
        “name”: <name of the tracked person>,
        “score” : <value indicating the variance between predicted person and face it got as input>,
        “location”: <location of the person in the field of view>
}


## Prerequisites

1. A Linux workstation with Ubuntu 18.04.

2. Install Android Platform tools (ADB, Fastboot) 

3. Download and install the SDK [Manager](https://developer.qualcomm.com/qualcomm-robotics-rb5-kit/quick-start-guide/qualcomm_robotics_rb5_development_kit_bring_up/download-and-install-the-SDK-manager)

4. [Flash](https://developer.qualcomm.com/qualcomm-robotics-rb5-kit/quick-start-guide/qualcomm_robotics_rb5_development_kit_bring_up/flash-images) the RB5 firmware image on to the board

5. Setup the [Network](https://developer.qualcomm.com/qualcomm-robotics-rb5-kit/quick-start-guide/qualcomm_robotics_rb5_development_kit_bring_up/set-up-network) 


6. Setup the [Pybind11](https://pybind11.readthedocs.io/en/stable/installing.html).

7. Setup opencv for python on RB5

8. Turtlebot burger is assembled, operational and is connected to RB3

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.
1. Clone the  project repository from the github to RB5.
```sh
git clone 
```


### Steps to install additional python libraries

1.Install pybind11
```sh
python3.5 -m pip install pybind11
```
2. Install opencv for python
```sh
python3.5 -m pip install opencv-python
```
3. Install Flask
```sh
python3.4 -m pip install Flask
```
4. Setup mosquitto Broker
```sh
sudo apt-get update
sudo apt-get install mosquitto
```
Test the broker by installing mosquitto client
```sh
sudo apt-get install mosquitto-clients
```
Now subscribe to test topic publish to that topic and check whether subscriber got the message
```sh
mosquitto_sub -t "test"
mosquitto_pub -m "message from publisher" -t "test"
```

<!-- USAGE -->
## Usage

Follow the below steps for initializing the application:

1. Start the web server
```sh
python3.5 server.py

```
2. Start the MQTT client for tracking:
```sh
python3.5 main.py
```

<!-- ## Contributors -->
## Contributors
* [Rakesh Sankar](s.rakesh@globaledgesoft.com)
* [Steven P](ss.pandiri@globaledgesoft.com)
* [Ashish Tiwari](t.ashish@globaledgesoft.com)
* [Arunraj A P](ap.arunraj@globaledgesoft.com)






