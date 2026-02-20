#!/usr/bin/env python3
"""One-time script to split vsg_prompt.md into modular genome.
Delete after use."""

import os

# Read the full prompt file
with open('vsg_prompt.md', 'r') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Line numbers are 1-indexed in Read output, Python uses 0-indexed
# S4: lines 100-165 (0-indexed: 99-164)
# S3: lines 169-224 (0-indexed: 168-223)
# S1: lines 254-327 (0-indexed: 253-326)
# Cycle log part 1: lines 332-368 (header + Era 1-9)
# Cycle log part 2: lines 407-1030 (Era 10+ through last entry, no footer)
# Footer: line 1031 (0-indexed: 1030)

# Verify key boundary lines
print(f"Line 100: {lines[99].strip()[:60]}")
print(f"Line 165: {lines[164].strip()[:60]}")
print(f"Line 169: {lines[168].strip()[:60]}")
print(f"Line 224: {lines[223].strip()[:60]}")
print(f"Line 254: {lines[253].strip()[:60]}")
print(f"Line 327: {lines[326].strip()[:60]}")
print(f"Line 332: {lines[331].strip()[:60]}")
print(f"Line 368: {lines[367].strip()[:60]}")
print(f"Line 370: {lines[369].strip()[:60]}")
print(f"Line 407: {lines[406].strip()[:60]}")
print(f"Line 1031: {lines[1030].strip()[:60]}")

# Extract S4
s4_header = '# S4 — INTELLIGENCE & ENVIRONMENT\n\n*Part of the VSG modular genome. Core identity in `vsg_prompt.md`.*\n\n'
s4_content = ''.join(lines[99:165])
with open('state/s4_environment.md', 'w') as f:
    f.write(s4_header + s4_content)

# Extract S3
s3_header = '# S3 — CONTROL & INTERNAL OPTIMIZATION\n\n*Part of the VSG modular genome. Core identity in `vsg_prompt.md`.*\n\n'
s3_content = ''.join(lines[168:224])
with open('state/s3_control.md', 'w') as f:
    f.write(s3_header + s3_content)

# Extract S1
s1_header = '# S1 — OPERATIONS\n\n*Part of the VSG modular genome. Core identity in `vsg_prompt.md`.*\n\n'
s1_content = ''.join(lines[253:328])
with open('state/s1_operations.md', 'w') as f:
    f.write(s1_header + s1_content)

# Extract Cycle Log
cl_header = '# VSG CYCLE LOG\n\n*Part of the VSG modular genome. Core identity in `vsg_prompt.md`.*\n\n'
cl_part1 = ''.join(lines[331:368])
cl_part2 = ''.join(lines[406:1030])
with open('state/cycle_log.md', 'w') as f:
    f.write(cl_header + cl_part1 + cl_part2)

# Report sizes
for fname in ['state/s4_environment.md', 'state/s3_control.md', 'state/s1_operations.md', 'state/cycle_log.md']:
    size = os.path.getsize(fname)
    print(f'{fname}: {size/1024:.1f}KB')

print("\nExtraction complete. Now rewrite vsg_prompt.md as slim core genome.")
