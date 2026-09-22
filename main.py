import sys
import argparse
import re

def parse_point(s):
    m = re.fullmatch(r'Point\(\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)', s.strip())
    if m:
        return ("Point", float(m.group(1)), float(m.group(2)))
    return None

def parse_line(s):
    m = re.fullmatch(r'Line\(\s*(Point\(.*?\))\s*,\s*(Point\(.*?\))\s*\)', s.strip())
    if not m:
        return None
    p1 = parse_point(m.group(1))
    p2 = parse_point(m.group(2))
    if p1 is None or p2 is None:
        return None
    return ('Line', p1, p2)

def parse_circle(s):
    m = re.fullmatch(r'Circle\(\s*(Point\(.*?\))\s*,\s*(-?\d+\.?\d*)\s*\)', s.strip())
    if not m:
        return None
    center = parse_point(m.group(1))
    if center is None:
        return None
    return ('Circle', center, float(m.group(2)))

def parse_object(line):
    line = line.strip()
    if not line:
        return None

    color = None
    color_match = re.search(r'Color\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$', line)
    if color_match:
        r = int(color_match.group(1))
        g = int(color_match.group(2))
        b = int(color_match.group(3))
        color = (r, g, b)
        line = line[:color_match.start()].strip()

    obj = None
    if line.startswith("Point"):
        obj = parse_point(line)
    elif line.startswith("Line"):
        obj = parse_line(line)
    elif line.startswith("Circle"):
        obj = parse_circle(line)

    if obj is not None:
        return (obj[0], obj[1], obj[2], color)

    return None

def format_point(p):
    return f"Point({p[1]}, {p[2]})"

def format_object(obj):
    color = obj[3]
    if color is not None:
        color_str = f" Color({color[0]}, {color[1]}, {color[2]})"
    else:
        color_str = ""

    if obj[0] == 'Point':
        res = format_point(obj)
    elif obj[0] == 'Line':
        res = f"Line({format_point(obj[1])}, {format_point(obj[2])})"
    elif obj[0] == 'Circle':
        res = f"Circle({format_point(obj[1])}, {obj[2]})"
    else:
        res = str(obj)

    return res + color_str

def read_file(path):
    objects = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                obj = parse_object(line)
                if obj is not None:
                    objects.append(obj)
    except FileNotFoundError:
        print("Ошибка: файл не найден", file=sys.stderr)
        sys.exit(1)
    except OSError:
        print("Ошибка чтения файла", file=sys.stderr)
        sys.exit(1)
    return objects

def main():
    parser = argparse.ArgumentParser(description="Обработка файла")
    parser.add_argument('-f', '--file', required=True, help='путь к файлу')
    parser.add_argument('-o', '--oper', required=True, choices=['print', 'count', 'rem'], help='операция: print, count или rem')
    parser.add_argument('-c', '--color', required=False, help='цвет в формате RGB')
    args = parser.parse_args()
    objects = read_file(args.file)
    target_color = None
    if args.color:
        parts = args.color.split(',')
        if len(parts) == 3:
            target_color = (int(parts[0]), int(parts[1]), int(parts[2]))
        else:
            print("Ошибка: цвет должен быть в формате RGB", file=sys.stderr)
            sys.exit(1)
            return

    if args.oper == 'count':
        print(len(objects))

    elif args.oper == 'print':
        for obj in objects:
            if target_color:
                if obj[3] == target_color:
                    print(format_object(obj))
            else:
                print(format_object(obj))

    elif args.oper == 'rem':
        if target_color is None:
            print("Ошибка: для удаления укажите цвет через -c)", file=sys.stderr)
            sys.exit(1)

        objects = [obj for obj in objects if obj[3] != target_color]
        for obj in objects:
            print(format_object(obj))

if __name__ == "__main__":
    main()
