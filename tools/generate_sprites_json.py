#!/usr/bin/env python3
"""
generate_sprites_json.py
- 설명: 스프라이트 시트(투명 배경 PNG)를 분석하여 각 비어있지 않은(투명 아님) 연결 영역의 바운딩 박스(x,y,width,height)를 찾아 JSON으로 내보냅니다.
- 출력 JSON 형식은 사용자가 첨부한 예시('sprites' 배열, spriteSheetWidth/Height 등)를 따릅니다.
- 사용법:
  [자동 모드] python generate_sprites_json.py input_sheet.png output.json [--prefix name_prefix] [--padding N] [--min-area N]
  [그리드 모드] python generate_sprites_json.py input_sheet.png output.json --grid COLS ROWS [--prefix name_prefix] [--padding N]

  예: python generate_sprites_json.py sprites/player/texture2d/player_attack/penintent_attack_combo_anim.png sprites/player/texture2d/player_attack/penintent_attack_combo_anim.json --grid 6 5 --prefix penitent_three_hits_attack_combo_no_slashes --padding 10

주의: 이 스크립트는 Pillow (PIL) 설치가 필요합니다: pip install pillow
"""

from PIL import Image
from collections import deque
import json
import sys
import os


def find_connected_components(img, alpha_threshold=0, padding=0, min_area=0):
    """이미지(RGBA)의 알파 채널을 이용해 4-연결 구성요소의 바운딩 박스를 반환합니다.
    반환값: list of (x, y, w, h)
    좌표계: (0,0) = 이미지 왼쪽 위
    """
    w, h = img.size
    a = img.split()[-1]
    mask = a.point(lambda p: 1 if p > alpha_threshold else 0)
    pixels = mask.load()

    visited = [[False] * w for _ in range(h)]
    boxes = []

    for yy in range(h):
        for xx in range(w):
            if pixels[xx, yy] and not visited[yy][xx]:
                # BFS
                q = deque()
                q.append((xx, yy))
                visited[yy][xx] = True
                minx = xx; maxx = xx
                miny = yy; maxy = yy
                while q:
                    cx, cy = q.popleft()
                    # update bounds
                    if cx < minx: minx = cx
                    if cx > maxx: maxx = cx
                    if cy < miny: miny = cy
                    if cy > maxy: maxy = cy
                    # neighbors 4-way
                    for nx, ny in ((cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)):
                        if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx] and pixels[nx, ny]:
                            visited[ny][nx] = True
                            q.append((nx, ny))
                # expand padding and clamp
                minx = max(0, minx - padding)
                miny = max(0, miny - padding)
                maxx = min(w-1, maxx + padding)
                maxy = min(h-1, maxy + padding)

                area = (maxx - minx + 1) * (maxy - miny + 1)
                if area >= min_area:
                    boxes.append((minx, miny, maxx - minx + 1, maxy - miny + 1))
    return boxes


def extract_grid_frames(img, cols, rows, padding=0):
    """그리드 기반으로 스프라이트 시트를 분할합니다.
    각 셀에서 투명하지 않은 영역의 바운딩 박스를 찾습니다.
    반환값: list of (x, y, w, h)
    """
    sheet_w, sheet_h = img.size
    cell_w = sheet_w // cols
    cell_h = sheet_h // rows

    boxes = []
    for row in range(rows):
        for col in range(cols):
            # 셀의 영역 계산
            cell_x = col * cell_w
            cell_y = row * cell_h

            # 셀 영역 자르기
            cell = img.crop((cell_x, cell_y, cell_x + cell_w, cell_y + cell_h))

            # 셀 내에서 투명하지 않은 영역 찾기
            a = cell.split()[-1]
            pixels = a.load()

            minx, miny = cell_w, cell_h
            maxx, maxy = 0, 0
            found = False

            for y in range(cell_h):
                for x in range(cell_w):
                    if pixels[x, y] > 0:  # 투명하지 않음
                        found = True
                        if x < minx: minx = x
                        if x > maxx: maxx = x
                        if y < miny: miny = y
                        if y > maxy: maxy = y

            if found:
                # 패딩 적용
                minx = max(0, minx - padding)
                miny = max(0, miny - padding)
                maxx = min(cell_w - 1, maxx + padding)
                maxy = min(cell_h - 1, maxy + padding)

                # 전체 시트 좌표로 변환
                abs_x = cell_x + minx
                abs_y = cell_y + miny
                width = maxx - minx + 1
                height = maxy - miny + 1

                boxes.append((abs_x, abs_y, width, height))

    return boxes


def generate_json(image_path, out_path, prefix="frame", padding=0, min_area=0, grid_mode=None):
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size

    if grid_mode:
        cols, rows = grid_mode
        boxes = extract_grid_frames(img, cols, rows, padding=padding)
        pack_mode = "grid"
    else:
        boxes = find_connected_components(img, alpha_threshold=0, padding=padding, min_area=min_area)
        # 정렬: 위에서 아래, 왼쪽에서 오른쪽
        boxes.sort(key=lambda b: (b[1], b[0]))
        pack_mode = "auto"

    sprites = []
    for i, (x, y, bw, bh) in enumerate(boxes, start=1):
        sprites.append({
            "fileName": f"{prefix}_{i}.png",
            "width": int(bw),
            "height": int(bh),
            "x": int(x),
            "y": int(y)
        })

    out = {
        "sprites": sprites,
        "packMode": pack_mode,
        "padding": int(padding),
        "backgroundColor": "rgba(0, 0, 0, 0)",
        "spriteSheetWidth": int(w),
        "spriteSheetHeight": int(h)
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(sprites)} frames to {out_path}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:")
        print("  [Auto mode] python generate_sprites_json.py input.png output.json [--prefix name] [--padding N] [--min-area N]")
        print("  [Grid mode] python generate_sprites_json.py input.png output.json --grid COLS ROWS [--prefix name] [--padding N]")
        print("\nExamples:")
        print("  python generate_sprites_json.py attack.png attack.json --grid 6 5 --prefix attack --padding 10")
        print("  python generate_sprites_json.py idle.png idle.json --prefix idle --padding 2 --min-area 100")
        sys.exit(1)

    image_path = sys.argv[1]
    out_path = sys.argv[2]
    prefix = "frame"
    padding = 0
    min_area = 0
    grid_mode = None

    args = sys.argv[3:]
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--prefix' and i+1 < len(args):
            prefix = args[i+1]; i += 2
        elif a == '--padding' and i+1 < len(args):
            padding = int(args[i+1]); i += 2
        elif a == '--min-area' and i+1 < len(args):
            min_area = int(args[i+1]); i += 2
        elif a == '--grid' and i+2 < len(args):
            cols = int(args[i+1])
            rows = int(args[i+2])
            grid_mode = (cols, rows)
            i += 3
        else:
            i += 1

    generate_json(image_path, out_path, prefix=prefix, padding=padding, min_area=min_area, grid_mode=grid_mode)
