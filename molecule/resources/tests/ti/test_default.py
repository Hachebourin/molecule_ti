import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('haproxy')


def get_curl_result(host, port):
    return host.run("curl -s localhost:" + port).stdout


def test_ha_proxy_round_robin(host):
    res = []
    list_serv = host.ansible.get_variables()['groups']['srv_web']
    nb_serv = len(list_serv)

    assert nb_serv != 0
    assert host.package('haproxy').is_installed

    for i in range(nb_serv):
        res.append(get_curl_result(host, "8080").rstrip('\n'))

    for i in list_serv:
        assert "Hostname: %s" % (i) in res
        res.remove("Hostname: %s" % (i))
