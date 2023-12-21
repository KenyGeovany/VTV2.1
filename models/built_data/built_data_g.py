import pandas as pd
import numpy as np
import sys
import warnings

"Example"
"python3 built_bash_g.py pdhg_rgb_den_gradient 20 5 7 0.01 0.01 0.001 10000"

model = sys.argv[1]

gamma_0 = float(sys.argv[2])
gamma_h = float(sys.argv[3])
no_intervals = int(sys.argv[4])

tau = sys.argv[5]
sigma = sys.argv[6]
epsilon = sys.argv[7]
iterMax = sys.argv[8]

# Built data
df_out = pd.DataFrame()
df_out['Image'] = None

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
for i in range(no_intervals):
    gamma_i = str(round(gamma_0 + gamma_h*i,4))
    df_out['PSNR final (gamma = ' + gamma_i + ')'] = []
    df_out['SSIM final (gamma = ' + gamma_i + ')'] = []
    df_out['No. Iter. (gamma = ' + gamma_i + ')'] = []
    df_out['mse final (gamma = ' + gamma_i + ')'] = []
    df_out['log_grad (gamma = ' + gamma_i + ')'] = []
    df_out['theta (gamma = ' + gamma_i + ')'] = []
    df_out['PSNR max (gamma = ' + gamma_i + ')'] = []
    df_out['SSIM (k) (gamma = ' + gamma_i + ')'] = []
    df_out['No. Iter. (k) (gamma = ' + gamma_i + ')'] = []
    df_out['mse final (k) (gamma = ' + gamma_i + ')'] = []
    df_out['log_grad (k) (gamma = ' + gamma_i + ')'] = []
    df_out['theta (k) (gamma = ' + gamma_i + ')'] = []
warnings.filterwarnings("default", category=pd.errors.PerformanceWarning)

for i in range(1,25):
    df_out.at[i,'Image'] = 'kodim'+str(i)
    for j in range(no_intervals):
        df = pd.read_csv('../output/' + model + '/R_' + model + '/k' + str(i) + '_n25_Info' + '_g' + str(round(gamma_0 + gamma_h*j,4)) + '_t' + str(tau) + '_s' + str(sigma) + '_e' + epsilon + '_I' + str(iterMax) + '.csv')
        gamma_j = str(round(gamma_0 + gamma_h * j, 4))
        df_out.at[i, 'PSNR final (gamma = ' + gamma_j + ')'] = df.at[0, 'psnr_final']
        df_out.at[i, 'SSIM final (gamma = ' + gamma_j + ')'] = df.at[0, 'ssim_final']
        df_out.at[i, 'No. Iter. (gamma = ' + gamma_j + ')'] = df.at[0, 'nIter']
        df_out.at[i, 'mse final (gamma = ' + gamma_j + ')'] = df.at[0, 'mse_final']
        df_out.at[i, 'log_grad (gamma = ' + gamma_j + ')'] = df.at[0, 'log_grad_final']
        df_out.at[i, 'theta (gamma = ' + gamma_j + ')'] = df.at[0, 'theta_final']
        df_out.at[i, 'PSNR max (gamma = ' + gamma_j + ')'] = df.at[0, 'max_psnr']
        df_out.at[i, 'SSIM (k) (gamma = ' + gamma_j + ')'] = df.at[0, 'ssim_argmax_psnr']
        df_out.at[i, 'No. Iter. (k) (gamma = ' + gamma_j + ')'] = df.at[0, 'argmax_psnr']
        df_out.at[i, 'mse final (k) (gamma = ' + gamma_j + ')'] = df.at[0, 'mse_graph_argmax_psnr']
        df_out.at[i, 'log_grad (k) (gamma = ' + gamma_j + ')'] = df.at[0, 'log_grad_graph_argmax_psnr']
        df_out.at[i, 'theta (k) (gamma = ' + gamma_j + ')'] = df.at[0, 'theta_graph_argmax_psnr']

df_out.to_csv('output/'+model + '.csv', header=True, index=False, sep=';', decimal=',')


# Built resumme 1
df_summary = pd.DataFrame()
df_summary['Image'] = None
df_summary['BEST g PSNR'] = []
df_summary['BEST PSNR'] = []
df_summary['SSIM (P)'] = []
df_summary['Iteraciones (P)'] = []
df_summary['log_grad (P)'] = []
df_summary['theta (P)'] = []
df_summary['BEST g SSIM'] = []
df_summary['BEST SSIM'] = []
df_summary['PSNR (S)'] = []
df_summary['Iteraciones (S)'] = []
df_summary['log_grad (S)'] = []
df_summary['theta (S)'] = []

df_summary['BEST g PSNR'] = (df_out.iloc[:,1::12].idxmax(axis=1)).str.extract(r'(\d+\.\d+)\)', expand=False).astype(float)
df_summary.at[25, 'BEST g PSNR'] = np.mean(df_summary['BEST g PSNR'])
df_summary['BEST g SSIM'] = (df_out.iloc[:,2::12].idxmax(axis=1)).str.extract(r'(\d+\.\d+)\)', expand=False).astype(float)
df_summary.at[25, 'BEST g SSIM'] = np.mean(df_summary['BEST g SSIM'])
df_summary['BEST PSNR'] = df_out.iloc[:,1::12].max(axis=1)
df_summary.at[25, 'BEST PSNR'] = np.mean(df_summary.loc[:,'BEST PSNR'])
df_summary['BEST SSIM'] = df_out.iloc[:,2::12].max(axis=1)
df_summary.at[25, 'BEST SSIM'] = np.mean(df_summary.loc[:,'BEST SSIM'])

columnas = df_summary.columns.tolist()
for i in range(1,25):
    df_summary.at[i, 'Image'] = 'kodim'+str(i)
    columna_nueva = df_out.columns.get_indexer([df_out.iloc[:,1::12].idxmax(axis=1)[i]])[0]
    df_summary.at[i, 'SSIM (P)'] = df_out.iloc[i - 1, columna_nueva +1]
    df_summary.at[i, 'Iteraciones (P)'] = df_out.iloc[i-1,columna_nueva+2]
    df_summary.at[i, 'log_grad (P)'] = df_out.iloc[i - 1, columna_nueva+4]
    df_summary.at[i, 'theta (P)'] = df_out.iloc[i - 1, columna_nueva+5]
    columna_nueva = df_out.columns.get_indexer([df_out.iloc[:, 2::12].idxmax(axis=1)[i]])[0]
    df_summary.at[i, 'PSNR (S)'] = df_out.iloc[i - 1, columna_nueva - 1]
    df_summary.at[i, 'Iteraciones (S)'] = df_out.iloc[i - 1, columna_nueva + 1]
    df_summary.at[i, 'log_grad (S)'] = df_out.iloc[i - 1, columna_nueva + 3]
    df_summary.at[i, 'theta (S)'] = df_out.iloc[i - 1, columna_nueva + 4]

df_summary.at[25, 'SSIM (P)'] = np.mean(df_summary.loc[1:25, 'SSIM (P)'])
df_summary.at[25, 'Iteraciones (P)'] = np.mean(df_summary.loc[1:25,'Iteraciones (P)'])
df_summary.at[25, 'log_grad (P)'] = np.mean(df_summary.loc[1:25, 'log_grad (P)'])
df_summary.at[25, 'theta (P)'] = np.mean(df_summary.loc[1:25, 'theta (P)'])

df_summary.at[25, 'PSNR (S)'] = np.mean(df_summary.loc[1:25, 'PSNR (S)'])
df_summary.at[25, 'Iteraciones (S)'] = np.mean(df_summary.loc[1:25,'Iteraciones (S)'])
df_summary.at[25, 'log_grad (S)'] = np.mean(df_summary.loc[1:25, 'log_grad (S)'])
df_summary.at[25, 'theta (S)'] = np.mean(df_summary.loc[1:25, 'theta (S)'])

df_summary.to_csv('output/'+model + '_summary.csv', header=True, index=False, sep=';', decimal=',')

# Built resume 2
# Crear DataFrame df_summary2 con el índice adecuado
df_summary2 = pd.DataFrame()
df_summary2['Gamma'] = np.array(range(no_intervals))*gamma_h + gamma_0
df_summary2['mean PSNR'] = df_out.iloc[:,1::12].mean().set_axis(range(no_intervals))
df_summary2['mean SSIM'] = df_out.iloc[:,2::12].mean().set_axis(range(no_intervals))
df_summary2['mean Iteraciones'] = df_out.iloc[:,3::12].mean().set_axis(range(no_intervals))
df_summary2['mean log_grad'] = df_out.iloc[:,5::12].mean().set_axis(range(no_intervals))
df_summary2['mean theta'] = df_out.iloc[:,6::12].mean().set_axis(range(no_intervals))

idx_max_mean_psnr = df_summary2.loc[:,'mean PSNR'].idxmax(axis=0)
df_summary2.at[no_intervals+1, 'Gamma'] = df_summary2.at[idx_max_mean_psnr, 'Gamma']
df_summary2.at[no_intervals+1, 'mean PSNR'] = df_summary2.at[idx_max_mean_psnr, 'mean PSNR']
df_summary2.at[no_intervals+1, 'mean SSIM'] = df_summary2.at[idx_max_mean_psnr, 'mean SSIM']
df_summary2.at[no_intervals+1, 'mean Iteraciones'] = df_summary2.at[idx_max_mean_psnr, 'mean Iteraciones']
df_summary2.at[no_intervals+1, 'mean log_grad'] = df_summary2.at[idx_max_mean_psnr, 'mean log_grad']
df_summary2.at[no_intervals+1, 'mean theta'] = df_summary2.at[idx_max_mean_psnr, 'mean theta']

idx_max_mean_ssim = df_summary2.loc[:,'mean SSIM'].idxmax(axis=0)
df_summary2.at[no_intervals+2, 'Gamma'] = df_summary2.at[idx_max_mean_ssim, 'Gamma']
df_summary2.at[no_intervals+2, 'mean PSNR'] = df_summary2.at[idx_max_mean_ssim, 'mean PSNR']
df_summary2.at[no_intervals+2, 'mean SSIM'] = df_summary2.at[idx_max_mean_ssim, 'mean SSIM']
df_summary2.at[no_intervals+2, 'mean Iteraciones'] = df_summary2.at[idx_max_mean_ssim, 'mean Iteraciones']
df_summary2.at[no_intervals+2, 'mean log_grad'] = df_summary2.at[idx_max_mean_ssim, 'mean log_grad']
df_summary2.at[no_intervals+2, 'mean theta'] = df_summary2.at[idx_max_mean_ssim, 'mean theta']

df_summary2.to_csv('output/'+model + '_summary2.csv', header=True, index=False, sep=';', decimal=',')


# Print the min and max values
best_gamma_min = (df_summary.loc[1:24, 'BEST g PSNR']).min()
best_gamma_max = (df_summary.loc[1:24, 'BEST g PSNR']).max()

if (gamma_0 < best_gamma_min)and(best_gamma_max < round(gamma_0+gamma_h*(no_intervals-1),4)):
    print("Es un buen intervalo: ", gamma_0, " < ", best_gamma_min, " - ",
          best_gamma_max, " < ", round(gamma_0+gamma_h*(no_intervals-1),4))
else:
    print("No es un buen intervalo")