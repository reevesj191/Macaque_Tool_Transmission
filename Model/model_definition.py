from agents import Monkey, ToolResource
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from abm_functions import get_random_alphanumeric_string
from datetime import datetime
import pandas as pd
import random
import os

def compute_n_users(model):

    agents = [agent for agent in model.schedule.agents if isinstance(agent, Monkey)]
    agents = [agent.tool_user for agent in agents if agent.tool_user is True]
    return len(agents)

def compute_n_w_trait(model):

    agents = [agent for agent in model.schedule.agents if isinstance(agent, Monkey)]
    agents = [agent.tool_user for agent in agents if agent.tool_trait is True]
    return len(agents)

class Mendelian_Monkeys(Model):

    def __init__(self,
                 height, width, Na, N_Starting_Tool_users = 1, 
                 N_Resources = 0, attraction = 5, learn_rate = 1,
                 trans_mode = "social", runs_path = "Test"):
        self.runs_path = runs_path
        self.run_id = get_random_alphanumeric_string(6)
        #self.run_id = "debug" # For debugging puposes only
        self.datetime = datetime.now()
        self.max_ts = 50000 # For debugging only
        self.starting_users = N_Starting_Tool_users # The number of individuals that begin with the tool use trait. 
        self.model_stop = -1 # This will be populated with the reason the simulation ended. 
        self.current_id = 0 # The id to be given to the next agent. This attribute is handled by mesa.
        self.running = True # Determines if the model is running or not. This attribute is also handled by mesa 
        self.timestep = 0 # The current time-step of the simulation
        self.Na = Na # The number of agents in the model. 
        self.Nr = N_Resources # The number of attractors within the model. 
        self.asocial_rate = learn_rate
        self.attractor_strength = attraction
        self.transmission_mode = trans_mode # how the tool use trait is transmitted from one individual to the other. 

        #### Debuging
        # print(self.asocial_rate)
        # print(self.Nr)
        # print(self.attractor_strength)

        ### Space, Scheduling

        self.schedule = RandomActivation(self) # The order that the agents are iterated through during each time-step. 

        self.grid = MultiGrid(width=width, # Grid type. This particular grid allows multiple agents to occupy a space. 
                              height=height, 
                              torus= False)
        self.node_data = []
        self.social_links = pd.DataFrame({'source': [], 'target': []} ) # Creates a dataframe where information on each interaction is held. Used to generate the social networks. 
        self.ancestry_links = pd.DataFrame({'source': [], 'target': []}) # Creates a dataframe where information on each repoductive event is held. Not used in the paper. 

        ## create agents

        for i in range(Na-N_Starting_Tool_users):
            hair = random.choice([1,2])
            agent = Monkey(self.next_id(), self, tool_user= False,mom="Unknown", mom_user= "Unknown", hair=hair)
            agent.age = random.randint(0,100) # stops mass die off events
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent,(x,y))
            self.schedule.add(agent)

    
        for i in range(Na-(Na-N_Starting_Tool_users)):
            hair = 2
            agent = Monkey(self.next_id(), self, tool_user=True , mom="Unknown", mom_user="Unknown", hair=hair)
            x = int(width/2)
            y = int(height/2)
            agent.learned_tool_use = "OG"
            agent.age = 25
            agent.tool_trait = True
            self.grid.place_agent(agent,(x,y))
            self.schedule.add(agent)

        
        if self.transmission_mode == "resource_attraction":

            coord_list = []

            for i in range(width):
                x = i
                for j in range(height):
                    y=j 
                    coord_list.append((x,y))

    
            coord_list = random.sample(coord_list, self.Nr)

            for coords in coord_list:
  
                agent = ToolResource(self.next_id(), self)
                self.grid.place_agent(agent,coords)
                self.schedule.add(agent)

                self.attractors = [obj for obj in self.schedule.agents if isinstance(obj, ToolResource)]
                self.attractor_xy = [agent.pos for agent in self.attractors]
            
        # write run Summary...

        print(self.run_id)
        if not os.path.exists(self.runs_path):
            os.mkdir(self.runs_path)
        else:
            pass

    def step(self):
        
        self.n_users = compute_n_users(self)
        self.n_w_trait = compute_n_w_trait(self)
        self.schedule.step()
        self.timestep += 1
        
        # Stopping Critera
        prop_users = self.n_users/self.Na
        if prop_users >= .50:
            
            stop = True
            self.model_stop = "Tool Pop Achieved"

        elif self.transmission_mode == "social" and self.n_users == 0:
                
            stop = True
            self.model_stop = "No more users"

        elif self.transmission_mode == "inherited" and self.n_w_trait == 0:

            stop = True
            self.model_stop = "No more users"

        elif len(self.schedule.agents) == 0:
            stop = True
            self.model_stop = "All Agents Dead"
        
        else: 
            stop = False
        
        if stop is True:
            
            # Print Summary Data
            sum_path = os.path.join(self.runs_path, self.run_id + "_run_data.csv")
            run_sum = pd.DataFrame({'run_id': self.run_id,
                                    'datetime': self.datetime,
                                    'h': self.grid.height,
                                    "w": self.grid.width,
                                    "starting_users": self.starting_users,
                                    'n_time_steps': self.timestep,
                                    'n_agents': self.Na,
                                    'n_attractors': self.Nr,
                                    'a_learn_rate': self.asocial_rate,
                                    'attractor_strength': self.attractor_strength,
                                    'transmission_mech': self.transmission_mode,
                                    'stop_reason': self.model_stop
                                    }, index=[0])
            run_sum.to_csv(sum_path)
            monkeys = [agent for agent in self.schedule.agents if isinstance(agent, Monkey)]
            for agents in monkeys:
                node_dat = {"id": agents.unique_id, 
                            "run_id": self.run_id,
                            "living": agents.living,
                            "tool_user": agents.tool_user,
                            "learned_tool_use": agents.tool_user,
                            "tool_user_encounters": agents.tool_user_encounters,
                            "age_learned_tool_use": agents.age_learned_tool_use,
                            "time_step_learned": agents.ts_learned,
                            "learning_method": agents.transmission_method,
                            "age": agents.age,
                            "mother": agents.mother,
                            "mother_tool_user": agents.mother_tool_user,
                            "hair": agents.hairpattern}

                self.node_data.append(node_dat)
            
            nodes = pd.DataFrame(self.node_data)
            node_path = os.path.join(self.runs_path, self.run_id + "_nodes.csv")
            nodes.to_csv(node_path)

            link_path = os.path.join(self.runs_path, self.run_id + "_social_edges.csv")
            self.social_links.to_csv(link_path)

            link_path = os.path.join(self.runs_path, self.run_id + "_genetic_edges.csv")
            self.ancestry_links.to_csv(link_path)
            self.running = False

        else: 
            pass




