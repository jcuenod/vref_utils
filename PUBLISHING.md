# Publishing to Pypi

This is configured to happen automatically through Github actions **when a new release is cut**.

## Steps for cutting a new release:

1. The version number comes from setup.py. Update it before cutting a new release (use semver).
2. Create a new release on Github. The tag should be the version number, and the release notes should include the changes since the last release.

# Development

To build the package, run:

```bash
pip uninstall vref_utils
rm -rf dist
python setup.py sdist
```

To install the package locally, run:

```bash
pip install ./dist/vref_utils-<version-number>.tar.gz
```

# Tests

_Forthcoming_
