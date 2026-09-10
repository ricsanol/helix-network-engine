# Helix Network Engine

Helix Network Engine is a Python portfolio project for transforming structured network-service data into vendor-specific configuration workflows with validation and pre-check stages.

> **Public portfolio edition:** all inventories, hostnames, IP addresses, identifiers and credentials included here are fictitious lab examples.

## What it demonstrates

- Structured Excel input and model validation
- Multi-vendor configuration rendering with Jinja2
- Cisco and Huawei workflow components
- SSH pre-check architecture using Netmiko
- Pipeline decisions for approved/blocked configuration generation
- Separation between input, domain models, validation, templates and generated output
- Environment-based credential handling

## Project structure

```text
helix_network_engine/
├── data/                 # Fictitious lab spreadsheets
├── helix/
│   ├── core/             # Pipeline, decisions, settings and orchestration
│   ├── input/            # Excel readers and mappers
│   ├── models/           # Domain/data models
│   ├── precheck/         # Clients, commands, validators and reports
│   └── templates/        # Rendering helpers
├── templates/
│   ├── cisco/            # IOS / IOS XR Jinja templates
│   └── huawei/           # VRP Jinja templates
├── .env.example
├── main.py
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and replace the placeholder values only in your local environment. The `.env` file is ignored by Git.

## Run

```bash
python main.py
```

The included spreadsheets are intentionally fictitious. Running the full pre-check against them will not connect to real devices. For a real lab, supply your own local inventory and credentials without committing them.

## Security and publication

The public repository intentionally excludes IDE metadata, Python bytecode/cache, runtime logs, reports, generated configuration output and real operational data. See `SECURITY.md`.

## License

No open-source license is granted at this time. This repository is published for portfolio and demonstration purposes.
