"""Test rayvision_blender.analyse_blender model."""
from unittest import mock


def test_check_local_os(blender):
    """Test print_info this interface."""
    mock_return = "win"
    blender.check_local_os = mock.Mock(return_value=mock_return)
    result = blender.check_local_os()
    assert result == "win"
