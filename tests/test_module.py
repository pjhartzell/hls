import stactools.hls


def test_version() -> None:
    assert stactools.hls.__version__ is not None
