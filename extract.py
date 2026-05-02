import cv2
import numpy as np
import os
import math

img_path = r"C:\Users\MAPFRE\.gemini\antigravity\brain\0cc474c9-6460-4ff2-8e12-3b87efd38b4f\media__1777750878485.jpg"
out_dir = r"C:\Users\MAPFRE\.gemini\antigravity\scratch\historia-saul-ninos\imagenes"

os.makedirs(out_dir, exist_ok=True)

image = cv2.imread(img_path)
if image is None:
    print("Error: Could not read image.")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Find white borders. The borders are around 255. 
_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

bboxes = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    # Ignore small artifacts or full image bounds just in case
    if w > 100 and h > 100 and w < image.shape[1]*0.9:
        bboxes.append((x, y, w, h))

# Sort bounding boxes top-to-bottom, then left-to-right
# Group by rows based on Y coordinate matching within a tolerance
bboxes.sort(key=lambda b: b[1])

rows = []
current_row = []
current_y = None
row_tolerance = 50

for b in bboxes:
    if current_y is None:
        current_y = b[1]
        current_row.append(b)
    else:
        if abs(b[1] - current_y) < row_tolerance:
            current_row.append(b)
        else:
            # Sort current row strictly left to right
            current_row.sort(key=lambda x: x[0])
            rows.append(current_row)
            current_row = [b]
            current_y = b[1]

if current_row:
    current_row.sort(key=lambda x: x[0])
    rows.append(current_row)

print(f"Found {len(rows)} rows.")

# Known mapping based on reading order from user prompt
# Row 0: 1, 2, 3, 4, 5
# Row 1: 6, 7, 8, 9, 10
# Row 2: 11, 12, 16
# Row 3: 13, 14, 15, 17
ordered_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 13, 14, 15, 17]

idx = 0
for row_idx, row in enumerate(rows):
    print(f"Row {row_idx} has {len(row)} images.")
    for b in row:
        x, y, w, h = b
        crop = image[y:y+h, x:x+w]
        if idx < len(ordered_ids):
            out_name = f"slide_{ordered_ids[idx]}.jpg"
        else:
            out_name = f"extra_{idx}.jpg"
        cv2.imwrite(os.path.join(out_dir, out_name), crop)
        print(f"Saved {out_name}")
        idx += 1
