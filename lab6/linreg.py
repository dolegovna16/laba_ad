import numpy as np
import matplotlib.pyplot as plt

# значення прямої
k_true = 2.5  # true slope
b_true = 1.0  # true зсув

n_points = 100

# seeding and ahh for generated numbers to be the same
np.random.seed(42)
# рівномірно розподіляємо по всьому інтервалу для навчання
x = np.random.uniform(-10, 10, n_points)
# тіпа ріальні дані (нормальна форма(навколо нуля,стандартне відхил))
noise = np.random.normal(0, 5, n_points)                                                                                                           # міра розкиду даних навколо середнього
y = k_true * x + b_true + noise

print("first five (x, y):")
for i in range(5):
    print(f"x={x[i]:.2f}, y={y[i]:.2f}")


# метод найменших квадратів
def least_squares(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    # чисельник нахилу (deviation)
    numerator = np.sum((x - x_mean) * (y - y_mean))
    # знаменник нахилу
    denominator = np.sum((x - x_mean) ** 2)
    # нахил
    k = numerator / denominator
    # зсув
    b = y_mean - k * x_mean

    return k, b


k_est, b_est = least_squares(x, y)
print(f"Least Squares: k = {k_est:.2f}, b = {b_est:.2f}")

# degree 1 - straight, 2 - quadratic etc. оцінка поліному методом найменших квадратів
coefficients = np.polyfit(x, y, 1)
k_polyfit, b_polyfit = coefficients
print(f"np.polyfit: k = {k_polyfit:.2f}, b = {b_polyfit:.2f}")

#  ітераційний метод оптимізації, який використовується для знаходження loss function
def gradient_descent(x, y, learning_rate, n_iter):
    n = len(x)
    k = 0  # початкове припущення
    b = 0  # теж
    errors = []  # mean SqUaRe ERROR

    for _ in range(n_iter):
        y_pred = k * x + b  # sigma guess

        # градієнти
        dk = -(2 / n) * np.sum(x * (y - y_pred))
        db = -(2 / n) * np.sum(y - y_pred)

        # наскільки великі кроки при оновленні
        k -= learning_rate * dk
        b -= learning_rate * db

        # 我爱
        mse = np.mean((y - y_pred) ** 2)

        # 约翰·波克
        if _ % 100 == 0:
            print(f"Iteration {_}: k = {k:.4f}, b = {b:.4f}, MSE = {mse:.4f}")

        # invalid
        if np.isnan(mse) or np.isinf(mse):
            print("MSE is NaN or Inf! stopping...")
            break

        errors.append(mse)

    return k, b, errors


learning_rate = 0.01
n_iter = 1000
k_gd, b_gd, errors = gradient_descent(x, y, learning_rate, n_iter)
print(f"Gradient Descent: k = {k_gd:.2f}, b = {b_gd:.2f}")


# основна фіг
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Data', alpha=0.6)
# розподіляємо ікс для візуала
x_range = np.linspace(-10, 10, 100)
y_true = k_true * x_range + b_true
plt.plot(x_range, y_true, color='green', label=f'True Line (y = {k_true:.2f}x + {b_true:.2f})', linestyle='--')

# найменших квадратів
y_est = k_est * x_range + b_est
plt.plot(x_range, y_est, color='red', label=f'Least Squares (y = {k_est:.2f}x + {b_est:.2f})')

# np.polyfit
y_polyfit = k_polyfit * x_range + b_polyfit
plt.plot(x_range, y_polyfit, color='purple', label=f'np.polyfit (y = {k_polyfit:.2f}x + {b_polyfit:.2f})',
         linestyle=':')

# градієнтний спуск
y_gd = k_gd * x_range + b_gd
plt.plot(x_range, y_gd, color='orange', label=f'Gradient Descent (y = {k_gd:.2f}x + {b_gd:.2f})', linestyle='-.')

# налаштовуємо
plt.title('Linear Regression')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()

# error (MSE) vs iterations
plt.figure(figsize=(10, 6))
plt.plot(range(0, n_iter), errors, color='teal')
plt.title('Error (MSE) vs Iterations')
plt.xlabel('Iterations')
plt.ylabel('MSE')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(range(len(errors)), errors, color='teal')
plt.xlim(left=0, right=49)
plt.ylim(bottom=0, top=(errors[0]) * 1.1)
plt.title('Error (MSE) vs Iterations (First 50 Iterations)')
plt.xlabel('Iterations')
plt.ylabel('MSE')
plt.grid(True)
plt.show()

normalized_errors = (errors - min(errors)) / (max(errors) - min(errors))

plt.figure(figsize=(10, 6))
plt.plot(range(0, len(normalized_errors)), normalized_errors, color='teal')
plt.title('Normalized Error (MSE) vs Iterations')
plt.xlabel('Iterations')
plt.ylabel('Normalized MSE')
plt.grid(True)
plt.show()

