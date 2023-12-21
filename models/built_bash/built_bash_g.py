import sys

"python3 built_bash_g.py pdhg_rgb_den_gradient 10 2.5 25 0.01 0.01 0.001 10000"

model = sys.argv[1]
model_split = model.split('_')
experiment = model_split[1]+'_'+model_split[2]+'.py'

gamma_0 = float(sys.argv[2])
gamma_h = float(sys.argv[3])
no_intervals = int(sys.argv[4])

tau = float(sys.argv[5])
sigma = float(sys.argv[6])
epsilon = float(sys.argv[7])
iterMax = int(sys.argv[8])

file_out = open('output/' + model + '.sh', 'w')

for k in range(1,25):
    img_k = 'kodim' + str(k)
    for i in range(no_intervals):
        gamma_i = round(gamma_0 + gamma_h*i,4)
        experiment_name = 'python3 ' + experiment + ' ' + model + ' ' + img_k + ' ' + str(gamma_i) + ' ' + str(tau) + ' ' + str(sigma) + ' ' + str(epsilon) + ' ' + str(iterMax) + '\n'
        file_out.write(experiment_name)

file_out.close()