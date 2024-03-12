"""Strip all "+SKIP" directives from readme-doctest.rst."""


def main():
    with open("readme-doctest.rst", "r") as f:
        lines = [ln.replace("\n", "") for ln in f.readlines()]
        for i, ln in enumerate(lines):
            lines[i] = ln.replace("# doctest: +SKIP", "").rstrip(" ")

    with open("README.rst", "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
