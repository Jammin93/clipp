"""
A POSIX-compliant, CLI parser library for building CLI interfaces, designed
to be flexible, intelligent, and uncompromisingly simple. Clipp aims to make
code more reusable and easily scalable, without compromising performance.
"""
from clipp.core import Command, OptionGroup, NULL

__author__ = "Ben Ohling"
__copyright__ = f"Copyright (C) 2024, {__author__}"
__version__ = "0.0.1"
__all__ = ["Command", "OptionGroup", "NULL"]