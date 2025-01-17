<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/images/icon.png">
    <img src="https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/images/icon.png" alt="Icon" width="150" height="150">
  </a>

  <h2 align="center">Automated Telemetry Monitor</h2>
  <p align="center">
    A smart monitor transforming telemetry data into actions and real-time alerts!
    <br />
    <br />
    <a href="https://github.com/TheSKBroook/Automated-Telemetry-Monitor"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#demostration">View Demo</a>
    &middot;
    <a href="https://github.com/TheSKBroook/Automated-Telemetry-Monitor/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/TheSKBroook/Automated-Telemetry-Monitor/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#About-this-project ">About this project</a>
    </li>
    <li>
      <a href="#Architecture-Overview">Architecture Overview</a>
    </li>
    <li><a href="#How-to-use">How to use</a></li>
      <ul>
        <li><a href="#Adding-Rules">Adding Rules</a></li>
        <li><a href="#Adding-Action-Playbook">Adding Action Playbook</a></li>
      </ul>
    <li><a href="#Pre-requisite">Pre-requisite, Install and Deploy</a></li>
    <li><a href="#Demonstration">Demonstration</a></li>
    <li><a href="#License">License</a></li>
  </ol>
</details>

## About this project 

The Automated Telemetry Monitor is a powerful solution designed to monitor and manage telemetry data efficiently from target nodes. It integrates Prometheus, Grafana, and Alertmanager for data collection, visualization, and alerting.  

With config and playbooks, the project can perform counter-action against the specified alert, achieving immediate control to prevent system failures or any performance degradation.


### The project aims to...
- Gather metrics to support further anaylysis
- Provide a visual way to anaylyse data
- Fire alerts with pre-defined rules with the option of sending via LINE
- Event-driven actions against specific alert

__*The current version supports linux ubuntu system*__  

> [!Warning]
> __*Unfortunately, LINE Notify will end on March 31, 2025. We will be looking for alternative solutions to replace its functionality.*__


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Architecture Overview
<div align="center">
  <img src="https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/images/architecture.png">
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How to use  

> 💁 After deployment, all Docker containers will be running. You will be able to monitor your target by navigating to :
>  -  `localhost:9090` -- prometheus
>  -  `localhost:9093` -- alertmanager
>  -  `localhost:3000` -- grafana
> 

### Adding Rules

You can customize your rules in an Excel file by either editing or replacing `metrics_excel.xlsx` with your own file in the `update` folder.  

> [!IMPORTANT]  
> While adding your own rules, please follow the expected format in the default Excel file.
>  - Blue section are required to be filled in. ( A and B and M ~ R )
>  - Enter `Y` or `N` in `Enable` section to enable rules.
>  - To create both Warning and Critical severity rules, separating them with a new line, and apply the same approach to the expressions.

![Excel Screenshot](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/screenshots/Excel_Screenshot1.png)
![Excel Screenshot](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/screenshots/Excel_Screenshot2.png)

After adding your rules, remember to update them in Prometheus by running:  

```shell
cd update
ansible-playbook update-rule.yml -K
```

### Adding Action Playbook

Feel free to add your own playbook in `handle_alert.yml` in `update` folder for event-driven actions.  
Here is an easy template for you to follow :

```yaml
- name: NAME_OF_YOUR_PLAY
  hosts: "{{ target }}"
  tags: ALERT_NAME + _Warning or _Critical
  tasks:
    - name: TASK_NAME
      # ... write your tasks here ..
```
> [!NOTE]  
> __The variables listed below are included in the default request that Alertmanager sends to the webhook server.__  
>
> __general__ : `status`, `alertname`, `instance`, `severity`, `description`, `summary`, `startsAt`, `endsAt`, `generatorURL`, `fingerprint`  
> __extra__ :  `job` ( _node-exporter_ ), `groupname` ( _process-exporter_ )
>  
> Any other variables will need to be parsed from `extravars` in `webhook.py`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Pre-requisite 

<details>
<summary><b>Download ansible for HOST ( 2.10 above )</b></summary>
<hr>
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

</details>

<details>
<summary><b>Download node_exporter and process_exporter for Targets ( via docker )</b></summary>
<hr>

💁 _If you want to install them in another way, check out [node_exporter](https://prometheus.io/docs/guides/node-exporter/) and [process_exporter](https://github.com/ncabatoff/process-exporter)_

<hr>

-------- __Installation Image__ ----------- 

~~~shell
  docker pull prom/node-exporterversion: '3.8'
  docker pull ncabatoff/process-exporter
~~~  

-------- __Configuration__ --------  

~~~shell
mkdir config
nano config/config.yml
  process_names:
    - name: "{{.Comm}}"
      cmdline:
      - '.+'
~~~

-------- __Docker Compose__ --------  

> __docker-compose.yml__
~~~yaml
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
</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🖥️ Install & Deploy
<div align="center">
  <h2 align="center" style="font-weight: bold">Flow Chart</h2>
  <img src="https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/images/deployment_chart.png" width="750" height="1000">
</div>

-------- __Installation__ -----------  

Clone the project to your local repo
~~~shell
git clone https://github.com/TheSKBroook/Automated-Telemetry-Monitor.git
~~~
-------- __Configuration__ -----------  

Add or edit target information in `inventory.ini` located in the `deploy-server` folder:  

> example inventory.ini
~~~INI
[local]
localhost ansible_host=10.00.00.3 ansible_user=test token= ENTER_YOUR_LINE_TOKEN

[targets]
target1 ansible_host= 10.00.00.4 ansible_user=test
# You can add more targets by:
# target2 ansible_host=
~~~

> [!NOTE]
> Get Line Notify token from [Line](https://notify-bot.line.me/en/). More information can be found [here](https://hackmd.io/@sideex/line-notify-zh).  


-------- __Deployment__ -----------  

In deploy_server directory :    
~~~shell
ansible-playbook -i inventory.ini main.yml -K
~~~

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a id="demostration"></a>

## Demonstration  

<div align="center">

Take a look at these screenshots to see it in action!

### Prometheus
![Prometheus](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/screenshots/prometheus.png?raw=true)  

__Query and explore your telemetry metrics in real time with Prometheus.__
<hr>

### Grafana
![Grafana](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/screenshots/grafana.png)  

__Visualize your data with customizable dashboards in Grafana.__
<hr>

### Alertmanager
![Alertmanager](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/screenshots/alertmanager.png)  

__Manage and view alert notifications efficiently with Alertmanager.__
<hr>

### Line Notify
![Line](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/github-image/screenshots/Line.png)  

__Receive instant alerts on your LINE app for critical events.__

</div>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/TheSKBroook/Automated-Telemetry-Monitor/blob/main/LICENSE) file for more details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
