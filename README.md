
# Automated Telemetry Monitor

## ℹ️ Overview

Automated Telemetry Monitor can...

(linux ubuntu system)

The project aims to...

## 📜 Architecture Overview
![Architecture Overview](/image/images/architecture.png"Architecture Overview")


## 🧰 Features
- Gather log information to support further anaylysis
- Provide a visual way to anaylyse data
- Send out alert with given rules 
- Fire immediate notification via Line
- Automate actions against specific alert


## ⏯️ Pre-requisite 
#### __Download ansible ( 2.10 above )__  

-------- will be using with config and deploy -----------  

install pip:  

~~~
sudo apt install python3-pip:
~~~

install ansible from apt and pip:
~~~
sudo apt install ansible
python3 -m pip install --user ansible
~~~

## 🖥️ Install & Deploy
-------- __Installation__ -----------  

Clone the project to your local repo
~~~
git clone https://github.com/TheSKBroook/Automated-Telemetry-Monitor.git
~~~
-------- __Configuration__ -----------  

Add/edit target(s) information in `inventory.ini` in inventory folder:  

You can either:
~~~
# Edit in your terminal
nano inventory/inventory.ini
~~~
or  open `inventory.in` in inventory file in text editor

> inventory.ini 

~~~INI
[local]
localhost ansible_connection=local ansible_host= ansible_become_password=

[targets]
target1 ansible_host= ansible_user= ansible_password= ansible_become_password=
target2 ansible_host= ansible_user= ansible_password= ansible_become_password=

# Append more targets with same syntex 
# target3 ansible_host=......
~~~

> example inventory.ini
~~~INI
[local]
localhost ansible_connection=local ansible_host=130.01.01.2 ansible_become_password=password

[targets]
target1 ansible_host=130.01.01.3  ansible_user=tester ansible_password=password ansible_become_password=password
~~~

-------- __Deployment__ -----------  

~~~
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory/inventory.ini deploy_playbook.yml
~~~



### 

--------  -----------  
~~~
nano inventory/inventory.ini

~~~

## How to use


## Demonstration

## License



