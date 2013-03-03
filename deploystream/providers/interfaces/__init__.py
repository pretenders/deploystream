from zope import interface as zinterface
from zope.interface import verify

# These imports are here for convenience, to be re-imported by others
from build_info import IBuildInfoPlugin
from planning import IPlanningPlugin
from source_code_control import ISourceCodeControlPlugin

__all__ = [
    IBuildInfoPlugin, IPlanningPlugin, ISourceCodeControlPlugin,
    'is_implementation'
]


def is_implementation(cls, interface):
    """
    Check that the given class implements the given interface.

    Mimics the signature and behaviour of `isinstance`, for interfaces.

    :returns:
        A boolean
    """
    zinterface.classImplements(cls, interface)
    try:
        verify.verifyClass(interface, cls)
        return True
    except Exception:
        #raise
        return False
