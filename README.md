# NetDevOps CI/CD Testbed 🌐

**Automated BGP Peering Orchestration via Jinja2 & Docker-based FRRouting**

[![NetDevOps CI](https://github.com/KelvinNjiru/NetDevOps-CICD-Testbed/actions/workflows/bgp-ci.yml/badge.svg)](https://github.com/KelvinNjiru/NetDevOps-CICD-Testbed/actions)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FRRouting](https://img.shields.io/badge/Routing%20Engine-FRRouting%20(FRR)-orange.svg)](https://frrouting.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An Infrastructure as Code (IaC) and NetDevOps pipeline that dynamically models, templates, and deploys BGP topologies using containerized routing engines (FRRouting), Jinja2 structured data abstraction, and GitHub Actions continuous integration testing.

---

### ⚡ Architecture & Automation Flow

1. **Data Model (`data.yml`):** Defines interface addressing, AS numbers, and peering definitions in decoupled YAML structures.
2. **Template Engine (`template.j2`):** Parameterized Jinja2 templates generating vendor-compliant routing configurations.
3. **Orchestrator (`deploy.py`):** Automatically renders templates and drives configuration state directly into container runtime shells (`vtysh`).
4. **Automated CI/CD (`bgp-ci.yml`):** Validates whole-topology deployment, daemon lifecycles, and established BGP states on headless GitHub Actions runners.

---

### 🚀 Quick Start

```bash
# 1. Spin up the containerized network fabric
docker compose up -d

# 2. Bootstrap daemons & push configuration
python deploy.py

# 3. Verify peering convergence
docker exec -it r1 vtysh -c "show ip bgp summary"
👤 Author
Kelvin Nyaga Njiru

Network Automation Engineer | NetDevOps Specialist
