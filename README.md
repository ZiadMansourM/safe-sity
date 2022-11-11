# safe-sity

## Store in DB Info about Car , Time, Location

![Blankdiagram1](https://user-images.githubusercontent.com/62894826/201434012-e4d6d869-4cb7-49f2-85a5-6763c1b3d615.png)

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

- Return imahe to RGB
- Use a certain part in the cropped image where the colour could be and take the colour of surrounding pixels
- Store colour in DB

## Appeal the violation in Traffic System

- Take Info (Plate Info , Number of violation)
- Search in DB stored if this Plate was actually in this location or not
- If after matching the plate was found somewhere else the car fine is removed
