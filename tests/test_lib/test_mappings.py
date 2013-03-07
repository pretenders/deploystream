from hamcrest import assert_that, equal_to

from deploystream.lib.transforms import remap


class TestRemap(object):

    def test_name_remap(self):
        """
        Test remapping of field names only.
        """

        original = {"identifier": 123, "name": "A feature"}
        mapping = {"identifier": "id", "name": "title"}
        expected = {"id": 123, "title": "A feature"}

        mapped = remap(original, mapping)

        assert_that(mapped, equal_to(expected))

    def test_name_and_value_remap(self):
        """
        Test remapping of field names and values.
        """

        original = {"identifier": 123, "class": "bug"}
        original2 = {"identifier": 124, "class": "story"}
        mapping = {"identifier": "id", "class": ("type", {"bug": "defect"})}
        expected = {"id": 123, "type": "defect"}
        expected2 = {"id": 124, "type": "story"}

        mapped = remap(original, mapping)
        mapped2 = remap(original2, mapping)

        assert_that(mapped, equal_to(expected))
        assert_that(mapped2, equal_to(expected2))
