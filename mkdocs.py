"""Strip all "+SKIP" directives from readme-doctest.rst."""


def main():
    with open("readme-doctest.rst", "r") as f:
        lines = f.readlines()
        for i, ln in enumerate(lines):
            ln = ln.replace("# doctest: +SKIP", "").rstrip(" ")
            lines[i] = ln

    with open("README.rst", "w") as f:
        f.write("".join(lines))


if __name__ == "__main__":
    main()
