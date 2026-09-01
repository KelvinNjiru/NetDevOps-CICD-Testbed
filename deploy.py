import subprocess
import yaml
from jinja2 import Environment, FileSystemLoader

with open("data.yml") as f:
    data = yaml.safe_load(f)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template.j2")

for router in data["routers"]:
    config = template.render(router)
    print(f"\n{'='*20} Deploying to {router['name']} {'='*20}")
    print(config)

    command = f'docker exec -i {router["name"]} vtysh -c "configure terminal" ' + \
              " ".join([f'-c "{line}"' for line in config.strip().splitlines() if line])
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f" Successfully configured {router['name']}")
    else:
        print(f"❌ Error configuring {router['name']}:\n{result.stderr}")