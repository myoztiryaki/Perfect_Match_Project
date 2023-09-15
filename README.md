![logo](https://github.com/myoztiryaki/Perfect_Match_Project/blob/master/assets/pmlogo.png)

# PERFECT MATCH

## Astrological Relationship Compatibility By JR.Eros

### Purpose of The Project 
**Predicting relationship compatibility between people based on their birth dates.**

Predicting whether the two people to be examined are soul mates/twin flame or not, based on the date, time, and place of birth information entered by the user, and give the score of their relationship compatibility.

## Project Steps

### BACKEND

#### API

Birth Chart - Astrology API: astrologyapi.com

We created a data frame by taking the birth chart data of two people from the API. We put this DataFrame through data pre-processing steps and produced new magical astrological features that will be important for relationship compatibility.

**from API variables**
- "Sun"
- "Moon"
- "Venus"
- "Mars"
- "Mercury"
- "Jupiter"
- "Saturn"
- "Neptune"
- "Uranus"
- "Pluto"
- "Chiron"
- "Node"

### DATA PROCESSING & FEATURES EXTRACTION

**Produced variables**
- "SNode"
- "MC"
- "IC"
- "ASC"
- "DSC"
- "Juno"

Create a new DF: The angles of the two people's planets to each other were calculated.

Relationship Analysis: We created a form and collected couples' birth date data. 

Sinastri Excel: Training set that will enable the model to learn magic formulas about soul mate, twinflame and relationship harmony.

After training our model with the data, we developed a system that gives relationship compatibility results according to the date of birth information entered by the user from the interface.


### FRONTEND

### Streamlit

We decided to present it to users with an interface using Streamlit. There are fields on the user interface to enter the birth date information of two people. The information going backend from the Streamlit service is processed and the prediction result is presented to the user through the Streamlit interface.

![streamlit](https://github.com/myoztiryaki/Perfect_Match_Project/blob/master/assets/perfectmatcheros.JPG)


## Team Members 

- ### Merve Öztiryaki

<a target="_blank" href="https://www.linkedin.com/in/merveoztiryaki"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white"></img></a>
<a target="_blank" href="https://www.kaggle.com/merveoztiryaki"><img src="https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white"></img></a>
<a target="_blank" href="https://medium.com/@myoztiryaki"><img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white"></img></a>


- ### Elif Kızıl

<a target="_blank" href="https://www.linkedin.com/in/elif-kizil/"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white"></img></a>
<a target="_blank" href="https://www.kaggle.com/elifkzl"><img src="https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white"></img></a>


- ### Aleyna Sözer

<a target="_blank" href="https://www.linkedin.com/in/aleynasozer/"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white"></img></a>
<a target="_blank" href="https://www.kaggle.com/aleynaszer"><img src="https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white"></img></a>

- ### Ahmet Onat Türk

<a target="_blank" href="https://www.linkedin.com/in/ahmet-onat-turk/"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white"></img></a>
<a target="_blank" href="https://www.kaggle.com/onatturk"><img src="https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white"></img></a>






