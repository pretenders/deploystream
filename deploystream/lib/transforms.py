def nativify(data):
    """
    Convert stuff to native datatypes that can be json-encoded.

    This is a bespoke implementation that works with the types
    of objects we support.
    """
    if isinstance(data, unicode):
        return data.encode('utf-8')
    if isinstance(data, basestring) or isinstance(data, int):
        return data
    elif isinstance(data, list) or isinstance(data, tuple):
        return [nativify(x) for x in data]
    elif isinstance(data, dict):
        return {
            k: nativify(v)
            for k, v in data.items() if not k.startswith('_')
        }
    elif data is None:
        return 'null'
    elif hasattr(data, '__dict__'):
        return nativify(data.__dict__)
    else:
        return '"{0}"'.format(data)


def remap(original, keymap, keep_extra=True):
    """
    Return a new dictionary using data from original mapped using keymap.

    This is a base adaptation layer to simplify translating various
    field names as provided by 3rd party services so that they are
    mapped to canonical values as used within `deploystream`.

    :param original:
        The original dictionary (typically, a response from a JSON
        API).

    :param keymap:
        A dictionary mapping original field name => transformation.
        Transformation can be a single string, representing the new
        name for the field, if only the name changes, or a tuple
        containing `(new_name, value_mapping)`.
        Original field name can be a single string, representing the location
        in the original dict to find the value, or a tuple of keys if the value
        is nested.

    :param keep_extra:
        If ``True``, all existing keys are brought across. If ``False``, only
        keys defined in keymap will be moved across to the new dictionary.
    """

    if keep_extra:
        new_dict = original.copy()
    else:
        new_dict = {}

    for find_key, new_key in keymap.iteritems():
        if isinstance(find_key, tuple):
            # Get the nested value of the composite key
            found_value = original
            for sub_key in find_key:
                if not found_value:
                    break
                found_value = found_value[sub_key]
        else:
            found_value = original.get(find_key)

        if isinstance(new_key, tuple):
            new_key, valuemap = new_key
            found_value = valuemap.get(found_value, found_value)
        new_dict[new_key] = found_value

    return new_dict
