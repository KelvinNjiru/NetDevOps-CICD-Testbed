Plaintext
# Containerized BGP NetDevOps CI/CD Lab

[![NetDevOps BGP CI Testbed](https://github.com/KelvinNjiru/NetDevOps-CICD-Testbed/actions/workflows/bgp-ci.yml/badge.svg)](https://github.com/KelvinNjiru/NetDevOps-CICD-Testbed/actions)
📄 **[Download Full Lab Notes PDF](docs/NetDevOps-CI-CD-Documentation.pdf)**

---

## 1. Project Overview & Motivation
This repository is a hands-on learning testbed built to explore **Network Automation and NetDevOps** practices. 

Instead of configuring routing devices by hand through a manual CLI or heavy GUI simulators, this project applies Infrastructure as Code (IaC) principles. It automates router configuration generation, containerized topology orchestration, and continuous testing through a CI/CD pipeline.

### Core Objectives
* **Data-Driven Configuration:** Decouple environment-specific parameters (ASNs, interfaces, neighbor IPs) from raw syntax using YAML and Jinja2 templates.
* **Programmatic Deployment:** Execute Python scripts to dynamically assemble and inject router configurations into active Linux containers.
* **Automated Network Validation:** Use GitHub Actions to spin up the topology, verify BGP session state, inject test routes, and assert data-plane reachability automatically on code commits.

---

## 2. Lab Architecture & Technologies
* **Routing Engine:** FRRouting (FRR running bgpd and zebra)
* **Virtualization & Environment:** Docker, Docker Compose, Linux virtual network namespaces
* **Automation & Scripting:** Python 3, Jinja2, PyYAML
* **Networking Protocols:** Border Gateway Protocol (eBGP between AS 65001 and AS 65002), TCP/IP (Port 179), ICMP
* **Continuous Integration:** GitHub Actions

---

## 3. Directory Layout

* `.github/workflows/bgp-ci.yml` — Automated CI testing workflow
* `docs/NetDevOps-CI-CD-Documentation.pdf` — Complete reference PDF
* `venv/` — Python virtual environment
* `data.yml` — Lab variables (ASNs, interfaces, neighbors)
* `template.j2` — Jinja2 template for FRR BGP configuration
* `deploy.py` — Python automation script
* `docker-compose.yml` — Multi-router container definitions
* `.gitignore` — Files excluded from git
* `README.md` — Lab overview and runbook

---

## 4. Testbed Runbook & Commands

### Step 1: Launch Container Topology
Start the two FRR router instances (r1 and r2) attached to an isolated Docker bridge network (10.0.0.0/24):

`docker compose up -d`

### Step 2: Initialize Routing Daemons
Enable the BGP routing daemon inside each container and launch the background daemons:

Enable bgpd in FRR daemon configuration
docker exec -i r1 sed -i 's/bgpd=no/bgpd=yes/' /etc/frr/daemons
docker exec -i r2 sed -i 's/bgpd=no/bgpd=yes/' /etc/frr/daemons

Create CLI configuration files
docker exec -i r1 touch /etc/frr/vtysh.conf
docker exec -i r2 touch /etc/frr/vtysh.conf

Start bgpd background daemons
docker exec -d r1 /usr/lib/frr/bgpd -d
docker exec -d r2 /usr/lib/frr/bgpd -d


### Step 3: Run Configuration Automation
Activate the Python virtual environment and run the deployment script to read data.yml, render the Jinja2 template, and push commands via vtysh:

source venv/bin/activate
python deploy.py


### Step 4: Inject Test Prefix on Router 1
Create a virtual dummy interface on r1 to simulate a connected local subnet (192.168.10.0/24), then advertise the prefix via BGP:

Create dummy interface with IP
docker exec -it r1 ip link add dummy0 type dummy
docker exec -it r1 ip addr add 192.168.10.1/24 dev dummy0
docker exec -it r1 ip link set dummy0 up

Advertise subnet into BGP
docker exec -it r1 vtysh -c "configure terminal"

-c "router bgp 65001"

-c "address-family ipv4 unicast"

-c "network 192.168.10.0/24"


---

## 5. Verification & Testing

### 1. Check BGP Control Plane Session
Verify that the eBGP session between r1 (10.0.0.10) and r2 (10.0.0.20) reaches the Established state:

`docker exec -it r1 vtysh -c "show ip bgp summary"`

### 2. Verify Route Table Convergence
Verify that r2 has learned the 192.168.10.0/24 network via BGP next-hop 10.0.0.10:

`docker exec -it r2 vtysh -c "show ip route bgp"`

### 3. Test End-to-End Data Plane Reachability
Send ICMP echo requests from r2 across the transit link to the simulated LAN interface on r1:

`docker exec -it r2 ping -c 3 192.168.10.1`

---

## 6. Continuous Integration Workflow
The GitHub Actions workflow (.github/workflows/bgp-ci.yml) runs automatically on every code push:

* Spawns an Ubuntu runner and deploys the container topology using Docker Compose.
* Executes deploy.py to generate and apply configurations dynamically.
* Automatically validates control-plane peering status (Established).
* Injects the test prefix and asserts data plane reachability with 0% packet loss.
