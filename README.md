# meal-prep-help
## Disclaimers
* This is not nutritional advice.
* This is not financial advice.
* This is not a suggested meal plan.
* This is a hobby project, it is not robust agains unexpected inputs and do not contain any error handling.

## What is this code?
This is an optimization code: given a list of foods with their nutritional value and price, it constructs the cheapest shopping list that achives a certain target for nutrients: calories, proteins, carbohydrates, fats, fiber and servings of fruits/vegetables a day.

## How it works
### Target
The file 'target.csv' contains a daily goal for each macronutrient. This values are given per unit of weight (except for fiber and servings of vegetable), so take that into account when putting your values. Kilograms, pounds, stones, or any other weight unit of measure will work as long as you are consistent with it through the process.

The provided example are targets per kilogram of weight and the values were taken from the [Barbell Medicine article on general health](https://www.barbellmedicine.com/blog/584-2/) (for a male wanting to lose body fat). Feel free to use the values in the article, to do your own research or to input random values; remember: **this repo is not nutrition advice**.

This code treats calories, carbs and fats targets as an upper limit while proteins, fruits, and fiber as a lower limit (eg. the code should not result in more calories or less fiber than spcified. If you want to reverse this for weight gain purposes, you can contact me and it should be easy.

### Foods
The file 'foods.xlsx' contains a list of foods that you want to maybe be included in your meal prep. Each line is a food with nutrients quantities by serving (what is a serving? whatever you like, the final result will give the shopping list in servings and it will work as long you are consistent). The upper_bound and lower_bound columns let you limit the quantity of servings of a food you want to eat per day, its a way to force variaty in the plan at the cost of a suboptimal price point. For example, if you want to eat less than 10 cucumbers a day you can set the upper bounds of the number of cucumbers to less than 10. If you want to eat at least an apple a day (something about doctors, but this is not health advice) input 1 in the lower bound for apples.

You can change the food spreadsheet anytime to add, remove or change available foods. One idea is to adjust the price based on your market price and enjoy some well timed discounts.

### Running the optimization
You have to choose 3 parameters:
* Weight: how much do you weigh in the same unit as you chose for your target.
* Scaler: between 0 and 1 for how much of the calories do you want planned. You may use this to leave room in the plan for cooking oils, sauces, unplanned ingredients.
* Days: how many days this plan will account for.
* Date: a string (between quotes) that will be the name of the plan: you may use it do declare the date at the start of the eating phase, and repeat this pattern every block to create a eating log. You can also create different templates and name them like you want "chicken destroyer" "the veggie king", etc.

In the terminal run
```
python meal_prep.py weight scaler days "date"
```
The shopping list should be printed on the screen in this format:
```
Weight: 81.0
6.0 Days
           calories   protein    carb        fat   fiber   fruit/veg
target  2057.400000    225.18  179.82  48.600000    35.0        10.0
actual  1921.868088    225.18  179.82  29.845512    35.0        10.0
                daily_qt   total_qt
Food                               
Chicken Breast  6.790420  40.742518
Yam             2.524818  15.148907
Corn            2.000000  12.000000
Cabbage         2.000000  12.000000
Cucumber        2.000000  12.000000
Carrot          2.000000  12.000000
Banana          1.172510   7.035061
Apple           0.827490   4.964939
Daily spending: 19.638962572617125
Total spending: 117.83377543570275
```
A .txt file will be created with the name 'date.txt' in the log folder. If you create a new plan with the same name, it will overwrite it.

### TODO
(Don't hold your breath).
* Make an analyser tool that reads the logs and plot key metrics.
* Add upper/lower bounds for target macronutrients.
