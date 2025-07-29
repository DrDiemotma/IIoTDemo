#!/bin/bash

cd ..

podman build -f ControlNode/Dockerfile -t controlnode:latest .
podman build -f CollectorNode/Dockerfile -t collectornode:latest .
podman build -f Ui/Dockerfile -t uiservice:latest .
podman build -f UiNode/Dockerfile -t uinode:latest .
podman builder prune -f
