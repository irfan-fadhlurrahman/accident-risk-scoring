## Accident Risk Index Scoring
As stated by IBEF, in the fiscal year between 2016 and 2020, domestic automobiles production and sales increased at 2.36% and 1.29% CAGR respectively. In India, in fiscal year 2020, the number of vehicle sales are around 20 million which contribute to the increase of vehicles. This increase can make the road more vulnerable to accidents that leads to more insurance claims and payout rise to the company. In order to plan the losses in advance, the insurance company must the past accident data to understand the risk across the geographical units i.e postal code [[source](https://machinehack.com/hackathon/predict_accident_risk_score_for_unique_postcode/data)]. 

### Objective
The aim of this project is to predict the Accident Risk Index that is the average of casualties per postal code, based on location, time, and other conditions data.
This is a regression task, which predicts the continuous value target. To evaluate the model performance, root mean squared error (RMSE) will be used.

### Benefit
Being able to calculate the risk of accidents in each postal code region, the insurance company can reduce the losses due to the surging rise in insurance claims.

### Data Source
The dataset can be downloaded from this [link](https://machinehack.com/hackathon/predict_accident_risk_score_for_unique_postcode/overview). This dataset was used for competition in Machine Hack. There are 5 files in the dataset, consisting of train.csv, test.csv, sample_submission.csv and 2 optional files such as population.csv and fileroads_network.csv. To simplify the analysis, the dataset that will be used only train.csv and test.csv. 

The train and test dataset have 600,000 total observations with ratio 80% train and 20% test set.  There are 27 variables in this dataset. But, in this notebook, I only use 18 variables because 10 other variables do not have a clear explanation and make the model less complex.

### Exploratory Data Analysis
#### Target Variable
* The accident risk index ranges from 1 to 5 with approximately 95% of observations are in range 1 to 2.

#### Distribution
* Number of vehicles that were involved in accidents varied from 1 to 4 with approximately 93% of accidents involving at least one vehicle.
* 68.9% of accidents occured in the road with speed limit 30, while only 3.4% accidents occurred with speed limit 70.
* Around 68% accidents caused only one casualty, while almost 21% accidents caused two casualties.

#### Recommendation
* Charge more to the people who subscribe the insurance if they have similar attributes or profiles with the one who has a higher accident risk index, so that the insurance company can reduce the losses if the insurance claims are increasing in certain regions.