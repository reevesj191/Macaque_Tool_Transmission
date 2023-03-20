
# Social Network Data associated with the paper titled, "Simulation and social network analysis provide insight into the acquisition of tool behavior in hybrid macaques"
---

The dataset published here comprises a combination of simulated data and observational data associated with a group of hybrid long-tailed macaques (Macaca fascicularis) from Koram island in Thailand. These data were used to explore the transmission pathways through which individuals within this group acquire the ability to use tools. The simulated data published here were used to generate expectations for how one might detect evidence of different transmission pathways within a social network. The simulation data provided some evidence that different transmission processes such as social learning and inheritance could be distinguished from each other using social network data. These expectations were then applied to the data derived from Koram island to discuss the role of social learning and inheritance in tool-use acquisition in hybrid macaques. 

## Description of the data and file structure

The dataset comprises 6 data tables provided in CSV format. These include:

1) ABM_Social_Condition.csv

2) ABM_Inheritance_Condition.csv

3) ABM_Asocial_na1as25_Condition.csv

4) ABM_Asocial_na10as25_Condition.csv

5) ABM_Asocial_na200as25_Condition.csv

6) Koram.csv

Each CSV file contains noded data of individuals within a social network. Each row is an individual node. Each individual possesses the attributes analyzed using Bayesian methods in the paper. Each individual or row is characterized by the following variables: tool user status (U), eigenvector centrality (C), the strength of connections with tool users (S), age (A), and phenotype (H).

**tool user status (U)**: A integer value of either 1 or 0. 1 indicates that the individual is a tool user. 0 indicates that the individual is not a tool user.

**eigenvector centrality (C)**: This value is the network position of the individual as characterized by eigenvector centrality.

**strength of connections with tool users (S)**: A measure of how strongly an individual is connected with tool users.

**age**: An integer value of 1 or 0. 1 indicates that the individual is of an age where they can use tools. 0 implies the individual is not quite old enough to use stone tools.

**phenotype**: The hair pattern associated with the individual.

Datasets 1-5 are generated using the agent-based simulation (ABM) reported in the paper. The code for the model is actively maintained at this [link](https://github.com/reevesj191/Macaque_Tool_Transmission). Each CSV file comprises data from 30 model iterations of each modeled condition. Dataset 1 is associated with the social learning condition. Dataset 2 is associated with the genetic inheritance condition of the model. Datasets 3 - 5 contain data from the asocial model which explored the influence of resource attraction on proximity associations between individuals. For information regarding the design and implementation of the ABM see the complete model description provided as supplementary material.

Dataset 6: Contains social network data for individuals from Koram island, Thailand.


## Sharing/Access information

Data associated with this work is only publicly available on Dryad. 

## Code/Software

All code associated with the analysis of these datasets and associated readme files can be accessed on the author's [github page](https://github.com/reevesj191/Macaque_Tool_Transmission)


