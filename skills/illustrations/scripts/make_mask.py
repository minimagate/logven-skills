import os
import struct
import subprocess
import sys
import tempfile
import zlib

MAX_EDGE = 840
WHITE = 232
INK = 45
TRIM_ALPHA = 40
LIGHT_PREVIEW = ((0x15, 0x16, 0x19), (0xFF, 0xFF, 0xFF))
DARK_PREVIEW = ((0xEC, 0xEE, 0xF3), (0x1A, 0x1B, 0x1F))


def resized(source, directory):
    target = os.path.join(directory, "resized.png")
    subprocess.run(["sips", "-Z", str(MAX_EDGE), source, "--out", target], check=True, capture_output=True)
    return target


def read_png(path):
    with open(path, "rb") as handle:
        data = handle.read()

    position, compressed = 8, bytearray()
    while position < len(data):
        length, kind = struct.unpack(">I4s", data[position : position + 8])
        chunk = data[position + 8 : position + 8 + length]
        if kind == b"IHDR":
            width, height, depth, color, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
            if depth != 8 or interlace != 0 or color not in (2, 6):
                sys.exit(f"unsupported PNG: depth {depth}, color {color}, interlace {interlace}")
        elif kind == b"IDAT":
            compressed += chunk
        position += 12 + length

    channels = 4 if color == 6 else 3
    raw = zlib.decompress(bytes(compressed))
    stride = width * channels
    previous = bytearray(stride)
    rows = []
    offset = 0
    for _ in range(height):
        kind = raw[offset]
        row = bytearray(raw[offset + 1 : offset + 1 + stride])
        offset += stride + 1
        if kind == 1:
            for i in range(channels, stride):
                row[i] = (row[i] + row[i - channels]) & 255
        elif kind == 2:
            for i in range(stride):
                row[i] = (row[i] + previous[i]) & 255
        elif kind == 3:
            for i in range(stride):
                left = row[i - channels] if i >= channels else 0
                row[i] = (row[i] + (left + previous[i]) // 2) & 255
        elif kind == 4:
            for i in range(stride):
                a = row[i - channels] if i >= channels else 0
                b = previous[i]
                c = previous[i - channels] if i >= channels else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                predictor = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                row[i] = (row[i] + predictor) & 255
        rows.append(row)
        previous = row
    return width, height, channels, rows


def write_png(path, width, height, rows):
    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))

    raw = b"".join(b"\x00" + bytes(row) for row in rows)
    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    with open(path, "wb") as handle:
        handle.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def clamp(value):
    return max(0, min(255, int(round(value))))


def mask_of(width, channels, rows):
    masks = []
    for row in rows:
        mask = bytearray(width * 4)
        for x in range(width):
            i = x * channels
            level = (row[i] + row[i + 1] + row[i + 2]) / 3
            mask[x * 4 + 3] = clamp((WHITE - level) * 255 / (WHITE - INK))
        masks.append(mask)
    return masks


def trimmed(width, height, masks):
    columns = [x for x in range(width) if any(row[x * 4 + 3] > TRIM_ALPHA for row in masks)]
    lines = [y for y in range(height) if any(masks[y][x * 4 + 3] > TRIM_ALPHA for x in range(0, width, 2))]
    if not columns or not lines:
        sys.exit("nothing drawn: the image is blank after masking")
    left, right, top, bottom = columns[0], columns[-1] + 1, lines[0], lines[-1] + 1
    return right - left, bottom - top, [row[left * 4 : right * 4] for row in masks[top:bottom]]


def preview(masks, ink, paper):
    output = []
    for row in masks:
        flat = bytearray(len(row))
        for i in range(0, len(row), 4):
            alpha = row[i + 3] / 255
            for c in range(3):
                flat[i + c] = clamp(ink[c] * alpha + paper[c] * (1 - alpha))
            flat[i + 3] = 255
        output.append(flat)
    return output


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: make_mask.py <drawing.png> <output-stem>")
    source, target = sys.argv[1], sys.argv[2]

    with tempfile.TemporaryDirectory() as directory:
        width, height, channels, rows = read_png(resized(source, directory))

    trimmed_width, trimmed_height, masks = trimmed(width, height, mask_of(width, channels, rows))
    write_png(f"{target}.png", trimmed_width, trimmed_height, masks)
    write_png(f"{target}-preview-light.png", trimmed_width, trimmed_height, preview(masks, *LIGHT_PREVIEW))
    write_png(f"{target}-preview-dark.png", trimmed_width, trimmed_height, preview(masks, *DARK_PREVIEW))
    print(f"{target}.png {trimmed_width}x{trimmed_height}")


main()
