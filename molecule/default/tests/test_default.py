import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_host(host):
    docker_sock_default = '/var/run/docker.sock'
    docker_sock = os.environ['ZEND_DOCKER_HOST'].replace('unix://', '', 1)
    assert host.file(docker_sock)
    if docker_sock != docker_sock_default:
        cmd = host.run('ln -s {} {}'.format(docker_sock, docker_sock_default))
        assert cmd.rc == 0


def test_zend_container(host):
    # Check container
    ctr_name = os.environ['ZEND_DOCKER_CTR_NAME']
    ctr = host.docker(ctr_name)
    assert ctr
    assert ctr.is_running

    # Check network
    ctr_net_name = os.environ['ZEND_DOCKER_NET_NAME']
    ctr_net = ctr.inspect()['NetworkSettings']['Networks'].get(ctr_net_name)
    assert ctr_net
    assert ctr_net['IPAddress'] == os.environ['ZEND_DOCKER_IPV4']


def test_zend_service(host):
    svc_name = os.environ['ZEND_SVC_NAME']
    zend_svc = host.service(svc_name)
    assert zend_svc.is_running
    assert zend_svc.is_enabled
