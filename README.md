# OSAwards: Visualization Tool for OS projects

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This README provides an overview of the Visualization Tool within OSAwards project.

It is handled by Tecnalia and part of WP3, Task number T3.4.

## Introduction

The Visualization Tool consists of a solution mainly intended for anyone interested in OS indicators (students, journalists, scientists…). Its design makes it possible to offer:

- A mean for consulting metrics about Open-Source projects, fed by the outcomes of WP3 tasks and other external data sources.

- A space for publishing successful stories about projects, actors, companies...

- Interaction with the defined indicators and metrics using chart elements.

- Support to the nomination process for the Awards.

- Provide support (if needed) for articles and publications on the EOSA website.

The information is presented primarily through interactive dashboards, thereby enabling analysis and visualization of the critical areas. To build those dashboards, a multi-component framework has been developed, providing support to all integration, storage, and visualization requirements.

Finally, it is important to highlight that the Visualization Tool complies with privacy laws and regulations. As the tool is accessible to the general public, no personal data is used or displayed.

---

## Getting started

### System requirements

The recommended system requirements are as follows:

| Requirement      | Value                     |
| ---------------- | ------------------------- |
| RAM Memory       | 8 GB                      |
| Disk size        | 100 GB                    |
| Number of CPUs   | 4                         |
| Operative System | Linux Ubuntu 24.04 Server |

All the components of the Visualization Tool are dockerized, and Docker Compose has been selected as the orchestration mechanism. So, it is necessary to ensure that the following software is installed:

| Feature        | Version             |
| -------------- | ------------------- |
| Docker Engine  | 28.0.0 (2025-02-19) |
| Docker Compose | 2.33.0              |

And to carry out new developments or modify existing code:

| Feature | Version |
| ------- | ------- |
| Python  | 3.12    |
| Poetry  | 1.8.2   |

### Installation

Clone the repository in the desired directory:

```
cd directory
git clone https://github.com/osawardsTecnalia/visualizationtool.git
```

### Deployment

There is a series of environment files located in the root directory. Before deployment, and if considered necessary, edit each of them to change usernames, passwords, ports... and other configuration variables. The following table establishes the relationship between the files and the configurable properties:

| Environment file   | Properties to be configured                                                                                                                                                                                                      |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| .env-datacollector | --                                                                                                                                                                                                                               |
| .env-elasticsearch | ES_PORT                                                                                                                                                                                                                          |
| .env-framework     | FRAMEWORK_TRAEFIK_HOST                                                                                                                                                                                                           |
| .env-gateway       | GATEWAY_API_KEY_HASHED<br>GATEWAY_GROUPNAME    (for SFTP Server)<br>GATEWAY_PORT    (for SFTP Server)<br>GATEWAY_USERNAME    (for SFTP Server)<br>GATEWAY_PASSWORD    (for SFTP Server)<br>GATEWAY_HELLO<br>GATEWAY_TRAEFIK_HOST |
| .env-kibiter       | KIBITER_PORT<br>KIBITER_STATUS<br>KIBITER_TRAEFIK_HOST                                                                                                                                                                           |
| .env-portainer     | PORTAINER_PASSWORD                                                                                                                                                                                                               |
| .env-sftp          | SFTP_GROUPNAME<br>SFTP_PORT<br>SFTP_USERNAME<br>SFTP_PASSWORD                                                                                                                                                                    |
| .env-traefik       | TRAEFIK_EMAIL                                                                                                                                                                                                                    |

Since Docker Compose was chosen as the orchestration system, there is also a *compose.yaml* file in the root directory. This file defines all microservices, volumes, and the internal Docker network. In principle, no modifications are necessary, as the configurations are located in the environment files; however, the file can be edited to adjust settings as considered necessary.

The final step is to carry out the deployment. To do this, enter the command in a terminal:

```
bash deploy.sh
```

To verify that everything is correctly deployed:

- **Gateway API:**       https://<*VT_host*>/osawards/api/v1/documentation

- **GrimoireLab:**       https://<*VT_host*>

- **User Interface:**    https://<*VT_host*>/framework

---

## License

The project is licensed under the Apache 2.0 license.

---

## Version

The current version of the Visualization Tool is **0.9.0** (view [this file](VERSION)).

---

## Documentation

- To view the documentation for the Visualization Tool Modules, access [here](docs/modules/README.md).

- To review the Administrator Manual, access [here](docs/admin_manual/README.md).

- To review the User Manual, access [here](docs/user_manual/README.md).

- To view some examples scenarios) of Use Cases, access [here](docs/use_cases/README.md).
