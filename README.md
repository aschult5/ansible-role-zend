# Ansible Role: zend (Horizen)

[![Build Status](https://travis-ci.org/aschult5/ansible-role-zend.svg?branch=master)](https://travis-ci.org/aschult5/ansible-role-zend)

Installs and runs Horizen's zend in a container on Ubuntu servers.

## Requirements

- Docker installed.
- Zend P2P port open (see `zend_port_p2p` below)

## Role Variables

Available variables are listed below, along with default values (see [defaults/main.yml](defaults/main.yml)):

    zend_ver: latest

The version of zend to install. Refer to [zen-node tags on Docker Hub](https://hub.docker.com/r/zencash/zen-node/tags) for valid version strings.

    zend_user_name: zenops
    zend_group_name: zenops

Name of the user/group that will own `zend_dir` and will run `zend`.
If the user/group doesn't already exist, it will be created as a system user/group.

    zend_port_p2p: "9033"
    zend_port_rpc: "8231"

The ports that zend listens on for P2P and RPC.
The P2P port *is* published to the internet.
The RPC port *is not* published to the internet.

    zend_dir: /mnt/horizen

Absolute path to the directory that will be mounted onto the container.
This directory corresponds to `~/.zen` from typical operation.

    zend_svc_name: zend
    zend_svc_enabled: yes

Configuration of the systemd service for zend.

    zend_docker_host: unix:///var/run/docker.sock
    zend_docker_ctr_name: zend
    zend_docker_ctr_stop_timeout: 600
    zend_docker_net_name: ZenNet
    zend_docker_net_subnet: 172.42.0.0/24
    zend_docker_net_gateway: 172.42.0.254
    zend_docker_ipv4: 172.42.0.1

Variables to configure Docker.

    zend_zcash_srcvol: zcash-params

Source docker volume to store zcash-params from `zen-fetch-params`.

    zend_ipv4: ''
    zend_ipv6: ''

External IP addresses to be used by zend.

    zend_tls_cert_path: ''
    zend_tls_key_path: ''
    zend_tls_cert_dir: /etc/letsencrypt/live/{{ inventory_hostname }}

Relevant paths for the *optional* server certificate and private key files.
If either `zend_tls_cert_path` or `zend_tls_key_path` is empty or non-existent,
`zend_tls_cert_dir` will be checked for cert.pem and privkey.pem.
This role does not generate or renew the server certificate.
This role chgrps the certificate files' parent directory to `zend_group_name`.

## Dependencies

- None

## Example Playbook

```yaml
- hosts: zend
  roles:
    - role: aschult5.zend
      become: yes
```

## See Also
[aschult5.zen_nodetracker](https://github.com/aschult5/ansible-role-zen-nodetracker)
[aschult5.horizen](https://github.com/aschult5/ansible-collection-horizen)

## License

MIT

## Author Information

This role was created in 2019 by Andrew Schultz for use with [Nodeler](https://www.nodeler.com)
