# IIoT Demo

This project demonstrates a modular industrial internet of thigns (IIoT) setup.
t is meant for educational purposes only, not for productive use.
Use it at your own risk!

!!WARNING!! Early stage. Not all features are working.

The structure is divided in two different sub-projects.
Core of the project is the DataCollectorDemo.
The DataSourceDemo is for demonstration purposes of the collector only if no other source is available.
This setup demonstrates a way how a single software can stay flexible in order to adapt to different machines.
Likewise, features can be adapted and unified in order to create new functionality within the same platform.

## Getting Started

To download the project, use the following command: `git clone git@github.com:DrDiemotma/IIoTDemo.git`

## Installation

The project is based on dockerfiles, tested with Podman.
You might use Docker as well.
To install the services, for the client, you have three options:

- Using Podman Compose with the provided docker-compose.yml file. Currently, untested.
- Using the script make/make_services.sh.
- Using `podman build -t <image_name> -f Dockerfile .` in the respective server directory.

If you want to install the services individually, you have to be aware that
there are dependencies between them.
For example, all services depend on the ControlNode which always has to be
installed and started first.

## Starting the Services

We recommend using the Podman Desktop application to control the services.
For demonstration, this provides the best overview of the services installed.
Please see the manuals for that software on how to work with the services.

### Ports

- ControlNode: 8000
- UiNode: 8012
- Ui: 8501
- CollectorNode: 8001

OPC UA is usually working on port 4840.

## UI

The UI is a web application that provides some overview of the services running.
You can access them via the web browser at `http://localhost:8501`.
In order to have access to the services, the UiNode must be running as well.

## Architecture

![Data and command transfe of the DataCollectorDemo](Images/[OAB]%20Sending%20Command.png)

The architecture of the DataCollectorDemo consists of several components:

- ControlNode: The ControlNode is responsible for managing the overall system
and coordinating the communication between the other components.
- UiNode: The UiNode provides a controls and services for the UI.
- Ui: The Ui is a web application that provides some overview of the services running.
- CollectorNode: The CollectorNode is responsible for collecting data from OPC UA.

### Initialization

![Initialization](Images/[OAB]%20Edge%20Initialization.png)

All services register at the start procedure in the ControlNode.
They do not perform a communication between each other.
An exception is the UI which requires the UiNode to be running.

### OPC UA Connection

![OPC UA Connection](Images/[OAB]%20Activities%20for%20Data%20Receiving.png)

OPC UA initialization is so far without any security measures.
In a future build, we will add support for certificate-based authentication.
User and password authentification is not planned, as this is supposed to be a
demo for machine-to-machine communication.
