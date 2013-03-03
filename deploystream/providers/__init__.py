from importlib import import_module

# from zope import interface as zinterface

from interfaces import (
    ISourceCodeControlPlugin, IBuildInfoPlugin, IPlanningPlugin,
    isimplementation
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
    index_pos = path.rindex('.')
    mod_path, class_name = path[:index_pos], path[index_pos + 1:]
    mod = import_module(mod_path)
    return getattr(mod, class_name)


def init_plugin_set(plugin_set, plugin_interface, plugin_holder):
    "Create a set of plugins, check they are correct, add to a placeholder"
    for path in plugin_set:
        plugin_class = get_plugin_class(path)
        if isimplementation(plugin_class, plugin_interface):
            plugin_holder.append(plugin_class())


def init_plugins():
    from deploystream import app
    for config_name, plugin_class, holder in PLUGIN_INTERFACES:
        init_plugin_set(app.config[config_name],
                        plugin_class,
                        holder)
