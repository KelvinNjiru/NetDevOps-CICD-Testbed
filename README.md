# Containerized BGP NetDevOps CI/CD Lab

[![NetDevOps BGP CI Testbed](https://github.com/KelvinNjiru/NetDevOps-CICD-Testbed/actions/workflows/bgp-ci.yml/badge.svg)](https://github.com/KelvinNjiru/NetDevOps-CICD-Testbed/actions)
📄 **[Download Project PDF Reference](docs/NetDevOps-CI-CD-Documentation.pdf)**

---

## 1. Project Overview & Motivation
This is a hands-on learning lab designed to explore **NetDevOps and Network Automation** fundamentals. Instead of relying on manual CLI configuration or heavy GUI network emulators, this testbed sets up a lightweight, containerized routing environment to practice Infrastructure as Code (IaC) workflows.

### What This Testbed Demonstrates
* **Data & Template Separation:** Router variables (Autonomous System Numbers, IP addresses, BGP neighbor relationships) are defined in structured YAML (`data.yml`).
* **Automated Config Injection:** A Python script (`deploy.py`) uses Jinja2 (`template.j2`) to dynamically render FRRouting (FRR) configs and inject them into isolated Docker containers via the Linux CLI.
* **Automated CI Validation:** A GitHub Actions workflow spins up the Docker topology inside a headless Linux runner, deploys the configs, and runs automated assertions to verify dynamic eBGP peering and end-to-end data plane reachability.

---

## 2. Lab Architecture & Technologies
* **Routing Daemon & Containers:** FRRouting (FRR), Docker, Docker Compose
* **Automation & Scripting:** Python 3, Jinja2, PyYAML
* **Networking Concepts:** eBGP (AS 65001 to AS 65002), TCP/IP (Port 179), Linux virtual interfaces (`dummy0`), ICMP testing
* **CI/CD:** GitHub Actions

---

## 3. Directory Layout

```plaintext
NetDevOps-CICD-Testbed/
├── .github/
│   └── workflows/
│       └── bgp-ci.yml      # CI workflow running automated checks
├── docs/
│   └── NetDevOps-CI-CD-Documentation.pdf # Exported lab documentation
├── venv/                   # Local Python virtual environment
├── data.yml                # Lab variables (ASNs, interfaces, neighbors)
├── template.j2             # Jinja2 template for FRR BGP configuration
├── deploy.py               # Python automation script
├── docker-compose.yml      # Docker network and router container definitions
├── .gitignore              # Files excluded from git
└── README.md               # Lab overview and runbook
4. Step-by-Step Lab Runbook
Step 1: Spin Up the Virtual Router Topology
Start the two FRR router containers (r1 and r2) connected over a private Docker bridge network (10.0.0.0/24):

Bash
docker compose up -d
Step 2: Bootstrap FRR Daemons
Enable the BGP routing daemon inside each container and start the background processes:

Bash
# Enable bgpd
docker exec -i r1 sed -i 's/bgpd=no/bgpd=yes/' /etc/frr/daemons
docker exec -i r2 sed -i 's/bgpd=no/bgpd=yes/' /etc/frr/daemons

# Initialize vtysh config
docker exec -i r1 touch /etc/frr/vtysh.conf
docker exec -i r2 touch /etc/frr/vtysh.conf

# Start bgpd process
docker exec -d r1 /usr/lib/frr/bgpd -d
docker exec -d r2 /usr/lib/frr/bgpd -d
Step 3: Run the Automation Script
Activate the Python virtual environment and run the deployment script to render and push configs:

Bash
source venv/bin/activate
python deploy.py
Step 4: Inject a Test Prefix on R1
Simulate a local LAN network attached to r1 using a Linux dummy interface, then advertise the subnet into BGP:

Bash
# Create dummy interface with test IP
docker exec -it r1 ip link add dummy0 type dummy
docker exec -it r1 ip addr add 192.168.10.1/24 dev dummy0
docker exec -it r1 ip link set dummy0 up

# Advertise route into BGP
docker exec -it r1 vtysh -c "configure terminal" \
  -c "router bgp 65001" \
  -c "address-family ipv4 unicast" \
  -c "network 192.168.10.0/24"
5. Verification & Testing
1. Control Plane Peering Check
Verify that the eBGP session between r1 (10.0.0.10) and r2 (10.0.0.20) reaches the Established state:

Bash
docker exec -it r1 vtysh -c "show ip bgp summary"
2. Routing Table Check
Verify that r2 learned the advertised 192.168.10.0/24 subnet via next-hop 10.0.0.10:

Bash
docker exec -it r2 vtysh -c "show ip route bgp"
3. Data Plane Reachability Test
Assert that r2 can successfully forward ICMP packets to the simulated subnet on r1:

Bash
docker exec -it r2 ping -c 3 192.168.10.1
6. Continuous Integration (CI) Workflow
The GitHub Actions workflow (.github/workflows/bgp-ci.yml) replicates the manual steps above automatically on every commit:

Provisions the Ubuntu runner and launches the Docker Compose environment.

Executes deploy.py to configure both routers.

Automatically queries vtysh to assert that BGP peering is established.

Injects the test route and asserts 0% packet loss via ping checks.
