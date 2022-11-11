# safe-sity

## Store in DB Info about Car , Time, Location


![Blankdiagram](https://user-images.githubusercontent.com/62894826/201432682-3ab7ae63-0ffc-461f-8cbb-d0a0c4fc2b9a.png)


- Image Pre-Processing

  - RGB -> Grey Scale
  - Noise Reduction with Edge Preservation
  - Contrast Enhancement with Histogram Equalization

- Plate Area Extraction and Correction
- Number Plate Extraction
- Character Plate Extraction
- Colour Plate Extraction

## Appeal the violation in Traffic System

- Take Info (Plate Info , Number of violation)
- Search in DB stored if this Plate was actually in this location or not
- If after matching the plate was found somewhere else the car fine is removed
