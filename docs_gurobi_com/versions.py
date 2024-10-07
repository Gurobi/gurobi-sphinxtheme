""" Keeps version customisation (beta, dev, current, etc). This should be
the central place for updates with a new release.

Note that this deals with version numbering, not 'latest'/'current'.
"""


def is_released_version(version):
    try:
        numeric = float(version)
        return numeric < 12.0
    except ValueError:
        return False


def is_current_version(version):
    return version == "11.0"


def is_beta_version(version):
    return version == "12.0"


def test_is_released_version():
    assert is_released_version("2.0")
    assert is_released_version("10.0")
    assert is_released_version("11.0")
    assert not is_released_version("12.0")
    assert not is_released_version("12.9")
    assert not is_released_version("12.9.dev")
    assert not is_released_version("v12-nonlinear")


def test_is_current_version():
    assert not is_current_version("2.0")
    assert not is_current_version("10.0")
    assert is_current_version("11.0")
    assert not is_current_version("12.0")
    assert not is_current_version("12.9")
    assert not is_current_version("12.9.dev")
    assert not is_current_version("v12-nonlinear")


def test_is_beta_version():
    assert not is_beta_version("2.0")
    assert not is_beta_version("10.0")
    assert not is_beta_version("11.0")
    assert is_beta_version("12.0")
    assert not is_beta_version("12.9")
    assert not is_beta_version("12.9.dev")
    assert not is_beta_version("v12-nonlinear")
