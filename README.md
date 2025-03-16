# KMS Server

Microsoft Windows/Office KMS Local Activation Server

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Docker Image Version](https://img.shields.io/docker/v/oopsunix/kms)
![Docker Image Size](https://img.shields.io/docker/image-size/oopsunix/kms?color=0eb305)
![Docker Pulls](https://img.shields.io/docker/pulls/oopsunix/kms?color=7842f5)
***

<p>
  English | <a href="./README-zh.md">中文</a>
</p>

## 🌟 Supported products
- Responds to `v4`, `v5`, and `v6` KMS requests.
- Supports activating following versions of Windows Server:
	- Windows Server 2008
	- Windows Server 2008 R2
	- Windows Server 2012
	- Windows Server 2012 R2
	- Windows Server 2016
	- Windows Server 2019
	- Windows Server 2022
	- Windows Server 2025
- Supports activating following Volume Licensing versions of Windows:
	- Windows Vista
	- Windows 7
	- Windows 8
	- Windows 8.1
	- Windows 10
    - Windows 11
- Supports activating following Volume Licensing versions of Office:
	- Microsoft Office 2010
	- Microsoft Office 2013
	- Microsoft Office 2016
	- Microsoft Office 2019
	- Microsoft Office 2021
	- Microsoft Office LTSC 2021
	- Microsoft Office LTSC 2024

## 📦 Deployment

### Docker Compose Deployment

```yaml
services:
  kms:
    image: "oopsunix/kms:latest"
    # image: "ghcr.io/oopsunix/kms:latest" # GitHub Container Registry
    container_name: "kms"
    restart: "always"
    ports:
      - "1688:1688" # KMS service port
      - "8080:8080" # Web UI port (optional)
    environment:
      - WEBUI=1     # Enable Web UI (default is 0 to disable)

```

### Environment Variables

| Parameter | Value | Default |
| --------- | ----- | ------- |
| `TZ` | [Time Zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) | Asia/Shanghai |
| `DEBUG` | Will activate debug option for container image and app (if available) | |
| `KMS_LOCALE` | see Microsoft LICD specification | 1033 (en-US) |
| `KMS_CLIENTCOUNT` | client count > 25 | 26 |
| `KMS_ACTIVATIONINTERVAL` | Retry unsuccessful after N minutes | 120 (2 hours) |
| `KMS_RENEWALINTERVAL` | re-activation after N minutes | 129600 (90 days) |
| `KMS_LOGLEVEL` | CRITICAL, ERROR, WARNING, INFO, DEBUG, MININFO | INFO |

## ❤️ Thanks

* [py-kms](https://github.com/Py-KMS-Organization/py-kms)

## 🤝 Contributions

Welcome to contribute code or suggestions!

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This project is for learning and research purposes only. Please do not use it for commercial purposes. When using this project, please comply with the relevant service terms of the Microsoft License Agreement.

***

[![Star History Chart](https://api.star-history.com/svg?repos=oopsunix/kms&type=Date)](https://star-history.com/#oopsunix/kms&Date)