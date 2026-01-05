# Publishing `imagecorruptions` to PyPI

This guide assumes you have a PyPI account and the necessary tools (`build`, `twine`) installed.

## Prerequisites

1.  **Install Build Tools:**
    ```bash
    pip install build twine
    ```

2.  **Verify Code:**
    Ensure all tests pass and the code is clean.

## Building the Package

1.  Navigate to the package directory:
    ```bash
    cd imagecorruptions_package
    ```

2.  Build the source distribution and wheel:
    ```bash
    python -m build
    ```
    This will create a `dist/` directory containing `.tar.gz` and `.whl` files.

## Testing the Build (Optional but Recommended)

1.  Create a virtual environment:
    ```bash
    python -m venv test_env
    source test_env/bin/activate
    ```

2.  Install the built package:
    ```bash
    pip install dist/imagecorruptions-1.1.2-py3-none-any.whl
    ```

3.  Verify imports and usage in a python shell.

## Publishing to PyPI

1.  **Test PyPI (First time):**
    Upload to Test PyPI to ensure everything looks correct.
    ```bash
    python -m twine upload --repository testpypi dist/*
    ```
    Check the page on `test.pypi.org`.

2.  **Production PyPI:**
    Upload to the real PyPI.
    ```bash
    python -m twine upload dist/*
    ```
    You will be prompted for your username (usually `__token__`) and password (your API token).

## Updating the Package

1.  Increment the `version` in `pyproject.toml`.
2.  Clean the `dist/` directory: `rm -rf dist/*`.
3.  Re-run the build and upload steps.
