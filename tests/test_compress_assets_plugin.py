import os
import sys
from unittest import mock

import pytest

from sigal import init_plugins
from sigal.gallery import Gallery
from sigal.plugins import compress_assets

CURRENT_DIR = os.path.dirname(__file__)


def make_gallery(settings, tmpdir, method):
    settings['destination'] = str(tmpdir)
    # Really speed up testing
    settings['use_orig'] = True
    if "sigal.plugins.compress_assets" not in settings["plugins"]:
        settings['plugins'] += ["sigal.plugins.compress_assets"]

    # Set method
    settings.setdefault('compress_assets_options', {})['method'] = method

    compress_options = compress_assets.DEFAULT_SETTINGS.copy()
    # The key was created by the previous setdefault if needed
    compress_options.update(settings['compress_assets_options'])

    init_plugins(settings)
    gal = Gallery(settings)
    gal.build()

    return compress_options


def walk_destination(destination, suffixes, compress_suffix):
    for path, dirs, files in os.walk(destination):
        for file in files:
            original_filename = os.path.join(path, file)
            compressed_filename = '{}.{}'.format(
                os.path.join(path, file), compress_suffix
            )
            path_exists = os.path.exists(compressed_filename)
            file_ext = os.path.splitext(file)[1][1:]
            if file_ext in suffixes:
                assert path_exists
                assert (
                    os.stat(original_filename).st_mtime
                    <= os.stat(compressed_filename).st_mtime
                )
            else:
                assert not path_exists


@pytest.mark.parametrize(
    "method,compress_suffix,test_import",
    [('gzip', 'gz', None), ('zopfli', 'gz', 'zopfli.gzip'), ('brotli', 'br', 'brotli')],
)
def test_compress(
    disconnect_signals, settings, tmpdir, method, compress_suffix, test_import
):
    if test_import:
        pytest.importorskip(test_import)

    # Compress twice to test compression skip based on mtime
    for _ in range(2):
        compress_options = make_gallery(settings, tmpdir, method)
        walk_destination(
            settings['destination'], compress_options['suffixes'], compress_suffix
        )


@pytest.mark.parametrize(
    "method,compress_suffix,mask",
    [
        ('zopfli', 'gz', 'zopfli.gzip'),
        ('brotli', 'br', 'brotli'),
        ('__does_not_exist__', 'br', None),
    ],
)
def test_failed_compress(
    disconnect_signals, settings, tmpdir, method, compress_suffix, mask
):
    # See https://medium.com/python-pandemonium/how-to-test-your-imports-1461c1113be1
    with mock.patch.dict(sys.modules, {mask: None}):
        make_gallery(settings, tmpdir, method)
        walk_destination(
            settings['destination'], [], compress_suffix  # No file should be compressed
        )
