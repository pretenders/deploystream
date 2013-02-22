import imp
import inspect


class PluginError(Exception):
    pass


class ProviderPluginReader(object):

    required = {}
    optional = {}

    def __init__(self, plugin_name, module_path):
        self.plugin_name = plugin_name
        self._plugin = imp.load_source(plugin_name, module_path)
        self.check_method_defs()

    def __getattr__(self, attr):
        return getattr(self._plugin, attr)

    def check_method_defs(self):
        for func_name, required_args in self.required.items():
            try:
                meth = getattr(self, func_name)
            except AttributeError:
                raise PluginError("Required function {0} is not defined in"
                                  "the plugin {1}".format(func_name,
                                                          self.plugin_name))
            try:
                args, varargs, varkw, defaults = inspect.getargspec(meth)
                if "**kwargs" in required_args:
                    assert varkw is not None
                    required_args.remove("**kwargs")
                assert required_args == args
            except AssertionError:
                raise PluginError("Function definition of {0} does not match"
                                  " that defined in {1}".format(func_name,
                                                      self.__class__.__name__))
