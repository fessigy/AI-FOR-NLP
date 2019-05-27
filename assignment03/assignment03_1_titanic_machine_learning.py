import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

titanic_fname = "C:\\Users\\fangsj\\Desktop\\NLPcourse-2019.3\\pytest\\git-fessigy-AI-FOR-NLP\\AI-FOR-NLP\\assignment03\\titanic\\train.csv"
content = pd.read_csv(titanic_fname)
content = content.dropna()
fares = content['Fare']
ages = content['Age']
age_with_fares = content[(content['Age']>22) & (content['Fare']<400) & (content['Fare'] > 130)]
sub_fare = age_with_fares['Fare']
sub_age = age_with_fares['Age']
'''
报错：为什么这里加了.tolist()会报这个错？
TypeError: can only concatenate list (not "int") to list
'''
#plt.scatter(sub_age,sub_fare)
#plt.show()

def func(age, k, b):return age * k + b

#损失函数
def loss(y, yhat):
    return np.mean(np.abs(y - yhat))
    # return np.mean(np.square(y - yhat))
    # return np.mean(np.sqrt(y - yhat))


min_error_rate = float('inf')
best_k,best_b = None,None
loop_times = 10000
losses = []

change_directions = [
    (+1,-1),
    (+1,+1),
    (-1,-1),
    (-1,+1)
]

best_direction = None

def step():return random.random() * 1


k_hat = random.randint(-10, 10)
b_hat = random.randint(-10, 10)

direction = random.choice(change_directions)

def derivate_k(y,yhat,x):
    abs_values = [1 if (y_i - yhat_i) > 0 else -1 for y_i,yhat_i in zip(y,yhat)]
    return np.mean([a * -x_i for a,x_i in zip(abs_values, x)])

def derivate_b(y,yhat):
    abs_values = [1 if (y_i - yhat_i) > 0 else -1 for y_i,yhat_i in zip(y,yhat)]
    return np.mean([a * -1 for a in abs_values])

learning_rate = 1e-1

while loop_times > 0:

    # k_hat = random.random() * 20 -10
    # b_hat = random.random() * 20 -10

    # k_delta_direction,b_delta_diraction = direction

    # k_delta = k_delta_direction * step()
    # b_delta = b_delta_diraction * step()

    k_delta = -1 * learning_rate * derivate_k(sub_fare, func(sub_age, k_hat,b_hat),sub_age)
    b_delta = -1 * learning_rate * derivate_b(sub_fare, func(sub_age, k_hat,b_hat))

    k_hat = k_hat + k_delta
    b_hat = b_hat + b_delta

    estimated_fares = func(sub_age, k_hat, b_hat)
    error_rate = loss(y=sub_fare, yhat=estimated_fares)

    if error_rate < min_error_rate:
        min_error_rate = error_rate
        best_k, best_b = k_hat,b_hat
        # direction = (k_delta_direction,b_delta_diraction)
        print(error_rate)
        print("loop == {}".format(10000-loop_times))
        losses.append(min_error_rate)
        print("f(age)={} * age + {}, with error rate: {}, with delta k {} b {}".format(best_k,best_b,min_error_rate,k_delta,b_delta))
    # else:
        # direction =  random.choice(change_directions)
        # 没懂：
        # direction = random.choice(list(set(change_directions)-{(k_delta_direction,b_delta_diraction)}))
    loop_times -= 1



# plt.scatter(sub_age, sub_fare)
# plt.plot(sub_age, func(sub_age,best_k,best_b), c='r')
# plt.show()

plt.plot(range(len(losses)),losses)
plt.show()