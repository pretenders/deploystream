from os.path import join, dirname
import shutil
import filecmp

import certifi
import httplib2


def ensure_certifi_certs_installed():
    """Give certifi's latest pem to httplib2.

    This function was added to give httplib2 a more up to date collection of
    trusted CAs. It was required once we started using flask_oauth which relies
    on ``httplib2`` rather than ``requests``
    """
    source = certifi.where()
    destination = join(dirname(httplib2.__file__), 'cacerts.txt')
    if not filecmp.cmp(source, destination, shallow=False):
        print ("Writing new cacerts.txt")
        shutil.copyfile(source, destination)
