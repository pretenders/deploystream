from os.path import join, dirname
import shutil
import filecmp

import certifi
import httplib2


def ensure_certifi_certs_installed():
    "Give certifi's latest pem to httplib2"
    source = certifi.where()
    destination = join(dirname(httplib2.__file__), 'cacerts.txt')
    if not filecmp.cmp(source, destination, shallow=False):
        print ("Writing new cacerts.txt")
        shutil.copyfile(source, destination)
