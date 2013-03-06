from hamcrest import assert_that, equal_to

from deploystream.lib.transforms import remap


class TestRemap(object):

    def test_simple_name_remap(self):

        original = {"identifier": 123, "name": "A feature"}
        expected = {"id": 123, "title": "A feature"}

        mapped = remap(original, {"identifier": "id", "name": "title"})

        assert_that(mapped, equal_to(expected))
