import matplotlib.pyplot as plt

ITERATIONS = 5
ALPHA =5

def f(x):
    return x**2

def f_prime(x):
    return 2*x

def GD(x_0, alpha, num_it, f, f_prime):
    x_k = x_0
    x_ks = []
    for k in range(num_it):
        x_ks.append(x_k)
        x_k = x_k - alpha*f_prime(x_k)

    return x_k, f(x_k), x_ks

x_k , y_k, x_ks = GD(1, ALPHA, ITERATIONS, f, f_prime)

print(f"x_star = {x_k}")
print(f"f(x)_min = {y_k}")

xs = [i for i in range(ITERATIONS)]

plt.plot(xs, x_ks)
plt.xlabel("Iterations")
plt.ylabel("x_k")

plt.show()