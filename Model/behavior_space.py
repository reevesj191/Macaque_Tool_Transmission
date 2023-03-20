import os
from model_definition import *
from mesa.batchrunner import BatchRunnerMP
from multiprocessing import freeze_support

RUNS_PATH = "Model_2_Revisions"
N_ITER = 750
N_CORES = 65


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
                             nr_processes= N_CORES,
                             variable_parameters=variable_params,
                             fixed_parameters=fixed_params,
                             iterations=N_ITER,
                             max_steps=1000000000)

    mp_batch_run.run_all()


## Attraction null model

fixed_params = {"width": 20,
                "height":  20,
                "Na": 100,
                "runs_path": RUNS_PATH,
                "N_Starting_Tool_users": 1,
                "trans_mode": "resource_attraction"
                }


variable_params = {

    "N_Resources": (1, 10, 200, 300),
    "attraction": (1,5,25),
    "learn_rate": (2,5)

}


if __name__ == '__main__':
    freeze_support()

    mp_batch_run = BatchRunnerMP(model_cls=Mendelian_Monkeys,
                             nr_processes= N_CORES,
                             variable_parameters=variable_params,
                             fixed_parameters=fixed_params,
                             iterations=N_ITER,
                             max_steps=1000000000)

    mp_batch_run.run_all()
