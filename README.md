
# Automated Telemetry Monitor

## ℹ️ Overview

The Automated Telemetry Monitor is a powerful solution designed to monitor and manage telemetry data efficiently from target nodes. It integrates Prometheus, Grafana, and Alertmanager for data collection, visualization, and alerting.  

With config and playbooks, the project can perform counter-action against the specified alert, achieving immediate control to prevent system failures or any performance degradation.


### The project aims to...
- Gather metrics to support further anaylysis
- Provide a visual way to anaylyse data
- Fire alerts with pre-defined rules with the option of sending via LINE
- Event-driven actions against specific alert

__*The current version supports linux ubuntu system*__  

## 📜 Architecture Overview
![Architecture Overview](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/image/images/architecture.png?raw=true)


## ⏯️ Pre-requisite 

#### __Download ansible for HOST ( 2.10 above )__  

--------- Will be used in configuring and deploying -----------  

install pip:  

~~~
sudo apt install python3-pip:
~~~

install ansible from apt and pip:
~~~
sudo apt install ansible
python3 -m pip install --user ansible
~~~

#### __Download node_exporter and process_exporter for Targets ( via docker )__  

-------- __Installation Image__ ----------- 

~~~
  docker pull prom/node-exporterversion: '3.8'
  docker pull ncabatoff/process-exporter
~~~  

-------- __Configuration__ --------  

~~~
mkdir config
nano config/config.yml
  process_names:
    - name: "{{.Comm}}"
      cmdline:
      - '.+'
~~~

-------- __Docker Compose__ --------  

> __docker-compose.yml__
~~~
nano docker-compose.yml
  version: '3.8'
services:
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    ports:
      - 9100:9100
  process-exporter:
    image: ncabatoff/process-exporter:latest
    container_name: process_exporter
    volumes:
      - /proc:/host/proc:ro
      - ./config:/config:ro
    command:
      - '-procfs=/host/proc'
      - '-config.path=/config/config.yml'
    restart: unless-stopped
    ports:
      - 9256:9256
~~~

> [!NOTE]
> If you want install them in other ways, check out [node_exporter](https://prometheus.io/docs/guides/node-exporter/) and [process_exporter](https://github.com/ncabatoff/process-exporter)


## 🖥️ Install & Deploy
-------- __Installation__ -----------  

Clone the project to your local repo
~~~
git clone https://github.com/TheSKBroook/Automated-Telemetry-Monitor.git
~~~
-------- __Configuration__ -----------  

Add/edit target(s) information in `inventory.ini` in inventory folder:  

> example inventory.ini
~~~INI
[local]
localhost ansible_connection=local ansible_host=130.01.01.2 ansible_become_password=password tocken=

[targets]
target1 ansible_host=130.01.01.3  ansible_user=tester ansible_password=password ansible_become_password=password
~~~

-------- __Deployment__ -----------  

~~~
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory/inventory.ini deploy_playbook.yml
~~~


## How to use


## Demonstration

## License



