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
    net_name = os.environ['ZEND_DOCKER_NET_NAME']
    net = ctr.inspect()['NetworkSettings']['Networks'].get(net_name)
    assert net
    assert net['IPAddress'] == os.environ['ZEND_DOCKER_IPV4']

    # Check volume
    vol_str = os.environ['ZEND_ZCASH_SRCVOL']
    binds = ctr.inspect()['HostConfig']['Binds']
    assert filter(lambda k: vol_str in k, binds)


def test_zend_service(host):
    svc_name = os.environ['ZEND_SVC_NAME']
    zend_svc = host.service(svc_name)
    assert zend_svc.is_running
    assert zend_svc.is_enabled


def test_zend_user(host):
    u = host.user(name=os.environ['ZEND_USER_NAME'])

    assert u
    assert str(u.uid) == os.environ['ZEND_USER_ID']
