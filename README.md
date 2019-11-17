# Ansible Role: zend (Horizen)

[![Build Status](https://travis-ci.org/aschult5/ansible-role-zend.svg?branch=master)](https://travis-ci.org/aschult5/ansible-role-zend)

Installs and runs Horizen's zend in a container on Ubuntu servers.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see [defaults/main.yml](defaults/main.yml)):

    zend_ver: latest

The version of zend to install. Refer to [zen-node tags on Docker Hub](https://hub.docker.com/r/zencash/zen-node/tags) for valid version strings.

    zend_svc_name: zend

The name of the systemd service for zend.

    zend_port_p2p: "9033"
    zend_port_rpc: "8231"

The ports that zend listens on for P2P and RPC.
The P2P port *is* published to the internet.
The RPC port *is not* published to the internet.

    zend_dir: /mnt/horizen

Absolute path to the directory that will be mounted onto the container.
This directory corresponds to `~/.zen` from typical operation.

    zend_user_name: zenops
    zend_user_id: 1001
    zend_user_home: /home/{{ zend_user_name }}
    zend_user_shell: /bin/bash
    zend_user_groups_default: [ 'adm', 'systemd-journal', 'sudo' ]
    zend_user_groups: []

Variables to configure the server user that will own `zend_dir` and will run `zend`.
If there is an existing user you wish to use, modify these variables for that user.
Unless you have good reason to, you shouldn't modify `zend_user_groups_default`.
Instead, specify additional groups in `zend_user_groups`.

    zend_docker_host: unix:///var/run/docker.sock
    zend_docker_ctr_name: zend
    zend_docker_net_name: ZenNet
    zend_docker_net_subnet: 172.42.0.0/24
    zend_docker_net_gateway: 172.42.0.254
    zend_docker_net_connected: [ "{{ zend_docker_ctr_name }}" ]
    zend_docker_ipv4: 172.42.0.1

Variables to configure Docker.

    zend_tls_cert_path: ''
    zend_tls_key_path: ''

Absolute paths to the server certificate (cert.pem) and private key (privkey.pem) files.
This role does not generate or renew the server certificate.

## Dependencies

  - geerlingguy.firewall
  - geerlingguy.docker

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
