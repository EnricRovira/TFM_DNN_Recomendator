# [TFM]Recommendation engine for ecommerce scenarios
Custom Recomendator for my Master Final Project.

- Hybrid recommendator that combines the power of text and images, this gives full personalitzation.
- I did the project using Python, pandas, scikit-learn and Keras.
- Data scrapped from ecommerce WebPage and not shared

## Overview

Recommendation engine for ecommerce scenarios is a project that gathers all the workflow that a custom recommendator must have in order to make sure we  give good recommednations to our customers.

![alt text](ArquitecturaGeneral.PNG "Title")

As input receives the purchase history of customers with their corresponding items, which are received by a Model that generates items candidates to be recommended to each customer. With a much smaller size and a much smaller volume we look at the most outstanding characteristics through the Ranking model that receives the candidates and sorts them from greater to lesser affinity for the customer. In this way we can better manage the training times while we look at all the business characteristics that are important for the recommendation process.

## Getting started

- Install the python libraries (3.7) . [See Requirements](https://github.com/EnricRovira/TFM_DNN_Recomendator/requirements.txt)



