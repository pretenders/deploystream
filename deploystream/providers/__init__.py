from collections import defaultdict

from deploystream.apps.oauth import get_oauth_token
from deploystream.providers.interfaces import (
    IBuildInfoProvider, IPlanningProvider, ISourceCodeControlProvider,
    is_implementation)

ALL_PROVIDER_CLASSES = {}
"Populated by init_provider with keys of names and values of imported classes"


def get_provider_class(path):
    "Given a path to a class import the module and return the class"
    mod_path, class_name = path.rsplit('.', 1)
    mod = __import__(mod_path, globals(), locals(), [class_name])
    return getattr(mod, class_name)


def get_providers(configs, session):
    """
    Get appropriate providers for the given session.

    :param configs:
        A list of tuples with provider name and configuration.

    :param session:
        A session in which to find things for the provider.

    :returns:
        A dictionary of interface: list of providers that implement the
        interface
    """
    providers = defaultdict(list)
    for name, config in configs:
        provider_class = ALL_PROVIDER_CLASSES[name]
        kwargs = {}
        kwargs.update(config)
        try:
            kwargs['token'] = get_oauth_token(
                                    session,
                                    provider_class.oauth_token_required)
        except AttributeError:
            # The provider class doesn't define any oauth requirement.
            print ("INFO: provider {0} does not want a token".format(name))
            pass
        except KeyError:
            print ("WARNING: provider {0} wanted a token "
                   "but we didn't have one".format(name))
            pass

        provider = provider_class(**kwargs)

        for iface in [IBuildInfoProvider, IPlanningProvider,
                      ISourceCodeControlProvider]:
            if is_implementation(provider.__class__, iface):
                providers[iface].append(provider)
    return providers


def init_providers(provider_path_set):
    """Import and store in memory all available provider classes

    :param provider_path_set:
        A list of class paths to import.
    """
    for path in provider_path_set:
        provider_class = get_provider_class(path)
        ALL_PROVIDER_CLASSES[provider_class.name] = provider_class
