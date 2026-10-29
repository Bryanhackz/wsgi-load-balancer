# Security Policy

## Supported Versions
Currently, only the latest `main` branch is supported.

## Scope
This is a reverse proxy and load balancer. The primary security focus is on preventing HTTP request smuggling, header injection, and ensuring that backend health checks cannot be spoofed to route traffic maliciously. It assumes the backend servers are in a trusted internal network.

## Reporting a Vulnerability
Please do not report security vulnerabilities through public GitHub issues. Send an email to **br4yangil006@gmail.com**. You should receive a response within 48 hours.

Please include:
- Type of issue (e.g., request smuggling, SSRF via backend URL, header injection)
- Full paths of source file(s) related to the issue
- Step-by-step instructions to reproduce the issue
- Impact of the issue
