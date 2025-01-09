
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
![Architecture Overview](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/images/architecture.png)


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

Add/edit target(s) information in `inventory.ini` in deploy-server folder:  

> example inventory.ini
~~~INI
[local]
localhost ansible_host=10.00.00.3 token= ENTER_YOUR_LINE_TOKEN

[targets]
target1 ansible_host= 10.00.00.4
# You can add more targets by:
# target2 ansible_host=
~~~

> [!NOTE]
> Get Line Notify token from logging into [line](https://notify-bot.line.me/en/). More information can be found [here](https://hackmd.io/@sideex/line-notify-zh).  


-------- __Deployment__ -----------  

~~~
cd deploy-server
ansible-playbook -i inventory.ini deploy_playbook.yml -K
~~~


## How to use  

> 💁 After deployment, all the docker will be up. You will be able to monitor your target by going on :
>  -  `localhost:9090` -- prometheus
>  -  `localhost:9093` -- alertmanager
>  -  `localhost:3000` -- grafana
> 

### Adding Rules

You can customized your rules in excel file by either editting or replacing `metrics_excel.xlsx` with your excel file in update-rule folder. 

> [!IMPORTANT]  
> While adding your own rules, please do follow the expect format in the default excel file.  
> The screenshots below show the neccessary column which needs to be filled in. ( A ~ C and M ~ R )

![Excel Screenshot1](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/screenshots/Excel_Screenshot1.png)
![Excel Screenshot2](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/screenshots/Excel_Screenshot2.png)

After add your rules in, remember to update rules into prometheus by running :  

```
cd update-rules
ansible-playbook update-rule.yml -K
```

## Demonstration

## License



