from interfaces import (
    ISourceCodeControlPlugin, IBuildInfoPlugin, IPlanningPlugin,
    is_implementation
)

PLANNING_PLUGINS = []
SOURCE_CODE_PLUGINS = []
BUILD_INFO_PLUGINS = []

PLUGIN_INTERFACES = (
    ('SOURCE_CODE_PLUGINS', ISourceCodeControlPlugin, SOURCE_CODE_PLUGINS),
    ('BUILD_INFO_PLUGINS', IBuildInfoPlugin, BUILD_INFO_PLUGINS),
    ('PLANNING_PLUGINS', IPlanningPlugin, PLANNING_PLUGINS),
)
# A list of tuples of ('setting conf name', plugin interface class, holder_ref)


def get_plugin_class(path):
    "Given a path to a class import the module and return the class"
    mod_path, class_name = path.rsplit('.', 1)
    mod = __import__(mod_path, globals(), locals(), [class_name])
    return getattr(mod, class_name)


def init_plugin_set(plugin_set, plugin_interface, plugin_holder):
    "Create a set of plugins, check they are correct, add to a placeholder"
    for path, options in plugin_set:
        plugin_class = get_plugin_class(path)
        if is_implementation(plugin_class, plugin_interface):
            plugin_holder.append(plugin_class(**options))
        else:
            print('Skipping erroneous plugin: {0}'.format(path))


def init_plugins():
    from deploystream import app
    for config_name, plugin_class, holder in PLUGIN_INTERFACES:
        init_plugin_set(app.config[config_name],
                        plugin_class,
                        holder)
