import numpy as np
from scipy.optimize import linprog
import pandas as pd
import sys
import os


def get_foods(file):
    food = pd.read_excel(file, index_col=0, header=0)
    food['Fruit/Veg'] = food['Fruit/Veg'].astype(float)
    return food


def get_target(file, weight, scaler=1):
    target = pd.read_csv(file)
    multiplier = pd.Series(4*[weight*scaler] + [1, 1], index=target.columns)
    return multiplier*target


def get_matrix(food, target):
    # negative -> lower bound
    # positive -> upper bound
    b_direction = np.array([1, # Calories
                           -1, # Protein
                            1, # Carbs
                            1, # Fats
                           -1, # Fiber
                           -1]) # Fruit/vegs
    b = target*b_direction
    c = food['Price'].values
    A = food.drop(['Price', 'Lower Bound', 'Upper Bound'], axis=1).values
    A[:, np.where(b_direction == -1)] = A[:, np.where(b_direction == -1)]*-1
    bounds = list(zip(food['Lower Bound'], food['Upper Bound']))
    return b, c, A.T, bounds


if __name__ == '__main__':
    weight = float(sys.argv[1])
    scaler = float(sys.argv[2])
    n_days = float(sys.argv[3])
    date = sys.argv[4]

    dirname = os.path.dirname(__file__)
    food_file = os.path.join(dirname, './foods.xlsx')
    target_file = os.path.join(dirname, './target.csv')

    food = get_foods(food_file)
    target = get_target(target_file, weight, scaler)

    b, c, A, bounds = get_matrix(food, target)
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds)
    actual = abs(A@res.x)
    macros = pd.concat([target.T, pd.Series(actual, index=target.columns)], axis=1)
    macros.columns = ['target', 'actual']
    shopping_list = pd.DataFrame({'daily_qt': res.x, 'total_qt': n_days*res.x}, index=food.index)

    output = '\n'.join(['Weight: {weight}'.format(weight=weight),
                        '{days} Days'.format(days=n_days),
                        macros.T.to_string(),
                        (shopping_list.sort_values(by='total_qt', ascending=False).loc[shopping_list.total_qt >= 0.01]).to_string(),
                        'Daily spending: {daily}'.format(daily=res.fun),
                        'Total spending: {total}'.format(total=res.fun*n_days)])

    print(output)
    output_file = os.path.join(dirname, './logs/{file_name}'.format(file_name=date))
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as log:
        print(output, file=log)
