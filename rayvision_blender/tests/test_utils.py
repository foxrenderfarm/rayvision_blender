# -*- coding:utf-8 -*-
"""Test rayvision_blender.utils functions."""

# pylint: disable=import-error
import pytest

from rayvision_blender import utils


@pytest.mark.parametrize("message, py_version", [
    ("test to encode", 3),
])
def test_get_encode(message, py_version):
    """Test get_encode, we can get a expected result."""
    assert utils.get_encode(message, py_version) == "unicode"


@pytest.mark.parametrize("message, py_version", [
    ("test str to unicode", 3),
])
def test_str_to_unicode(message, py_version):
    """Test str_to_unicode, we can get a expected type."""
    result = utils.str_to_unicode(message, py_version)
    assert isinstance(result, str)


@pytest.mark.parametrize("str1, py_version", [
    ("test unicode to str", 3),
])
def test_unicode_to_str(str1, py_version):
    """Test str_to_unicode, we can get a expected type."""
    result = utils.unicode_to_str(str1, py_version=py_version)
    assert isinstance(result, str)


@pytest.mark.parametrize("str1, py_version, str_decode", [
    (b"test unicode to str", 3, 'utf-8'),
])
def test_bytes_to_str(str1, py_version, str_decode):
    """Test str_to_unicode, we can get a expected type."""
    result = utils.bytes_to_str(str1, py_version=py_version,
                                str_decode=str_decode)
    assert isinstance(result, str)


@pytest.mark.parametrize("encode_str, py_version", [
    ("to gbk", 3),
])
def test_to_gbk(encode_str, py_version):
    """Test str_to_unicode, we can get a expected type."""
    result = utils.to_gbk(encode_str, py_version)
    assert isinstance(result, str)


@pytest.mark.parametrize("path", [
    "D:/work/render/19183793/max/d/Work/c05.txt",
    "D:\\work/render/19183793\\max/d/Work/c05.txt"
])
def test_convert_path(path):
    """Test get_encode, we can get a expected result."""
    result_path = utils.convert_path(path)
    assert result_path == r"/D/work/render/19183793/max/d/Work/c05.txt"
