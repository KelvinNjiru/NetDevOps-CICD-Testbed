# Automated NetDevOps CI/CD Testbed

[![CI Pipeline](https://github.com/KelvinNjiru/NetDevOps-CICD-Testbed/actions/workflows/bgp-ci.yml/badge.svg)](https://github.com/KelvinNjiru/NetDevOps-CICD-Testbed/actions)
📄 **[Download Master Reference PDF](docs/NetDevOps-CI-CD-Documentation.pdf)**

---

## 1. Executive Summary & Problem Statement
Network configuration drift, manual syntax errors, and untested production pushes remain major operational bottlenecks in traditional network infrastructure management. 

This project implements an automated **NetDevOps CI/CD Testbed** applying **Infrastructure as Code (IaC)** principles to network configuration, deployment, and testing:
* Decouples network state parameters (ASNs, interface IPs, BGP neighbors) into structured YAML data models.
* Uses dynamic **Jinja2** templates and a **Python** orchestration engine (`deploy.py`) to render and inject configurations into containerized **FRRouting (FRR)** instances over an isolated Docker bridge.
* Integrates continuous testing via **GitHub Actions** to spin up virtual nodes on headless cloud runners, assert dynamic **eBGP** peering states (`Established`), and verify **0% packet loss** data plane forwarding on every commit.

---

## 2. Architecture & Tech Stack
* **Virtualization & Routing Fabric:** Docker, Docker Compose, FRRouting (FRR)
* **Programming & Templating:** Python 3, Jinja2, PyYAML
* **Protocols & Standards:** BGP (Border Gateway Protocol / eBGP), TCP/IP, Linux Networking
* **CI/CD & Source Control:** GitHub Actions, Git

---

## 3. Repository File Structure
```plaintext
NetDevOps-CICD-Testbed/
├── .github/
│   └── workflows/
│       └── bgp-ci.yml      # Automated GitHub Actions CI workflow
├── docs/
│   └── NetDevOps-CI-CD-Documentation.pdf # Master technical documentation PDF
├── venv/                   # Python virtual environment
├── data.yml                # Structured network state variables (ASNs, IPs)
├── template.j2             # Jinja2 template for FRR/BGP router configuration
├── deploy.py               # Python orchestration & configuration push engine
├── docker-compose.yml      # Containerized multi-router topology definition
├── .gitignore              # Git ignore rules
└── README.md               # Main project documentation
4. Technical Runbook & Command Reference
Topology & Container Lifecycle
Start Environment: Spawns the isolated virtual bridge network (10.0.0.0/24) and launches router containers (r1, r2) in the background:

Bash
docker compose up -d
Teardown & Clean: Stops and removes running containers, networks, and attached volumes:

Bash
docker compose down -v
Linux & Router Daemon Bootstrapping
Enable BGP Daemon: Enables bgpd inside the FRR container by editing configuration files in place:

Bash
docker exec -i r1 sed -i 's/bgpd=no/bgpd=yes/' /etc/frr/daemons
docker exec -i r2 sed -i 's/bgpd=no/bgpd=yes/' /etc/frr/daemons
Initialize CLI Configuration: Suppresses CLI initialization warnings:

Bash
docker exec -i r1 touch /etc/frr/vtysh.conf
docker exec -i r2 touch /etc/frr/vtysh.conf
Launch BGP Daemons: Starts the routing daemon binaries in background mode:

Bash
docker exec -d r1 /usr/lib/frr/bgpd -d
docker exec -d r2 /usr/lib/frr/bgpd -d
Python Automation Pipeline
Activate Virtual Environment:

Bash
source venv/bin/activate
Execute Deployment Engine: Reads data.yml, renders template.j2, and injects configs into routers:

Bash
python deploy.py
Data Plane & Route Advertisement
Create Dummy Interface: Simulates a local LAN subnet on r1:

Bash
docker exec -it r1 ip link add dummy0 type dummy
docker exec -it r1 ip addr add 192.168.10.1/24 dev dummy0
docker exec -it r1 ip link set dummy0 up
Advertise Prefix via BGP:

Bash
docker exec -it r1 vtysh -c "configure terminal" \
  -c "router bgp 65001" \
  -c "address-family ipv4 unicast" \
  -c "network 192.168.10.0/24"
Verification & Validation
Inspect BGP Peering State:

Bash
docker exec -it r1 vtysh -c "show ip bgp summary"
Verify Route Table Convergence: Confirm r2 learned 192.168.10.0/24 via next-hop 10.0.0.10:

Bash
docker exec -it r2 vtysh -c "show ip route bgp"
Assert End-to-End Data Plane Reachability:

Bash
docker exec -it r2 ping -c 3 192.168.10.1
5. Continuous Integration (GitHub Actions)
The workflow defined in .github/workflows/bgp-ci.yml executes on every push to main:

Checks out the repository and installs Python and Docker dependencies.

Deploys the containerized topology.

Renders and applies configurations using deploy.py.

Executes dynamic assertions verifying the BGP state reaches Established and pings return 0% packet loss.