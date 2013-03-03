from zope import interface as zinterface

from build_info import IBuildInfoPlugin
from planning import IPlanningPlugin
from source_code_control import ISourceCodeControlPlugin


def check_class_implements_interface(cls, interface):
    "Check that the given class implements the given interface. Return Bool"
    zinterface.classImplements(cls, interface)
    try:
        zinterface.verify.verifyClass(interface, cls)
        return True
    except Exception:
        return False
