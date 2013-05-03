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

        mapped = remap(original, mapping, keep_extra=False)

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

        mapped = remap(original, mapping, keep_extra=False)
        mapped2 = remap(original2, mapping, keep_extra=False)

        assert_that(mapped, equal_to(expected))
        assert_that(mapped2, equal_to(expected2))

    def test_nested_name_remap(self):
        """
        Test nested field names can be mapped.
        """
        original = {"somekey": {"identifier": 123, "other_data": 445}}
        mapping = {('somekey', 'identifier'): "id"}
        expected = {"id": 123}

        mapped = remap(original, mapping, keep_extra=False)

        assert_that(mapped, equal_to(expected))

    def test_name_remap_keep_original(self):
        """
        Test original fields can be kept if requested.
        """
        original = {"old_id": 123}
        mapping = {"old_id": "new_id"}
        expected = {"old_id": 123, "new_id": 123}

        mapped = remap(original, mapping, keep_extra=True)

        assert_that(mapped, equal_to(expected))
