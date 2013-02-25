from importlib import import_module

from zope.interface import classImplements, verify

from interfaces import ISourceCodeControlPlugin, ICIPlugin, IPlanningPlugin

PLANNING_PLUGINS = []
SOURCE_CODE_PLUGINS = []
CI_PLUGINS = []


def get_plugin_class(path):
    "Given a path to a class import the module and return the class"
    index_pos = path.rindex('.')
    mod_path, class_name = path[:index_pos], path[index_pos + 1:]
    mod = import_module(mod_path)
    return getattr(mod, class_name)


def init_plugin_set(plugin_set, plugin_check, plugin_holder):
    "Create a set of plugins, check they are correct, add to a placeholder"
    for path in plugin_set:
        plugin_class = get_plugin_class(path)
        if plugin_check(plugin_class):
            plugin_holder.append(plugin_class())


def init_plugins():
    global PLANNING_PLUGINS, SOURCE_CODE_PLUGINS, CI_PLUGINS
    from deploystream import app
    init_plugin_set(app.config['SOURCE_CODE_PLUGINS'],
                    is_source_control_plugin,
                    SOURCE_CODE_PLUGINS)

    init_plugin_set(app.config['PLANNING_PLUGINS'],
                    is_planning_plugin,
                    PLANNING_PLUGINS)

    init_plugin_set(app.config['CI_PLUGINS'],
                    is_ci_plugin,
                    CI_PLUGINS)


def _check_implements(cls, interface):
    classImplements(cls, interface)
    try:
        verify.verifyClass(interface, cls)
        return True
    except Exception, e:
        print e
        return False


def is_source_control_plugin(plugin):
    "Check the plugin class given implements ISourceCodeControlPlugin."
    return _check_implements(plugin, ISourceCodeControlPlugin)


def is_planning_plugin(plugin):
    "Check the plugin class given implements IPlanningPlugin."
    return _check_implements(plugin, IPlanningPlugin)


def is_ci_plugin(plugin):
    "Check the plugin class given implements ICIPlugin."
    return _check_implements(plugin, ICIPlugin)
