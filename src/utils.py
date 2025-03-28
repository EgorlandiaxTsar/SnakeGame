def require_object(obj, obj_type, argument_name='unknown'):
    if not (isinstance(obj, obj_type)):
        raise TypeError('Incompatible type of argument \'' + argument_name + '\', must be \'' + obj + '\'')
    return obj


def require_int(number, argument_name='unknown'):
    return require_object(number, int, argument_name)


def require_bool(boolean, argument_name='unknown'):
    return require_object(boolean, bool, argument_name)


def require_string(string, argument_name='unknown'):
    return require_object(string, str, argument_name)


def calculate_center_position(width, height, screen_width, screen_height):
    width = require_int(width, 'width')
    height = require_int(height, 'height')
    return {
        'x': (screen_width - width) / 2,
        'y': (screen_height - height) / 2
    }
