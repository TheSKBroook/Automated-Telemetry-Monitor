## Purpose
To convert prometheus rules in excel format into a yaml file and put it to the docker-mounted folder.

## Variable 
    - python_path : A relative path to the converter.py, located at Automated-Telemetru-Monitor/update-rule
        - default: conveter.py

    - SELECT : choose between 'update-rule' and 'deploy-service' depends on where this role is called.
        - default: update-rule

    - clone-to-destination : default true, can be turn off at defaults
        - default: true

## Problem
Couldn't find a good way to find the relative path of gb200_rules.yml, basically hard-code that...