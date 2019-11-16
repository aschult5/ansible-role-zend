import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_zend_is_installed(host):
    containers = host.docker.get_containers()
    zend = next((c for c in containers if c.name == 'zend'), None)
    assert zend


def test_zend_running(host):
    zend = host.service('zend')
    assert zend.is_enabled
    assert zend.is_running
