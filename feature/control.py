#!/usr/bin/python3

from flask import Flask, request
import ansible_runner, yaml, os, configparser

class Controller:
    def __init__ (self, useful_data):
        self.data = {**useful_data.pop('labels'), **useful_data.pop('annotations'), **useful_data}
        
    
    def take_action(self):
        if self.data.get("status") == "firing":
            extravars = {}
            r = ansible_runner.run(
                private_data_dir = os.path.join(os.path.dirname(__file__), 'playbook'),
                playbook='playbook.yml',
                tags=self.data['alertname'],
                extravars = {
                    "target": targets.get(self.data['instance'].split(':')[0], None),
                    **self.data
                },
                inventory=inventory_file
                )
        
        elif self.data["status"] == "resolved":
            ip = self.data["instance"].split(":")[0]
            print(
                "\nAlert ({}) from {} has been resolved.\n".format(self.data["alertname"], ip)
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

    myController = Controller(useful_data)

    myController.take_action()
    
    return request.data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)