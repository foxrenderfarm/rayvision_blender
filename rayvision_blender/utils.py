"""Common method for rayvision_blender API."""

import sys


def get_encode(encode_str, py_version=3):
    """Get the encoding of the string decoding.

    Args:
        encode_str (str, unicode): String.
        py_version (int): Python version, default is 3.

    Returns:
        str: Coding.

    """
    if ((py_version == 2 and isinstance(encode_str, str)) or (
            py_version == 3 and isinstance(encode_str, str))):
        encode = "unicode"
    else:
        for code in ["utf-8", sys.getfilesystemencoding(), "gb18030",
                     "ascii", "gbk", "gb2312"]:
            try:
                encode_str.decode(code, 'ignore')
                return code
            except UnicodeDecodeError:
                pass
        encode = 'utf-8'
    return encode


def str_to_unicode(encode_str, py_version=3):
    """Get the encoding of the string decoding.

    Args:
        encode_str (str, unicode): String.
        py_version (int): Python version, default is 3.

    Returns:
        str: String.

    """
    if (encode_str is None or encode_str == "" or encode_str == 'Null' or
            encode_str == 'null'):
        encode_str = ""
    elif ((py_version == 2 and isinstance(encode_str, str)) or (
            py_version == 3 and isinstance(encode_str, str))):
        pass
    else:
        code = get_encode(encode_str)
        encode_str = encode_str.decode(code, 'ignore')
    return encode_str


def unicode_to_str(str1, logger=None, str_encode='system', py_version=3):
    """Unicode encoded string converted to str."""
    if str1 is None or str1 == "" or str1 == 'Null' or str1 == 'null':
        str1 = ""
    elif ((py_version == 2 and isinstance(str1, str)) or (
            py_version == 3 and isinstance(str1, str))):
        try:
            if str_encode.lower() == 'system':
                str1 = str1.encode(sys.getfilesystemencoding(), 'ignore')
            elif str_encode.lower() == 'utf-8':
                str1 = str1.encode('utf-8', 'ignore')
            elif str_encode.lower() == 'gbk':
                str1 = str1.encode('gbk', 'ignore')
            else:
                str1 = str1.encode(str_encode, 'ignore')
        except UnicodeDecodeError as err_message:
            if logger:
                logger.info('[err]unicode_to_str:encode %s to %s failed',
                            str1, str_encode)
                logger.info(str(err_message))
    elif ((py_version == 2 and isinstance(str1, str)) or (
            py_version == 3 and isinstance(str1, bytes))):
        pass
    else:
        if logger:
            logger.info('%s is not unicode ', str1)
    return str(str1)


def bytes_to_str(str1, logger=None, str_decode='default', py_version=3):
    """Bytes encoded string converted to str."""
    if not ((py_version == 2 and isinstance(str1, str)) or
            (py_version == 3 and isinstance(str1, str))):
        try:
            if str_decode != 'default':
                str1 = str1.decode(str_decode.lower(), 'ignore')
            else:
                try:
                    str1 = str1.decode('utf-8', 'ignore')
                except UnicodeDecodeError:
                    try:
                        str1 = str1.decode('gbk', 'ignore')
                    except UnicodeDecodeError:
                        str1 = str1.decode(sys.getfilesystemencoding(),
                                           'ignore')
        except UnicodeDecodeError as err_message:
            if logger:
                logger.info('[err]bytes_to_str:decode %s to str failed', str1)
                logger.info(str(err_message))
    return str1


def to_gbk(encode_str, py_version):
    """Convert string to gbk code."""
    if ((py_version == 2 and isinstance(encode_str, str
                                        )) or (py_version == 3 and
                                               isinstance(encode_str, str))):
        pass
    else:
        code = get_encode(encode_str)
        encode_str = encode_str.decode(code).encode('GBK', 'ignore')
    return encode_str


def convert_path(path):
    """Convert to the path the server will accept.

    Args:
        path (str): Local file path.
            e.g.:
                "D:/work/render/19183793/max/d/Work/c05/112132P-embery.jpg"

    Returns:
        str: Path to the server.
            e.g.:
                "/D/work/render/19183793/max/d/Work/c05/112132P-embery.jpg"

    """
    lower_path = path.replace('\\', '/')
    if lower_path[1] == ":":
        path_lower = lower_path.replace(":", "")
        path_server = "/" + path_lower
    else:
        path_server = lower_path[1:]

    return path_server
