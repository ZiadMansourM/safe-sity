# safe-sity

## Store in DB Info about Car , Time, Location

![Blankdiagram](https://user-images.githubusercontent.com/62894826/201432682-3ab7ae63-0ffc-461f-8cbb-d0a0c4fc2b9a.png)

1- Image Pre-Processing

- RGB -> Grey Scale
- Noise Reduction with Edge Preservation
- Contrast Enhancement with Histogram Equalization

2- Plate Area Extraction and Correction

- Errorsion and Dilation
- Image Thresholding
- Skew Correction (fix angle of the image to meet our target area)
- Contouring
- Extract Box currounding Plate Number and Characters
- Cropping Region for Plate

3- Number Plate Extraction

- Use SE matrix to extract numbers from the Plate

4- Character Plate Extraction

- Use SE matrix to extract characters from the Plate

5- Colour Plate Extraction

## Appeal the violation in Traffic System

- Take Info (Plate Info , Number of violation)
- Search in DB stored if this Plate was actually in this location or not
- If after matching the plate was found somewhere else the car fine is removed
