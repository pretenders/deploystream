def nativify(data):
    """
    Convert stuff to native datatypes that can be json-encoded.

    This is a bespoke implementation that works with the types
    of objects we support.
    """
    if isinstance(data, unicode):
        return data.encode('utf-8')
    if isinstance(data, basestring) or isinstance(data, int):
        return repr(data)
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


def remap(original, keymap):
    """
    Generate a new dictionary by mapping certain keys to others.

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
    """
    def _transform(k, v):
        newk = keymap.get(k, k)
        if isinstance(newk, tuple):
            newk, valuemap = newk
            return newk, valuemap.get(v, v)
        else:
            return newk, v

    return dict([_transform(k, v) for k, v in original.iteritems()])
