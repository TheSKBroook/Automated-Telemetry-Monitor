#!/usr/bin/python3

from flask import Flask, request
import ansible_runner, yaml, os, configparser


def take_action(useful_data):
    data = {**useful_data.pop('labels'), **useful_data.pop('annotations'), **useful_data}

    if data.get("status") == "firing":
        extravars = {}
        r = ansible_runner.run(
            private_data_dir = os.path.join(os.path.dirname(__file__), 'playbook'),
            playbook='test.yml',
            tags=data['alertname'],
            extravars = {
                "target": targets.get(data['instance'].split(':')[0], None),
                **data
            },
            inventory=inventory_file
        )
    
    elif data["status"] == "resolved":
        ip = data["instance"].split(":")[0]
        print(
            "\nAlert ({}) from {} has been resolved.\n".format(data["alertname"], ip)
        )

inventory_file = os.path.abspath('inventory.ini')

config = configparser.ConfigParser()
config.read(inventory_file)

targets = {}
for target in config['targets']:
    ansible_host = config['targets'][target].split(' ')[0]
    targets[ansible_host] = target.split(' ')[0]

app = Flask(__name__)

@app.route("/webhookcallback", methods=["POST"])

def hook():
    
    yaml_data = yaml.safe_load(request.data.decode('utf-8'))

    useful_data = {**yaml_data.get("alerts")[0]}

    take_action(useful_data)

    return request.data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)