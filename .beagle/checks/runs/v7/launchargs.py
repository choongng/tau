"""Split a `printf %q` command line into argv as bytes.

shlex cannot read bash's $'...' quoting, which printf %q uses for strings
with newlines, so this handles the three forms %q emits: backslash-escaped
bare words, '...' and $'...'.
"""
import sys

_SIMPLE = {"n": b"\n", "t": b"\t", "r": b"\r", "a": b"\a", "b": b"\b",
           "f": b"\f", "v": b"\v", "e": b"\x1b", "E": b"\x1b",
           "\\": b"\\", "'": b"'", '"': b'"', "?": b"?"}


def split(line):
    args, cur, have, i, n = [], bytearray(), False, 0, len(line)
    while i < n:
        c = line[i]
        if c in " \t\n":
            if have:
                args.append(bytes(cur))
                cur, have = bytearray(), False
            i += 1
        elif c == "\\":
            cur += line[i + 1].encode(); have = True; i += 2
        elif c == "'":
            j = line.index("'", i + 1)
            cur += line[i + 1:j].encode(); have = True; i = j + 1
        elif c == "$" and line[i + 1:i + 2] == "'":
            i += 2; have = True
            while line[i] != "'":
                if line[i] != "\\":
                    cur += line[i].encode(); i += 1; continue
                e = line[i + 1]
                if e in _SIMPLE:
                    cur += _SIMPLE[e]; i += 2
                elif e in "01234567":
                    k = i + 1
                    while k < i + 4 and k < n and line[k] in "01234567":
                        k += 1
                    cur.append(int(line[i + 1:k], 8) & 0xFF); i = k
                elif e == "x":
                    k = i + 2
                    while k < i + 4 and k < n and line[k] in "0123456789abcdefABCDEF":
                        k += 1
                    cur.append(int(line[i + 2:k], 16)); i = k
                elif e in "uU":
                    w = 4 if e == "u" else 8
                    k = i + 2
                    while k < i + 2 + w and k < n and line[k] in "0123456789abcdefABCDEF":
                        k += 1
                    cur += chr(int(line[i + 2:k], 16)).encode(); i = k
                else:
                    cur += b"\\" + e.encode(); i += 2
            i += 1
        elif c == '"':
            raise ValueError("double quotes are not printf %q output")
        else:
            cur += c.encode(); have = True; i += 1
    if have:
        args.append(bytes(cur))
    return args


if __name__ == "__main__":
    for a in split(sys.argv[1]):
        print(repr(a))
