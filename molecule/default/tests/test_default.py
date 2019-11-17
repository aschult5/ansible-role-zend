import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_zend_is_installed(host):
    zend_ctr = os.environ['ZEND_DOCKER_CTR_NAME']
    zend = host.docker(zend_ctr)
    assert zend


def test_zend_running(host):
    zend_svc = os.environ['ZEND_SVC_NAME']
    zend = host.service(zend_svc)
    assert zend.is_running
    assert zend.is_enabled
