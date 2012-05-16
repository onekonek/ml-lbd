import math


def grad_u(u, v):
    return 2 * (math.exp(v) + 2 * v * math.exp(-u)) * (u * math.exp(v) - 2 * v * math.exp(-u))


def grad_v(u, v):
    return 2 * (u * math.exp(v) - 2 * math.exp(-u)) * (u * math.exp(v) - 2 * v * math.exp(-u))


def error(u, v):
    return (u * math.exp(v) - 2 * v * math.exp(-u))**2


def descent(start, eta, gradients, error):
    point = start
    c_error = error(*point)
    iteration = 0
    while (c_error > 10e-14):
        update = [grad(*point) for grad in gradients]
        point = tuple([p - eta * u for p, u in zip(point, update)])
        c_error = error(*point)
        iteration += 1
        print iteration
        print c_error
    print point


def coord_descent(start, eta, gradients, error):
    point = start
    c_error = error(*point)
    iteration = 0
    while (iteration < 16):
        for i, grad in enumerate(gradients):
          # i = len(gradients) - i - 1
           #  grad = gradients[i]
            p = point[i] - eta * grad(*point)
            l = 0 if (i - 1 < 0) else i
            point = point[:l] + (p,) + point[i + 1:]
            c_error = error(*point)
            print c_error
        iteration += 1
        c_error = error(*point)
        print iteration
        print c_error
    print point


if __name__ == '__main__':
    descent((1.0, 1.0), 0.1, [grad_u, grad_v], error)
    coord_descent((1.0, 1.0), 0.1, [grad_u, grad_v], error)
