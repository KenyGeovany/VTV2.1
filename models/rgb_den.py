from lib_dif_operators import *
from lib_generic import *
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import csv
from numpy import genfromtxt
import sys

# Load the img_original image
img_name = sys.argv[2]
img_clean = open_img('input/img_clean/' + img_name + '.png', echo=False)
img_noise = open_img('input/img_denoising_gaussian/sigma25' + img_name + '.png', echo=False)

# Extract the BGR components
blue_clean, green_clean, red_clean = cv2.split(img_clean)
u = np.array([red_clean, green_clean, blue_clean]).astype(float)

# Extract the BGR components of the noised image
blue_noise, green_noise, red_noise = cv2.split(img_noise)
u_0 = np.array([red_noise, green_noise, blue_noise]).astype(float)

p=1

# MODELOS
def pdhg_rgb_den_gradient(u, u_0, img_name):
    # Parameters
    gamma = float(sys.argv[3])
    tau = float(sys.argv[4])
    sigma = float(sys.argv[5])
    tol = float(sys.argv[6])
    iterMax = int(sys.argv[7])
    par = np.array([gamma, tau, sigma, tol, iterMax])

    # Initial states
    (_, rows, cols) = u_0.shape
    mse = 10.
    k = 0
    m_ones = np.ones((rows, cols),dtype='float_')
    eta_k = np.zeros((6,rows,cols),dtype='float_')
    u_k = u_0

    psnr_graph = np.zeros(iterMax)
    ssim_graph = np.zeros(iterMax)
    mse_graph = np.zeros(iterMax)
    gradient_graph = np.zeros(iterMax)
    theta_graph = np.zeros(iterMax)

    while (mse > tol and k < iterMax) or (k < 50):
        print("k:", k)
        print("mse: ", mse)

        u_kplus1 = (u_0 + (gamma / tau) * (u_k - tau*divergence_2(eta_k))) / (1. + gamma / tau)

        ubar_k = 2 * u_kplus1 - u_k

        num = eta_k + sigma * gradient_2(ubar_k)
        norm_num = np.sqrt(np.sum(num**2, axis=0))**p
        den = np.maximum(m_ones, norm_num)
        eta_kplus1 = np.divide(num, den)

        mse = np.sqrt(np.sum((u_kplus1-u_k)**2)/u_0.size)

        u_k = u_kplus1
        eta_k = eta_kplus1

        psnr_graph[k] = psnr(np.clip(u_k[:, 1:-1, 1:-1], 0, 255) / 255., u[:, 1:-1, 1:-1] / 255.)
        ssim_graph[k] = ssim(np.clip(u_k[:, 1:-1, 1:-1], 0, 255) / 255., u[:, 1:-1, 1:-1] / 255., channel_axis=0, data_range=2.0)
        mse_graph[k] = mse
        gradient_k = gradient_2(u_k)
        gradient_graph[k] = np.log(np.linalg.norm(gradient_k))
        num_theta_k = dx_f2(u_k[0]) * dy_f2(u_k[1]) - dy_f2(u_k[0]) * dx_f2(u_k[1])
        den_theta_k = np.sqrt((dx_f2(u_k[0]) ** 2 + dy_f2(u_k[0]) ** 2) * (dx_f2(u_k[1]) ** 2 + dy_f2(u_k[1]) ** 2))
        theta_graph[k] = np.mean(np.abs(num_theta_k / (den_theta_k + 0.00000000000000001)))

        k += 1

    matrix_graphics_name_output = 'output/' + sys.argv[1] + '/k' + img_name[5:] + '_n25_Graph_g' + str(gamma) + '_t' + str(tau) + '_s' + str(sigma) + '_e' + str(tol) + '_I' + str(iterMax) + '.csv'
    vector_info_name_output = 'output/' + sys.argv[1] + '/k' + img_name[5:] + '_n25_Info_g' + str(gamma) + '_t' + str(tau) + '_s' + str(sigma) + '_e' + str(tol) + '_I' + str(iterMax) + '.csv'
    vector_info_header = ('beta', 'tau', 'sigma', 'tol', 'iterMax', 'time', 'psnr_final', 'ssim_final', 'mse_final', 'nIter', 'log_grad_final','theta_final', 'max_psnr', 'ssim_argmax_psnr', 'argmax_psnr', 'mse_graph_argmax_psnr', 'log_grad_graph_argmax_psnr', 'theta_graph_argmax_psnr')

    return u_k, k-1, psnr_graph, ssim_graph, mse_graph, gradient_graph, theta_graph, matrix_graphics_name_output, vector_info_name_output, vector_info_header, par

# Testing function
def test_model(u, u_0, img_name, model_function):
    # Run the model
    @time_measure
    def f(): return model_function(u, u_0, img_name)
    [u_k, iter_f, psnr_graph, ssim_graph, mse_graph, gradient_graph, theta_graph, matrix_graphics_name_output, vector_info_name_output, vector_info_header, par], _time = f()

    # Information
    psnr_f = psnr_graph[iter_f]
    ssim_f = ssim_graph[iter_f]
    mse_f = mse_graph[iter_f]
    log_grad_f = gradient_graph[iter_f]
    theta_f = theta_graph[iter_f]
    max_psnr = np.amax(psnr_graph)
    iter_max_psnr = np.argmax(psnr_graph)
    ssim_max_psnr = ssim_graph[iter_max_psnr]
    mse_max_psnr = mse_graph[iter_max_psnr]
    log_grad_max_psnr = gradient_graph[iter_max_psnr]
    theta_max_psnr = theta_graph[iter_max_psnr]

    # Save graphics and info
    matrix_graphics = np.real(np.transpose(np.array([np.arange(0, iter_f+1), psnr_graph[0:iter_f+1], ssim_graph[0:iter_f+1], mse_graph[0:iter_f+1], gradient_graph[0:iter_f+1], theta_graph[0:iter_f+1]])))
    matrix_graphics_header = ('k', 'PSNR', 'SSIM', 'mse', 'Log-Gradient', 'Angle')
    vector_info = np.real(np.concatenate((par, np.array([_time, psnr_f, ssim_f, mse_f, iter_f, log_grad_f, theta_f, max_psnr, ssim_max_psnr, iter_max_psnr, mse_max_psnr, log_grad_max_psnr, theta_max_psnr]))))
    with open(matrix_graphics_name_output, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(matrix_graphics_header)
        writer.writerows(matrix_graphics)
    with open(vector_info_name_output, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(vector_info_header)
        writer.writerow(vector_info)

    # Save image
    img_output = u_k

    return matrix_graphics_name_output, vector_info_name_output, img_output


def plot_graphics(name_graphics_file):
    matrix_graphics = genfromtxt(name_graphics_file, delimiter=',').T
    # Show graphics
    show_plot_cv2([matrix_graphics[1], matrix_graphics[2], matrix_graphics[3], matrix_graphics[4], matrix_graphics[5]],
                  ['PSNR', 'SSIM', 'mse', 'Gradient', 'Angle'], 'Graphics', cols_max=3, figsize=(14.2857*(3/2), 10*(3/2)),
                  savefig=True, name_savefig=name_graphics_file[:-4]+'.png')


def show_info(name_info_file):
    # name_model = gradient, dirac
    vector_info = genfromtxt(name_info_file,delimiter=',')[1].T

    # Print information
    print("Information: ")
    print(name_info_file)
    print("- tau = ", vector_info[0])
    print("- sigma = ", vector_info[1])
    print("- Gamma = ", vector_info[2])
    print("- tol = ", vector_info[3])
    print("- iterMax = ", vector_info[4])
    print("- Time = ", vector_info[5])
    print("- PSNR final = ", vector_info[6])
    print("- MSE final = ", vector_info[7])
    print("- Effective iterations = ", vector_info[8]-1)
    print("- log-grad final = ", vector_info[9])
    print("- Theta final = ", vector_info[10])
    print("- max(psnr) = ", vector_info[11])
    print("- argmax(psnr) = ", vector_info[12])
    print("- mse(argmax(psnr)) = ", vector_info[13])
    print("- logGrad(argmax(psnr)) = ", vector_info[14])
    print("- theta(argmax(psnr)) = ", vector_info[15])


def run_model():
    if sys.argv[1] == 'pdhg_rgb_den_gradient':
        # Change this line for the model to test
        graph_file_name, info_file_name, img_output = test_model(u, u_0, img_name, pdhg_rgb_den_gradient)
        # show_info(info_file_name)
        plot_graphics(graph_file_name)
        # Save image
        save_img(np.moveaxis(u[::-1,...],0,-1), "output/" + sys.argv[1] + "/" + img_name+"_clear.png")
        save_img(np.moveaxis(u_0[::-1,...], 0, -1), "output/" + sys.argv[1] + "/" + img_name + "_degraded.png")
        save_img(np.moveaxis(img_output[::-1,...], 0, -1), "output/" + sys.argv[1] + "/" + img_name + "_restored.png")
    else: print("Error: model incorrect.")

run_model()



