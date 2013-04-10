from zope import interface as zinterface
from zope.interface import verify
# These imports are here for convenience, to be re-imported by others
from build_info import IBuildInfoProvider
from planning import IPlanningProvider
from source_code_control import ISourceCodeControlProvider
from oauth import IOAuthProvider

__all__ = [
    IBuildInfoProvider, IPlanningProvider, ISourceCodeControlProvider,
    IOAuthProvider,
    'is_implementation', 'is_planning_provider', 'is_build_info_provider',
    'is_source_code_provider'
]


def is_implementation(obj, interface):
    """
    Check that the given object implements the given interface.

    Mimics the signature and behaviour of `isinstance`, for interfaces.

    :returns:
        A boolean
    """
    zinterface.classImplements(obj.__class__, interface)
    try:
        verify.verifyObject(interface, obj)
        return True
    except Exception:
        #raise
        return False


def is_planning_provider(provider):
    return is_implementation(provider, IPlanningProvider)


def is_build_info_provider(provider):
    return is_implementation(provider, IBuildInfoProvider)


def is_source_code_provider(provider):
    return is_implementation(provider, ISourceCodeControlProvider)
