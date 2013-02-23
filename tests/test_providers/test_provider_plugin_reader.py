from os.path import join, dirname, abspath

from nose.tools import assert_equal, assert_raises

from deploystream.providers.base import ProviderPluginReader, PluginError

example_mod = join(abspath(dirname(__file__)), 'data', 'dummy_module.py')


def test_accesses_module_functions():
    p = ProviderPluginReader('example_mod', example_mod)
    assert_equal("faked", p.fake_method())
    assert_equal("faked_2", p.fake_method_args("a", "b"))


def test_checking_of_required_functions():
    class DummyPlugin(ProviderPluginReader):
        required = {
            'fake_method_args': [
                'foo',
                'bar',
                '**kwargs',
            ]
        }

    # Works fine
    DummyPlugin('example_mod', example_mod)

    # Add a required method that doesn't exist - should error
    DummyPlugin.required['fake_method_non_existent'] = []
    assert_raises(PluginError, DummyPlugin, 'example_mod', example_mod)

    del DummyPlugin.required['fake_method_non_existent']

    # Works fine
    DummyPlugin('example_mod', example_mod)

    # Add an additional required arg to the fake_method_args - should error
    DummyPlugin.required['fake_method_args'].insert(0, 'arg1')
    assert_raises(PluginError, DummyPlugin, 'example_mod', example_mod)
