import os
from model_definition import *
from mesa.batchrunner import BatchRunnerMP
from multiprocessing import freeze_support

RUNS_PATH = "/Users/jonathanreeves/Dropbox/Jonathan_Reeves/Research/TechPrim/Macaque_Tool_Transmission/Model_2/Output/Life_span2"

if not os.path.isdir(RUNS_PATH):
    os.makedirs(RUNS_PATH)
else:
    print("Output folder Already Exists")

fixed_params = {"width": 20,
                "height":  20,
                "Na": 100,
                "runs_path": RUNS_PATH,
                "N_Starting_Tool_users": 1
                }

variable_params = {
    "trans_mode": ("social","inherited")
}


if __name__ == '__main__':
    freeze_support()

    mp_batch_run = BatchRunnerMP(model_cls=Mendelian_Monkeys,
                             nr_processes=4,
                             variable_parameters=variable_params,
                             fixed_parameters=fixed_params,
                             iterations=1000,
                             max_steps=1000000000)

    mp_batch_run.run_all()

