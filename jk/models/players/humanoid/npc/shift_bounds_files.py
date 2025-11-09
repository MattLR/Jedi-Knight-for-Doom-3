import re

# === USER CONFIGURATION ===
MD5ANIM_PATH = "BOTH_STAND1.md5anim"   # Input MD5ANIM file
OUTPUT_PATH = "ROOT1.md5anim"  # Output file
Z_OFFSET = 28  # Amount to shift Z up
# ==========================

def shift_bounds_z(md5anim_path, output_path, z_offset):
    with open(md5anim_path, 'r') as f:
        lines = f.readlines()

    in_bounds = False
    new_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("bounds {"):
            in_bounds = True
            new_lines.append(line)
            continue

        if in_bounds:
            if stripped.startswith("}"):
                in_bounds = False
                new_lines.append(line)
                continue

            # Match a bounds line: (minX minY minZ) (maxX maxY maxZ)
            match = re.match(
                r'\(\s*([-.\d]+)\s+([-.\d]+)\s+([-.\d]+)\s*\)\s*\(\s*([-.\d]+)\s+([-.\d]+)\s+([-.\d]+)\s*\)',
                stripped
            )
            if match:
                minX, minY, minZ, maxX, maxY, maxZ = map(float, match.groups())
                minZ += z_offset
                maxZ += z_offset
                new_line = f"\t({minX:.6f} {minY:.6f} {minZ:.6f}) ({maxX:.6f} {maxY:.6f} {maxZ:.6f})\n"
                new_lines.append(new_line)
            else:
                # Preserve any non-matching line inside bounds
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open(output_path, 'w') as f:
        f.writelines(new_lines)

    print(f"✅ Shifted bounds Z by {z_offset} and saved to {output_path}")


if __name__ == "__main__":
    shift_bounds_z(MD5ANIM_PATH, OUTPUT_PATH, Z_OFFSET)
