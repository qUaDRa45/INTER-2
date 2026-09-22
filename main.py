import sys
import argparse
import re

def parse_point(s):
    # Регулярка для Point(x, y), поддерживает целые и дробные числа с минусом
    m = re.fullmatch(r'Point\(\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)', s.strip())
    if m:
        return ("Point", float(m.group(1)), float(m.group(2)))
    return None

def parse_line(s):
    # Ищем Line(Point(...), Point(...))
    m = re.fullmatch(r'Line\(\s*(Point\(.*?\))\s*,\s*(Point\(.*?\))\s*\)', s.strip())
    if not m:
        return None
    p1 = parse_point(m.group(1))
    p2 = parse_point(m.group(2))
    if p1 is None or p2 is None:
        return None
    return ('Line', p1, p2)

def parse_circle(s):
    # Ищем Circle(Point(...), радиус)
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
    if line.startswith("Point"):
        return parse_point(line)
    if line.startswith("Line"):
        return parse_line(line)
    if line.startswith("Circle"):
        return parse_circle(line)
    return None

def format_point(p):
    return f"Point({p[1]}, {p[2]})"

def format_object(obj):
    if obj[0] == 'Point':
        return format_point(obj)
    if obj[0] == 'Line':
        return f"Line({format_point(obj[1])}, {format_point(obj[2])})"
    if obj[0] == 'Circle':
        return f"Circle({format_point(obj[1])}, {obj[2]})"
    return str(obj)

def read_file(path):
    objects = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                obj = parse_object(line)
                # Некорректные строки просто игнорируются
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
    parser = argparse.ArgumentParser(description="Обработка геометрических фигур из файла")
    parser.add_argument('-f', '--file', required=True, help='путь к файлу')
    parser.add_argument('-o', '--oper', required=True, choices=['print', 'count'], help='операция: print или count')
    args = parser.parse_args()

    objects = read_file(args.file)

    if args.oper == 'count':
        print(len(objects))
    elif args.oper == 'print':
        for obj in objects:
            print(format_object(obj))

if __name__ == "__main__":
    main()