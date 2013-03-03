from zope import interface as zinterface
from zope.interface import verify

from build_info import IBuildInfoPlugin
from planning import IPlanningPlugin
from source_code_control import ISourceCodeControlPlugin


def isimplementation(cls, interface):
    """
    Check that the given class implements the given interface.

    Mimics the signature and behaviour of `isinstance`, for interfaces.

    :returns:
        A boolean
    """
    zinterface.classImplements(cls, interface)
    try:
        zinterface.verify.verifyClass(interface, cls)
        return True
    except Exception:
        #raise
        return False
