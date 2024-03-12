"""Strip all "+SKIP" directives from readme-doctest.rst."""


def main():
    with open("readme-doctest.rst", "r") as f:
        lines = f.readlines()
        undoctest = False
        start = "# <undoctest>"
        end = "# </undoctest>"
        for i, ln in enumerate(lines):
            ln = ln.replace("# doctest: +SKIP", "").rstrip(" ")
            if undoctest:
                ln = ln.replace(">>> ", "")
                if end in ln:
                    ln = ln.replace(end, "").rstrip()
                    if ln.strip() == "":
                        lines[i] = None

                    undoctest = False
                else:
                    lines[i] = ln
            elif start in ln:
                ln = ln.replace(">>> ", "")
                ln = ln.replace(start, "").rstrip()
                if ln.strip() == "":
                    lines[i] = None
                else:
                    lines[i] = ln

                undoctest = True
            else:
                lines[i] = ln

    lines = [ln for ln in lines if ln is not None]
    with open("README.rst", "w") as f:
        f.write("".join(lines))


if __name__ == "__main__":
    main()
