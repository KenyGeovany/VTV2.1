import numpy as np
from scipy import signal  # Convolution

# Partial derivatives and second derivatives
def dx_f(m):
    c = m.shape[1]
    kernel = np.array([[0, 0, 0], [1, -1, 0], [0, 0, 0]])
    w = signal.convolve2d(m, kernel, 'same')
    w[:, c - 1] = w[:, c - 1] * 0
    return w


def dx_f2(m):
    rows, cols = m.shape
    w = m[:, 1:] - m[:, :-1]
    w = np.concatenate((w, np.zeros((rows, 1))), axis=1)
    return w


def dx_b(m):
    kernel = np.array([[0, 0, 0], [0, -1, 1], [0, 0, 0]])
    w = signal.convolve2d(m, kernel, 'same')
    w[:, 0] = w[:, 0] * 0
    return w


def dx_b2(m):
    rows, cols = m.shape
    w = - m[:, 1:] + m[:, :-1]
    w = np.concatenate((np.zeros((rows, 1)), w), axis=1)
    return w


def dy_f(m):
    r = m.shape[0]
    kernel = np.array([[0, 1, 0], [0, -1, 0], [0, 0, 0]])
    w = signal.convolve2d(m, kernel, 'same')
    w[r - 1, :] = w[r - 1, :] * 0
    return w


def dy_f2(m):
    rows, cols = m.shape
    w = m[1:, :] - m[:-1, :]
    w = np.concatenate((w, np.zeros((1, cols))), axis=0)
    return w


def dy_b(m):
    kernel = np.array([[0, 0, 0], [0, -1, 0], [0, 1, 0]])
    w = signal.convolve2d(m, kernel, 'same')
    w[0, :] = w[0, :] * 0
    return w


def dy_b2(m):
    rows, cols = m.shape
    w = - m[1:, :] + m[:-1, :]
    w = np.concatenate((np.zeros((1, cols)), w), axis=0)
    return w


def dx_c(m):
    return 0.5 * (dx_f(m) + dx_b(m))


def dy_c(m):
    return 0.5 * (dy_f(m) + dy_b(m))


def dx_c2(m):
    return 0.5 * (dx_f2(m) + dx_b2(m))


def dy_c2(m):
    return 0.5 * (dy_f2(m) + dy_b2(m))


def dxx(m):
    return dx_f2(m) - dx_b2(m)


def dyy(m):
    return dy_f2(m) - dy_b2(m)


# Basic operators: gradient, divergence, laplacian
def gradient(m):
    """
    Gradient of a function in format [u1,u2,...] where ui are nd_arrays of
    size (rows x cols)
    :param m: a vector of nd_arrays of size (n x rows x cols)
    :return: a vector of nd_arrays of size (2n x rows x cols) of the form
            [dx_u1, dy_u1, dx_u2, dy_u2, ...]
    """
    # Get the number of components of m
    num_comp = len(m.shape)
    if num_comp == 2:
        n = 1
    else:
        n = m.shape[0]

    grad = []
    if n > 1:
        for i in range(n):
            grad.append(dx_f(m[i]))
            grad.append(dy_f(m[i]))
    elif n == 1:
        grad = [dx_f(m), dy_f(m)]

    return np.array(grad)


def gradient_2(m):
    """
    Gradient of a function in format [u1,u2,...] where ui are nd_arrays of
    size (rows x cols)
    :param m: a vector of nd_arrays of size (n x rows x cols)
    :return: a vector of nd_arrays of size (2n x rows x cols) of the form
            [dx_u1, dy_u1, dx_u2, dy_u2, ...]
    """
    # Get the number of components of m
    num_comp = len(m.shape)
    if num_comp == 2:
        n = 1
    else:
        n = m.shape[0]

    grad = []
    if n > 1:
        for i in range(n):
            grad.append(dx_f2(m[i]))
            grad.append(dy_f2(m[i]))
    elif n == 1:
        grad = [dx_f2(m), dy_f2(m)]

    return np.array(grad)


def divergence(m):
    """
    Divergence of a function in format [u1,u2,...] where ui are nd_arrays of
    size (rows x cols). The function must have 2n components
    :param m: a vector of nd_arrays of size (2n x rows x cols)
    :return: a vector of nd_arrays of size (n x rows x cols) of the form
            [dx_u1 + dy_u1, dx_u2 + dy_u2, ...]
    """
    # Get the number of components of m
    num_comp = len(m.shape)
    if num_comp == 2:
        n = 1
    else:
        n = int((m.shape[0])/2)

    div = []
    if n > 1:
        for i in range(n):
            div.append(dx_b(m[2 * i]) + dy_b(m[2 * i + 1]))
    elif n == 1:
        div = dx_b(m[0]) + dy_b(m[1])
    return np.array(div)


def divergence_2(m):
    """
    Divergence of a function in format [u1,u2,...] where ui are nd_arrays of
    size (rows x cols). The function must have 2n components
    :param m: a vector of nd_arrays of size (2n x rows x cols)
    :return: a vector of nd_arrays of size (n x rows x cols) of the form
            [dx_u1 + dy_u1, dx_u2 + dy_u2, ...]
    """
    # Get the (number of components) / 2 of m
    num_comp = len(m.shape)
    if num_comp == 2:
        n = 1
    else:
        n = int((m.shape[0])/2)

    div = []
    if n > 1:
        for i in range(n):
            div.append(dx_b2(m[2 * i]) + dy_b2(m[2 * i + 1]))
    elif n == 1:
        div = dx_b2(m[0]) + dy_b2(m[1])
    return np.array(div)


def laplacian(m):
    """
    Laplacian of a function in format [u1,u2,...] where ui are nd_arrays of
    size (rows x cols)
    :param m: a vector of nd_arrays of size (n x rows x cols)
    :return: a vector of nd_arrays of size (n x rows x cols) of the form
            [d^2x_u1 + d^2y_u1, d^2x_u2 + d^2y_u2, ...]
    """
    return divergence(gradient(m))


def laplacian_2(m):
    """
    Laplacian of a function in format [u1,u2,...] where ui are nd_arrays of
    size (rows x cols)
    :param m: a vector of nd_arrays of size (n x rows x cols)
    :return: a vector of nd_arrays of size (n x rows x cols) of the form
            [d^2x_u1 + d^2y_u1, d^2x_u2 + d^2y_u2, ...]
    """
    return divergence_2(gradient_2(m))


def laplacian_3(m):
    """
    Laplacian of a function in format [u1,u2,...] where ui are nd_arrays of
    size (rows x cols)
    :param m: a vector of nd_arrays of size (n x rows x cols)
    :return: a vector of nd_arrays of size (n x rows x cols) of the form
            [d^2x_u1 + d^2y_u1, d^2x_u2 + d^2y_u2, ...]
    """
    # Get the number of components of m
    num_comp = len(m.shape)
    if num_comp == 2:
        n = 1
    else:
        n = m.shape[0]

    # Create a kernel for laplacian
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    if n == 1:
        w = -signal.convolve2d(m, kernel, mode='same', boundary='symm')
        w[0, :] = w[0, :] * 0
    else:
        w = []
        for i in range(n):
            w_i = -signal.convolve2d(m[i], kernel, mode='same', boundary='symm')
            w.append(w_i)

    return w


def gradient_c2(m):
    """
    Gradient of a function in format [u1,u2,...] where ui are nd_arrays of
    size (rows x cols)
    :param m: a vector of nd_arrays of size (n x rows x cols)
    :return: a vector of nd_arrays of size (2n x rows x cols) of the form
            [dx_u1, dy_u1, dx_u2, dy_u2, ...]
    """
    # Get the number of components of m
    num_comp = len(m.shape)
    if num_comp == 2:
        n = 1
    else:
        n = m.shape[0]

    grad = []
    if n > 1:
        for i in range(n):
            grad.append(dx_c2(m[i]))
            grad.append(dy_c2(m[i]))
    elif n == 1:
        grad = [dx_c2(m), dy_c2(m)]

    return np.array(grad)


def divergence_c2(m):
    """
    Divergence of a function in format [u1,u2,...] where ui are nd_arrays of
    size (rows x cols). The function must have 2n components
    :param m: a vector of nd_arrays of size (2n x rows x cols)
    :return: a vector of nd_arrays of size (n x rows x cols) of the form
            [dx_u1 + dy_u1, dx_u2 + dy_u2, ...]
    """
    # Get the (number of components) / 2 of m
    num_comp = len(m.shape)
    if num_comp == 2:
        n = 1
    else:
        n = int((m.shape[0])/2)

    div = []
    if n > 1:
        for i in range(n):
            div.append(dx_c2(m[2 * i]) + dy_c2(m[2 * i + 1]))
    elif n == 1:
        div = dx_c2(m[0]) + dy_c2(m[1])
    return np.array(div)


# Transformations between RGB and OPP spaces.
def rgb2opp(u, theta):
    L = (1 / (theta * np.sqrt(3))) * (u[0] + u[1] + u[2])
    C1 = (1 / np.sqrt(2)) * (u[0] - u[1])
    C2 = (1 / np.sqrt(6)) * (u[0] + u[1] - 2*u[2])
    return np.array([L, C1, C2])


def opp2rgb(u, theta):
    R = (theta / np.sqrt(3)) * u[0] + (1 / np.sqrt(2)) * u[1] + (1 / np.sqrt(6)) * u[2]
    G = (theta / np.sqrt(3)) * u[0] - (1 / np.sqrt(2)) * u[1] + (1 / np.sqrt(6)) * u[2]
    B = (theta / np.sqrt(3)) * u[0] - (2 / np.sqrt(6)) * u[2]
    return np.array([R, G, B])




