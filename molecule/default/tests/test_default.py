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
        cmd = host.run('ln -sf {} {}'.format(docker_sock, docker_sock_default))
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
    print(net)
    assert net['IPAddress'] == os.environ['ZEND_DOCKER_IPV4']

    # Check volume
    vol_str = os.environ['ZEND_ZCASH_SRCVOL']
    binds = ctr.inspect()['HostConfig']['Binds']
    print(binds)
    assert filter(lambda k: vol_str in k, binds)

    # Check ports
    port_p2p_num = os.environ['ZEND_PORT_P2P']
    port_rpc_num = os.environ['ZEND_PORT_RPC']
    ports = ctr.inspect()['NetworkSettings']['Ports']
    print(ports)

    # ...p2p port should be published
    port_p2p = next(k for k in ports.keys() if port_p2p_num in k)
    assert ports[port_p2p]
    assert filter(lambda p: p.get('HostPort') == port_p2p_num, ports[port_p2p])

    # ...rpc port should NOT be published
    port_rpc = next(k for k in ports.keys() if port_rpc_num in k)
    assert not ports[port_rpc]


def test_zend_service(host):
    svc_name = os.environ['ZEND_SVC_NAME']
    zend_svc = host.service(svc_name)
    assert zend_svc.is_running
    assert zend_svc.is_enabled


def test_zend_user(host):
    u = host.user(name=os.environ['ZEND_USER_NAME'])
    assert u
    print(u)

    assert str(u.uid) == os.environ['ZEND_USER_ID']
