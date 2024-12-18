#!/usr/bin/python3

from flask import Flask, request
import ansible_runner, yaml, os, configparser

inventory_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'inventory', 'inventory.ini')

app = Flask(__name__)

config = configparser.ConfigParser()
config.read(inventory_file)

targets = {}
for target in config['targets']:
    ansible_host = config['targets'][target].split(' ')[0]
    targets[ansible_host] = target.split(' ')[0]

@app.route("/webhookcallback", methods=["POST"])

def hook():
    yaml_data = yaml.safe_load(request.data.decode('utf-8'))


    useful_data = {
        **yaml_data.get("alerts")[0]
    }


    if useful_data.get("status") == "firing":
        extravars = {}
        r = ansible_runner.run(
            private_data_dir = os.path.join(os.path.dirname(__file__), 'playbook'),
            playbook='playbook.yml',
            tags=useful_data['labels']['alertname'],            
            extravars = {
                "COMPUTE_NODE": targets.get(useful_data['labels']['instance'].split(':')[0], None),
                "PROCESS_NAME": useful_data['labels'].get('groupname', None)
            },
            inventory=inventory_file
            )

    elif useful_data.get("status") == "resolved":
        ip = useful_data['labels']["instance"].split(":")[0]
        print(
            "\nAlert ({}) from {} has been resolved.\n".format(
                useful_data["labels"].get("alertname"), ip
            )
        )
    return request.data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)