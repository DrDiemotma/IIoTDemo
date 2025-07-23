#!/bin/bash

cd ..

podman build -f ControlNode/Dockerfile -t controlnode:latest .
podman build -f CollectorNode/Dockerfile -t collectornode:latest .
podman builder prune -f
