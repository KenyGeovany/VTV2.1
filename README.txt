PART 0.
General information.
1. Author: Keny Geovany Chin Parra.
2. This version is only a demo.
3. Historial of versions
    - VTV2.0 Wrote in November 2023.
    - VTV2.1 Wrote in December 2023.
    - VTV2.2 In developing.
4. Requirements

PART 1.
Execute the app:
1. In a terminal go to "VTV2.1/"
2. Execute: %python3 main.py
3. There are three options:
    - Test_exp: Test an individual experiment on a specific image.
    - Upload_exp: send many experiment to a existing cluster.
    - Download_exp: downloads the result obtained in upload_exp
    and processes the data.

PART 2.
Change some parameters inside the code:
1. The visible parameters in the app are:
    - model_name (e.g. pdhg_rgb_den_gradient)
    - Image (e.g. Kodim17)
    - name_job (e.g. den_g)
    - name_log (e.g. result.log)
    - tol, Iter
    - Parameters for the optimizer (e.g. tau, sigma)
    - Parameters for the mathematic model (e.g. gamma, beta)
    Note1: the built_data_script and the built_bash_script are not true
    parameters, because they depend on the model.
    Note2: the config parameter (e.g. 123456) only says which steps will
    be executed.
2. In the file "VTV2.1/upload" and "VTV2.1/download" set valid parameters
for remote_user, remote_host, remote_port.
3. Inside the file "VTV2.1/upload" in the section "# Updating slurm" you
can modify some specific parameters like partition, ntasks-per-node, ntasks
mail-user, etc. Check for problems.

PART 3.
Structure of the directory in the cluster.
~/models/
    - lib_generic.py
    - lib_dif_operators.py
    - rgb_den.py
    - rgb_deb.py
    - opp_den.py
    - opp_deb.py
    input/
        img_clean/
            -kodim1.png
            - ...
        img_deblurring_gaussian/
            - kodim1_small.png
            - ...
            - kodim1_small_blurred.png
            - ...
        img_denoising_gaussian/
            - sigma25kodim1.png
            - ....
    output/
    built_bash/
    log/
This is the initial structure of the remote directory models. The last three
directories are empty.
Note: Is important to install virtualenv in the cluster and create a virtual
environment to work (e.g. env_usr).

PART 4.
The results of the experiments.
- Test_exp: send all the results in the local directory "VTV2.1/models/output/model_name".
    For an individual experiment the result is
    - Graph.csv: contains all the data per iteration.
    - Info.csv: contains the data of the final iteration.
    - Graph.png: Are five graphs that shows the behavior of the experiment.
    - Clean.png, degraded.png, restored.png: are three images with the visual
    result of the experiment.
- Upload_exp:
    Returns all the data in the remote directory ~/models
    - log/result.log: a log with the information per iteration of all experiments.
    - output/R_model_name/: all the data returned in test_exp, but for all
    the experiments submitted.
- Download_exp:
    The data is in the local directory VTV2.1/models/built_data
    - /model_name.csv: Is a table with all the Info.csv information of
    all experiments
    - built_data/model_name_summary.csv: Is a table with a summary of the
    information made in model_name.csv, considering the mean-max-PSNR.
    - built_data/model_name_summary2.csv: Is a table with a summary of the
    information made in model_name.csv, considering the max-mean-PSNR.