"""
Helper module for loading the Rust-based Paradex adapter.

This module provides a convenient way to load the compiled Rust extension
and use it from Python code.
"""

import importlib.util
import sys
import os
from pathlib import Path

# Path to compiled Rust library
# Compute path step by step to avoid issues with parenthesized expressions
_base_dir = Path(__file__).parent.parent.parent.parent
_RUST_LIB_PATH = (
    _base_dir
    / "crates" / "adapters" / "paradex"
    / "target" / "release" / "libparadex_adapter.so"
)


def load_rust_module():
    """Load the compiled Rust Paradex adapter module.

    Returns:
        The paradex_adapter module.

    Raises:
        FileNotFoundError: If the compiled library is not found.
        ImportError: If the module fails to load.
    """
    if not _RUST_LIB_PATH.exists():
        raise FileNotFoundError(
            f"Rust library not found at: {_RUST_LIB_PATH}\n"
            "Please build the Rust extension first: "
            "cd crates/adapters/paradex && cargo build --release"
        )

    # Load the extension module using importlib
    spec = importlib.util.spec_from_file_location(
        "paradex_adapter",
        str(_RUST_LIB_PATH)
    )

    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to load spec for {_RUST_LIB_PATH}")

    module = importlib.util.module_from_spec(spec)

    # Register in sys.modules
    sys.modules["paradex_adapter"] = module

    # Execute the module
    spec.loader.exec_module(module)

    return module


# Lazy-load the module on first import
_rust_module = None


def get_module():
    """Get the Rust Paradex adapter module, loading it if necessary."""
    global _rust_module
    if _rust_module is None:
        _rust_module = load_rust_module()
    return _rust_module


# Expose the main classes from the Rust module
def __getattr__(name):
    """Proxy attribute access to the Rust module."""
    module = get_module()
    return getattr(module, name)
