# [TFM]Recommendation engine for ecommerce scenarios
Custom Recomendator for my Master Final Project.

- Hybrid recommendator that combines the power of text and images, this gives full personalitzation.
- I did the project using Python, Keras nad tensorflow.
- Data scrapped from ecommerce WebPage.

## Overview

Recommendation engine for ecommerce scenarios is a project that gathers all the workflow that a custom recommendator must have in order to make sure we  give good recommednations to our customers.

![alt text](/Images/ArquitecturaGeneral.PNG "Title")

As input receives the purchase history of customers with their corresponding items, which are received by a Model that generates items candidates to be recommended to each customer. With a much smaller size and a much smaller volume we look at the most outstanding characteristics through the Ranking model that receives the candidates and sorts them from greater to lesser affinity for the customer. In this way we can better manage the training times while we look at all the business characteristics that are important for the recommendation process.

## Getting started

- Project Explanation on [Thesis](https://github.com/EnricRovira/TFM_DNN_Recomendator/blob/master/Thesis.pdf) doc (Spanish)

- Download the code from GitHub:

```bash
git clone https://github.com/EnricRovira/TFM_DNN_Recomendator
cd TFM_DNN_Recomendator
```
- Install the python libraries (3.7) . [See Requirements](https://github.com/EnricRovira/TFM_DNN_Recomendator/blob/master/requirements.txt)

- Go to Data folder and download all the data from the link, dont forget to unzip the images folder:

```bash
cd ./FinalModel/Data/download_data.txt
```
- Go to Models folder and download all the data from the link:

```bash
cd ./FinalModel/Models/download_models.txt
```
- Go to Scripts folder and run the notebooks:

```bash
cd ./FinalModel/Scripts/
```

## Demo

 If you want to test the Demo with my data first follow *Geting Started* steps and later on, proceed as follows:
 
 - Go to Demo folder:
 
 ```bash
cd ./FinalModel/Demo/
```

- Add Flask App to environment:

 ```python
set FLASK_APP=WebService.py
```

- Run WebService App:

 ```python
flask run
```

- Open your browser and go to **localhost:5000**:

## Interface

![alt text](/Images/Interface1.PNG "Int1")
![alt text](/Images/Interface2.PNG "Int2")
![alt text](/Images/Interface3.PNG "Int2")

### Layout

- The index page request the user for a customer and a top N recommendations.
- When the 'enter' button is pressed, the webform send the arguments to the recommendation function that launches the prediction for that customer and gets the historic data and the recommended items.
- The next page is redirected automatically in which we can see the customer historical boughts and the recommendations, with the option to return home.

## References

- [Kschool](https://kschool.com/) [<img src="/Images/logo_kschool.png">](https://www.kschool.com)
- [My Linkedin](https://www.linkedin.com/in/enric-rovira-a30195a1/) [<img src="/Images/logo_linkedin.png">](https://www.linkedin.com/in/enric-rovira-a30195a1/)
