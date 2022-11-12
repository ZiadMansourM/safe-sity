# Safe-City


## 🦦 Abstract
Astigmatism (uh-STIG-muh-tiz-um) a common imperfection in the curvature of the eye that causes blurred distance and near vision. Nearly one in three people experience astigmatism. But when Astigmatism face the challenge of reading a car's number plate, that is one tough nightmare. According to some protocols number plates must be clearly visible from any point that is up to 20 metres from the number plate, and within an arc of 45 degrees from the surface of the number plate above or to either side of the vehicle. Number plates must be readable from a distance of at least 20m. That is not the case for people with Astigmatism. We aspire for a safe-city. Each street will have a small radar that extract number plates along side with time and type of car e.g. diplomatic car or a taxi. This can have so many crucial applications built on top of this. Two of them can be Governmental and Research purposes.

For the governmantal applications we can have a kind of an auto judge for cars fines to check if it is fair. Or, protect people with sight deformation like Astigmatism in case of accidents who won't be able to read number plates or the people who might just forget the numbers because of the chock. But, they will indeed remebmer the physical properties of the car. That will deeply narrow the search domain of the suspect.

`If you torture the data long enough, it will confess` - Ronald H. Coase. We can open these precious data for researchers to find patterns. One of them might be for climate: by calculating the percantage of routes taken by a private car that could have been taken by public transportation and how that could have affected the environment.



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
