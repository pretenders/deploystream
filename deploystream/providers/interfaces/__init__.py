from zope import interface as zinterface
from zope.interface import verify

# These imports are here for convenience, to be re-imported by others
from build_info import IBuildInfoPlugin
from planning import IPlanningPlugin
from source_code_control import ISourceCodeControlPlugin

__all__ = [
    IBuildInfoPlugin, IPlanningPlugin, ISourceCodeControlPlugin,
    'is_implementation', 'is_planning_provider', 'is_build_info_provider',
    'is_source_code_provider'
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


def is_planning_provider(provider):
    return is_implementation(provider.__class__, IPlanningPlugin)


def is_build_info_provider(provider):
    return is_implementation(provider.__class__, IBuildInfoPlugin)


def is_source_code_provider(provider):
    return is_implementation(provider.__class__, ISourceCodeControlPlugin)
