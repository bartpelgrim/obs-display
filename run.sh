#!/bin/bash

docker run -p 4000:5000 -v $PWD/data:/build/data obs-display
