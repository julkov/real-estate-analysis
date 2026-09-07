# Property Price Prediction Model

## Project Goal

One of the goals of the project was to create a model that can predict the price of a property based on information about the property. The data comes from property listings and contains information such as the city, property type, and surface area.

The problem can therefore be described in a simple way:

> **If we know some basic information about a property, can we use it to estimate its price?**

To solve this problem, machine learning methods were used. The main model analyzed in the project was a **Random Forest Regressor**.

## What Data Does the Model Use?

Before training the model, the data was prepared appropriately. The model uses three main pieces of information describing a property:

- **city**,
- **property type**,
- **surface area**.

The value that the model tries to predict is the **property price**.

Information about the city and property type is initially stored as text. However, a machine learning model cannot directly work with values such as `"Amsterdam"` or `"HOUSE"`. Therefore, these categories were converted into numerical values using a technique called **One-Hot Encoding**.

For example, instead of having one column:

```text
city = Amsterdam
```

the model receives information in the form of:

```text
city_Amsterdam = 1
city_Rotterdam = 0
city_Utrecht = 0
...
```

The 14 most frequently occurring cities were included separately. All remaining cities were combined into one category called `other`.

## Data Preparation

Before training the models, the dataset was checked for missing values and basic statistical properties.

One record was also removed because it was treated as an extreme case that could negatively affect the analysis.

The data was then prepared for machine learning by converting categorical variables into numerical ones.

The relationship between surface area and price was also examined. This is particularly interesting for property data because larger properties are generally expected to have higher prices.

Several diagnostic plots were created as well, including a price distribution histogram, a boxplot of prices, and a plot showing the relationship between surface area and price.

## What Is Random Forest?

Random Forest is a machine learning method based on **decision trees**.

A single decision tree can be imagined as a sequence of questions that eventually leads to an answer. For example, a model could learn rules similar to:

```text
Is the property larger than 70 m²?
        |
       YES
        |
Is it located in Amsterdam?
        |
       YES
        |
   predicted price
```

In reality, the trees used by the model are much more complex and can use many different combinations of features.

Random Forest does not rely on just one tree. Instead, it creates **many decision trees** and combines their predictions.

This can be compared to asking a large group of people for their opinions instead of relying on just one person. A single opinion may be inaccurate, but combining many opinions can produce a more stable result.

The Random Forest model used in this project consists of **100 decision trees**.

## Why Were Several Models Tested?

Random Forest was not the only model tested in the project. Several different regression methods were compared in order to find a suitable solution.

The experiment included:

- Linear Regression,
- Random Forest with different parameter settings,
- Ridge Regression,
- Lasso Regression.

All models were evaluated using the same training and test datasets. This makes the comparison more reliable because every model is tested under the same conditions.

The model selected for further analysis was **Random Forest with `min_samples_split=4`**.

This parameter determines how many observations must be present in a tree node for it to be split into smaller nodes. A value of 4 means that a node needs at least four observations to be considered for another split.

## How Does the Model Learn to Predict Prices?

The dataset was divided into two parts:

- **80% training data** – used to teach the model,
- **20% test data** – used to check how well the model performs on properties it has not seen before.

This distinction is important. A model that performs very well on the data it has already seen is not necessarily good at predicting prices for new properties.

This can be compared to studying for an exam. If a student simply memorizes the answers to the exercises used during preparation, they may perform very well on those exact exercises but struggle with new questions. Similarly, a machine learning model should learn general patterns in the data rather than simply memorize individual examples.

## How Is Model Performance Evaluated?

Three main metrics are used to evaluate the models.

### RMSE

**Root Mean Squared Error (RMSE)** measures the size of prediction errors. Larger errors have a greater impact on this metric.

**Lower RMSE means better performance.**

### MAE

**Mean Absolute Error (MAE)** measures the average absolute difference between the predicted and actual values.

For example, if MAE is 10,000, the model's predictions differ from the actual prices by about 10,000 on average.

**Lower MAE means better performance.**

### R²

**R² (coefficient of determination)** describes how well the model explains the variation in property prices.

A value closer to 1 generally indicates better model performance.

All three metrics are calculated for both the training and test datasets.

## Checking for Overfitting

An important part of model evaluation is checking for **overfitting**.

Overfitting occurs when a model performs extremely well on the data used for training but performs significantly worse on new data.

For this reason, the results for the training and test datasets are compared.

The program also calculates the difference between the training and test R² values. If this difference is greater than 0.10, the program reports a warning that the model may be overfitted.

## Does the Amount of Training Data Matter?

The project also examines how the amount of training data affects the performance of the Random Forest model.

The test dataset remains fixed, while the model is trained using different portions of the available training data — from 10% up to 100%.

For each amount of training data, RMSE and MAE are calculated for both the training and test datasets.

This makes it possible to observe whether providing the model with more examples improves its ability to predict prices for previously unseen properties.

## Which Feature Is the Most Important?

The analysis of the saved Random Forest model showed that **property surface area is by far the most important feature used by the model**.

The `feature_importances_` value for `surface` was approximately **78%**, while the remaining features had considerably smaller values.

This should not be interpreted as saying that "78% of the property price depends on its surface area". Instead, this value describes how important the feature was when the decision trees were making splits during the training process.

The strong importance of surface area is intuitive. Surface area is directly related to the size of a property, and larger properties generally tend to have higher prices.

The model also uses information about location and property type. However, in this particular dataset, these features have much less importance than surface area.

It is important to remember that feature importance depends on the features available to the model. The current model uses a relatively small set of property characteristics. If additional information were available — such as the exact location, number of rooms, floor, property condition, or other characteristics — some of the information currently associated with surface area might instead be explained by those features.

## Error Analysis

A single RMSE or R² value does not always provide enough information to understand how a model behaves. Therefore, the project also includes an analysis of **residuals**.

A residual is the difference between the actual and predicted price:

```text
residual = actual price - predicted price
```

For example, if the actual price is 520,000 and the model predicts 500,000, the residual is 20,000.

The project creates several diagnostic plots:

- actual prices versus predicted prices,
- residuals versus predicted prices,
- a histogram of residuals.

The actual-versus-predicted plot also contains a reference line representing perfect predictions. The closer the points are to this line, the smaller the prediction errors.

The residual plot can help determine whether the model makes errors randomly or whether there are visible patterns in its mistakes. Repeated patterns may suggest that the model is missing some important relationships in the data.

## Final Model

After the experiments and evaluation are completed, the selected Random Forest model is trained again using **all available data**.

The final model is saved as:

```text
my_random_forest_final.joblib
```

The saved file contains the complete pipeline, including the `StandardScaler` and the Random Forest model.

This means that the model can later be loaded and used for predictions without having to repeat the entire training process.

## Limitations

The model cannot take into account every factor that influences the price of a property. It can only use the information available in the dataset.

The current model does not include many potentially important characteristics, such as the exact location, number of rooms, floor, quality of the property, or other details, unless they are represented in the available variables.

Therefore, even a well-performing model cannot perfectly predict the price of every property.

Its purpose is not to "guess" the exact price, but to identify patterns in historical property listings and use those patterns to make a reasonable prediction for a new property.

## Summary

The developed system uses machine learning to predict property prices. The data is first cleaned and transformed into a format that can be processed by machine learning algorithms. Several different regression models are then trained and compared.

The **Random Forest model with `min_samples_split=4`** was selected for further analysis. It consists of 100 decision trees whose predictions are combined to produce the final price estimate.

The model was evaluated using RMSE, MAE, and R², while additional diagnostics were used to check for overfitting, analyze prediction errors, and investigate how the amount of training data affects performance.

One of the most important findings is that **property surface area is by far the most influential feature in the current model**. At the same time, this result also highlights a limitation of the current approach: including more detailed information about each property could allow the model to better capture the differences between individual listings.

Overall, the project demonstrates how machine learning can be used to transform relatively simple information about properties into a useful estimate of their market price.