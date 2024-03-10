#####
Clipp
#####

| **Latest Version:** 0.0.1
| **Status:** Unstable, active development


Clipp is a POSIX-compliant, CLI parser library for building CLI interfaces,
designed to be flexible, intelligent, and uncompormisingly simple. The
package is similar to argparse but aims to be more intuitive and less
cumbersome. Clipp allows for greater code re-use than argparse and is much
more scalable. In terms of parsing latency, clipp typically outperforms
argparse. Though simpler than arparse, clipp has most of the features you
would expect to find in a command-line parsing library and even adopts much
of argparse's API.

Features
========

- A simple and intuitive API, similar to that of argparse.
- Support for both positional and non-positional arguments, as well as flags.
- Option groups allow for greater code re-use and flexibility.
- Supports mutually exclusive and dependent options.
- Fast flags allow for early-exit function calls.
- Supports standard option escaping with double-dash (--) out of the box.
- Allows the dash character (-) to be used as a valid option alias or
  positional option name
- Supports sub-commands as well as nested sub-commands with the need for
  directly instantiating additional objects.
- Automatic help and usage formatting for top-level commands as well as
  sub-commands.
- Automatic handling of syntax errors encountred at the command-line.
- Automatic data type conversions for consumed arguments.
- Supports post-processing of arguments via callback functions for both
  positional and non-positional options.
- Supports alternative namespace IDs similar to argparse's ``dest`` argument.
- Easily override defaults for help and version info options.

Quickstart
==========

Creating a command is simple.

.. code:: python

   from clipp import Command

   command = Command("sum")

Adding options is just as easy. Let's add a positional option to our command.

.. code:: python

   command.add_parameter(
      "integer",
      quota="*",
      dtype=int,
      action=sum,
      dest="value",
      help="An integer value.",
   )

Clipp refers to positional options as parameters rather than options because
users are typically required to supply arguments to positional options. They
are, therefore, not typically optional. The asterisk (*) supplied above
represents a zero-or-more quota and is one exception to this rule. Parameters
with zero-or-more quotas are technically optional because the parser is
allowed to consume zero arguments. By contrast, the other greedy operator
which may be supplied to ``quota`` is the plus character (+). It represents
one-or-more. Unlike parameters with zero-or-more quotas, parameters with
quotas of one-or-more are not optional.

The parameter we have defined above tells the parser to consume a list of
strings representing integer values, convert those values to type ``int``,
compute the sum of those values, and map the computed sum to the key 'value'
in the namespace object which the parser returns. Let's get familiar with how
to parse arguments by supplying one of the aliases for the default help
option to the command's parse method.

.. code:: python

   command.parse(["--help"])

.. code-block::

   Usage: sum <integer>... [--help]

   Positional Arguments:
   integer               An integer value.

   Options:
   --help, -h            Display this help message.

The default help option is an example of a fast flag. When the parser
encounters an argument token which represents a valid alias for any of its
defined fast flags, it calls that flags callback function and then forces the
script to terminate. By default, the help option's callback function prints
the command's help message to the terminal.

Now that we understand our command's syntax, let's sum a few integers.

.. code:: python

   command.add_parameter(
      ...
      help="An integer value.",
   )
   processed = command.parse(["1", "2", "3"])
   print(processed)

.. code-block::

   Namespace(globals={}, locals={'sum': {'value': 6}}, extra=[])

The ``Namespace`` object returned by the parser is a ``namedtuple`` which has
three fields: ``globals``, ``locals``, and ``extra``. The ``globals`` field
contains all options which are global and are therefore recognized by all
commands in the command hierarchy (a topic we'll touch on shortly). The
``locals`` field is a dictionary containing each of the commands encountered
by the parser and ``extra`` is a list of all positional arguments which were
not consumed by the parser. Each of the nested dictionaries in ``locals``
contains that command's options and thier corresponding values.

In this case, we can see that the computed value for the positional option
'integer' was mapped to its destination (defined by ``dest``) 'value'.
Options which were defined but not encountered by the parser will not appear
in the namespace unless the options was provided a default value. Thus, we
can use membership testing to determine whether a spcific command or option
was invoked at the command-line or otherwise received its default value.

Surely, most utilities will be more complex than the utility we have created
thus far. Perhaps we wish to allow the user of our utility to perform further
computations on the sum.

.. code:: python

   command.add_option(
      "--mod", "-m",
      const=2,
      help="Compute the sum mod N, where N is a valid integer.",
   )
   print(command.format_help())

.. code-block::

   Usage: sum <integer>... [--help] [--mod=<arg>]

   Positional Arguments:
   integer               An integer value.

   Options:
   --help, -h            Display this help message.
   --mod, -m             Compute the sum mod N, where N is a valid
                         integer.

.. code:: python

    def compute_result(namespace: dict) -> int:
         """Compute and return `value` mod N if modulus supplied, else return
         `value`.
         """
         value = namespace["value"]
         if "--mod" in namespace:
             return value % namespace["--mod"]
         return value

    processed = command.parse(["3", "7", "9"])
    result = compute_result(processed.locals["sum"])
    print("Result:", result)

.. code-block::

   Result: 19

In the body of the function ``compute_result``, we do not perform a membership
test for 'value'. This is because options with zero-or-more quotas default to
an empty list when no default value is explicitly provided. Since '--mod' is
not invoked, it does not appear in the ``locals`` namespace, so we return the
value without computing the modulus.

.. code:: python

   processed = command.parse(["3", "7", "9", "--mod"])
   result = compute_result(processed.locals["sum"])
   print("Result:", result)

.. code-block::

   Result: 1

In the example above, we invoke '--mod' but do not provide an argument. Since
we explicitly passed ``const`` as an argument when adding the option, the value
of ``const`` is used as the option's argument, and we are able to compute the
sum mod ``const``.
