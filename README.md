# Read Me

*

  This is the repository for the code accompanying the agent-based model and analysis published in the paper entitled "Social learning and predisposition shape tool behavior in hybrid macaques". Please follow this link to download a copy of this paper. If you cannot gain access to the paper via the link, feel free to write me directly and I will do my best to respond to you. 
  
# Agent Based Model


All components of the ABM can be found in the model folder. All of the files contained within this folder should be kept together in order to ensure the full functionality of the model. The ABM makes use of the Mesa agent-based modeling framework for Python. Follow this [link](https://mesa.readthedocs.io/en/latest/) to learn more about about programming models using Mesa. 

## Requirements and Dependencies

  The model was developed and implemented in Python 3.9 but it should work on earlier versions of python. I have also tried running the model in Python 3.8 and 3.7 and it worked fine. I have not tried running the ABM using Anaconda but I do not see any reason that this would be an issue. 
  
  The majority of the libraries required to run the ABM are installed when Python is initially installed. The agent-based modeling library Mesa must also be installed. This can be done using pip. 

## Running the model

  There are a few different ways to run the model. The easiest way is to use the visualization.py file. Running this file initialize a visual version of the in your web browser. It provides you with the option to start and stop the model. Associated with the model run will be exported as a .csv file at the end of the run. Data will only be exported from models that reach fixation. In other words, no data is exported if you prematurely end the run.
  
  If you wish to conduct a parameter sweep or reproduce the dataset used in the publication, use the behavior_space.py file. There is no visualization associated with runs. Make sure that the number of cores is set to match the hardware of your computer. All data associated with each run will be exported to the "output" folder contained within the "Model" folder.
  
# Analysis Files

All of the code used to carry out the analysis is found in the "Analysis" folder. Here you will find 2 Rmarkdown files. The file called "Macaque_Diagnostics" reports on the Markov chain used to sample the posterior distributions.

The code makes use of the rethinking package. If you do not have the rethinking package installed, I would suggest that you visit the rethinking pape to make sure everything is installed properly.

The data needed to run these Rmarkdown files is provided in the "Data" folder. This folder contains the data for both agent-based modeling conditions. The data from Koram island is part of one of the author's ongoing research and, thus, cannot be made publically available. Nevertheless, we have provided a PDF of version of the Rmarkdown for those who wish to see the code. Those interested in reproducing this part of the paper or using this data set can make a request by writing the authors. 

# Feedback, bugs, issues

Please don't hesitate to contact me with any issues you might encounter.


