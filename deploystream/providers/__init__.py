ALL_PROVIDER_CLASSES = {}
"Populated by init_provider with keys of names and values of imported classes"


def get_provider_class(path):
    "Given a path to a class import the module and return the class"
    mod_path, class_name = path.rsplit('.', 1)
    mod = __import__(mod_path, globals(), locals(), [class_name])
    return getattr(mod, class_name)


def get_providers(config_dict, session):
    """
    Get appropriate providers for the given session.

    :param config_dict:
        A dictionary of provider name to configuration.

    :param session:
        A session in which to find things for the provider.
    """
    providers = []
    for name, config in config_dict.items():
        provider_class = ALL_PROVIDER_CLASSES[name]
        kwargs = {}
        kwargs.update(config)
        try:
            kwargs['token'] = session.get(
                                'tokens',
                                {})[provider_class.oauth_token_required]
        except AttributeError:
            # The provider class doesn't define any oauth requirement.
            pass
        except KeyError:
            print ("WARNING: A provider wanted a token but we didn't have one")
            pass
        providers.append(provider_class(**kwargs))
    return providers


def init_providers(provider_path_set):
    """Import and store in memory all available provider classes

    :param provider_path_set:
        A list of class paths to import.
    """
    for path in provider_path_set:
        provider_class = get_provider_class(path)
        ALL_PROVIDER_CLASSES[provider_class.name] = provider_class
