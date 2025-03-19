# KMS Server

Microsoft Windows/Office KMS 本地激活服务器

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Docker Image Version](https://img.shields.io/docker/v/oopsunix/kms)
![Docker Image Size](https://img.shields.io/docker/image-size/oopsunix/kms?color=0eb305)
![Docker Pulls](https://img.shields.io/docker/pulls/oopsunix/kms?color=7842f5)
***

<p>
  中文 | <a href="./README.md">English</a>
</p>

## 🌟 支持产品
- 响应 v4、v5 和 v6 KMS 请求。
- 支持激活以下版本的 Windows Server:
	- Windows Server 2008
	- Windows Server 2008 R2
	- Windows Server 2012
	- Windows Server 2012 R2
	- Windows Server 2016
	- Windows Server 2019
	- Windows Server 2022
	- Windows Server 2025
- 支持激活以下批量许可( Volume License )版本的 Windows:
	- Windows Vista
	- Windows 7
	- Windows 8
	- Windows 8.1
	- Windows 10
    - Windows 11
- 支持激活以下批量许可( Volume License )版本的 Office:
	- Microsoft Office 2010
	- Microsoft Office 2013
	- Microsoft Office 2016
	- Microsoft Office 2019
	- Microsoft Office 2021
	- Microsoft Office LTSC 2021
	- Microsoft Office LTSC 2024

## 📦 部署

### Docker Compose 部署

```yaml
services:
  kms:
    image: "oopsunix/kms:latest"
    # image: "ghcr.io/oopsunix/kms:latest" # GitHub Container Registry
    container_name: "kms"
    restart: "always"
    ports:
      - "1688:1688" # KMS 服务端口
      - "8080:8080" # Web UI 端口 (可选)
    environment:
      - WEBUI=1     # 启用 Web UI（默认为 0 不启用）
```

### 环境变量

| Parameter | Value | Default |
| --------- | ----- | ------- |
| `TZ` | [Time Zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) | Asia/Shanghai |
| `DEBUG` | Will activate debug option for container image and app (if available) | |
| `KMS_LOCALE` | 参见Microsoft LICD规范 | 1033 (en-US) |
| `KMS_CLIENTCOUNT` | 客户端数量 > 25 | 26 |
| `KMS_ACTIVATIONINTERVAL` | 失败重试间隔（分钟） | 120 (2 hours) |
| `KMS_RENEWALINTERVAL` | 自动续期间隔（分钟） | 129600 (90 days) |
| `KMS_LOGLEVEL` | CRITICAL, ERROR, WARNING, INFO, DEBUG, MININFO | INFO |

## ❤️ 致谢

* [py-kms](https://github.com/Py-KMS-Organization/py-kms)

## 🤝 贡献

欢迎贡献代码或提出建议！

## 📜 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## ⚠️ 免责声明

本项目仅供学习和研究之用，请勿用于商业用途。使用本项目时请遵守微软许可协议的相关服务条款。

***

[![Star History Chart](https://api.star-history.com/svg?repos=oopsunix/kms&type=Date)](https://star-history.com/#oopsunix/kms&Date)