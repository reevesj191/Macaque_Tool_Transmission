import numpy.random
from mesa import Agent
from pandas import DataFrame, concat
from math import sqrt
import random

class Monkey(Agent):
    """ The class of agent for the monkey model """
    
    # Aguements to be defined on instantiation.
    # self: inherited from the model
    # unique_id: assigned by the model
    # tool_user: True/False indicating whether the individual is a tool user or not
    # mom: unique id of agent that generated this agent.
    # mom_user: the tool_user_status of the mother.
    # hair: the hair pattern attributes.

    def __init__(self, unique_id, model, tool_user, mom, mom_user, hair):

        super().__init__(unique_id,model)
        self.tool_trait = False # True / False indicating whether the individual has the tool use trait.
        self.tool_user = tool_user # see tool_user argument
        self.learned_tool_use = False # True False statement indicating if the individual learned tool-use
        self.age = 0
        self.age_learned_tool_use = -1 # The 
        self.ts_learned = "Naive"
        self.transmission_method = "Naive"
        self.living = True
        self.tool_user_encounters = 0
        self.prox_associations = 0
        self.mother = mom
        self.mother_tool_user = mom_user
        self.hairpattern = hair

## Helper Functions

    def d2_mother(self, poss_steps, mom_loc):

        """Used by the move function determines the grid cell
         that minimizes the distance between the agent and its
         mother agent """
        
        # An empty vector to hold distances

        pos_dists = [] 

        # xy coordinates of mother location

        x1, y1 = mom_loc 

        # Determines the distance of each grid cell to the 
        # location of the mother

        for loc in poss_steps:
            x2, y2 = loc
            distance = sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
            pos_dists.append([distance])

        # return the index value for the grid-cell that is nearest
        #  the mother.

        return min(pos_dists), pos_dists.index(min(pos_dists))

## Interaction Methods

    def move(self):
        
        """
         Function moves the agent distance of one grid cell. The location
         of the agents next step is weighted by the individual's age and
         location of the individuals mother. 
        """

        # Identify all grid neighboring grids cells(i.e. grid cells that 
        # are a distance of 1 grid cell away from the agent)

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        # Identify the location of the agent's mother. 

        mom_loc = [agent.pos for agent in self.model.schedule.agents if agent.unique_id == self.mother]

        # If the agent's mother is unknown then the choice is random. This only
        # applies at the start of the model run when the initial population of
        # individuals has no mothers or when the mother agent has died and has 
        # been removed from the model itself. 

        if self.mother == "Unknown" or len(mom_loc) == 0:

            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

        else:
        
        # When the agent's mother is known then the grid cell the agent moves
        # into is determined by both age and the location of the mother.     

             # Ranks the possible steps from closest to farthest from the mother.
            d, idx = self.d2_mother(poss_steps= possible_steps, mom_loc=mom_loc[0])

            # determines the likelihood that the agent will move in a direction that 
            # minimizes the distance from the mother agent.  
            follow_prob = 1-((self.age*2)/100) 

            # The equation above (line 70) is designed to ensure that there is a decreasing 
            # likelihood that the agent will move toward their mother duing the 
            # first 50 time steps of their life. Once the age of the agent is above 50 the
            # the value returned will negative. Then the follow likelihood is set to 0.  

            if follow_prob < 0:
                follow_prob = 0
            else:
                pass
            
            # Whether the agent moves in the direction of its mother detemined
            #  by drawing from bimomial distribution where the probability of 
            # success is set equal to the follow_prob. If the binomial distribution
            # returns a 1 then the agent will move the direction of the mother's 
            # location or else the choice is random.

            if numpy.random.binomial(1, p= follow_prob) == 1:

                # Move in the direction of the mother

                new_position = possible_steps[idx]

            else:

                # Choice is random
                new_position = self.random.choice(possible_steps)

            # Update the location of the agent
            self.model.grid.move_agent(self, new_position)

    def social_interaction(self):

        """ Identifies the ids of other individuals that currently 
        occupy the grid cell that the agent has just moved into and
         then logs them as social interactions in the social_links dataframe"""


        # Returns a list of all individuals that share the location of the agent

        friends = self.model.grid.get_cell_list_contents(self.pos) 

        # Makes sure the list does not contain the agent itself.

        friends = [obj for obj in friends if obj.unique_id != self.unique_id] 

        # If the agent has moved into a grid cell occupied by other agents, then 
        # an intreraction event is logged for each of them. 

        if len(friends) > 0:

            friend = random.choice(friends)

            self.prox_associations += 1

            if friend.tool_user is True: 
                self.tool_user_encounters += 1

            link = DataFrame({"source":[friend.unique_id] , "target": [self.unique_id]})

            #self.model.social_links = self.model.social_links.append(link)
            self.model.social_links = concat([self.model.social_links, link])


            # for i in range(len(friends)):
            #     friend = friends[i]
            
            #     # Updates the edges dataframe with this proximity interaction
                
            #     link = DataFrame({"source":[friend.unique_id] , "target": [self.unique_id]})
            #     self.model.social_links = self.model.social_links.append(link)

            #     # Updates the agent attributes number of encounters and 
            #     # number of tool-user encounters
                
            #     self.prox_associations += 1

            #     # Update the number of tool_user_encounters 
            #     if friend.tool_user == True:
                    
            #         self.tool_user_encounters += 1

            #     else:
            #         pass

            
            return friend
        else: 
            pass
            
        # Returns of list of agents in the grid-cell to be passed to the reproduce function


    def reproduce(self, mate):

        """ Simulate reproductive events that generate new individuals. Also
        responsible for determining whether the tool use trait is inherited."""

        # Ensure there is some one to mate with.     
        # Individuals cannot reproduce with their 
        # mothers so mothers are removed from the 
        # selection 

        if mate.unique_id != self.mother_tool_user:

        # Determine the inheritance of hair pattern 
           
            hair_x = self.hairpattern
            hair_y = mate.hairpattern
            hair_score = hair_x + hair_y

            if hair_score == 4: # Both agents have hair pattern of 2
                hair = 2 # Therefore, the inherited hair pattern will have a hairpattern of 2

            elif hair_score == 3: # One agent has a hair pattern of one and the other agent has pattern of 2
                hair = random.randint(1,2) # hair pattern is then randomly chosen

            elif hair_score == 2: # Both agents have a hair pattern of 1
                hair = 1 # inherited hair pattern is 1
            else:
                pass

        # Creates a new individual. The hair variable is then passed to the offspring.
        
            offspring = Monkey(unique_id=self.model.next_id(),
                            model=self.model,
                            tool_user=False,
                            mom=self.unique_id, # records the id of the mother
                            mom_user=self.tool_user, # records the tool use status of the mother
                            hair = hair) # detemines hair pattern, see above.

        # Determines if the offsping inherits the tool_use trait.

            if offspring.hairpattern == 2: # The offspring can only inherit the tool-use trait it inherited a hair pattern of 2.

                if mate.tool_trait is True and mate.hairpattern == 2: # Check to make sure one or both of the parent agents possess the tool-use trait.
                    offspring.tool_trait = True
                elif self.tool_trait is True and self.hairpattern == 2:
                    offspring.tool_trait = True
                else:
                    offspring.tool_trait = False
            
            else:
                offspring.tool_trait = False

            

        ## Agent is added to the grid space and schedule
            self.model.grid.place_agent(offspring, self.pos)
            self.model.schedule.add(offspring)

        ## edges connecting the new individual to its "mother" are added.
            link = DataFrame({"source": [self.unique_id], "target": [offspring.unique_id]})
            
            #self.model.ancestry_links = self.model.ancestry_links.append(link)
            self.model.ancestry_links = concat([self.model.ancestry_links, link])
        else:
            
            pass
                
    def learn(self, friend, lr_multiplier = 5):
        
        """ Determine whether an individual becomes a tool user. The 
        criteria for learning differ between the two modes of transmission"""

        # Makes sure the individual who has a chance to learn is of the correct age and not already a tool-user.
        if self.age >= 25 and self.tool_user is False: 
            
            # Draws a random number between 0 and 100
            x = random.uniform(0, 100) 
            
            # The conditions for learning when the mode of transmission is social.
            if self.model.transmission_mode == "social": 
                
                if friend is not None and friend.tool_user is True:
                
                    # If the number of tool_user_encounters is less than x then the individual will learn tool use
                    if x < (self.tool_user_encounters * lr_multiplier):
                        
                        self.tool_user = True # updates the tool user status to True
                        self.age_learned_tool_use = self.age # record the age at which tool use is expressed
                        self.learned_tool_use = True # Makes sure the original tool-user at the beginning of the simulation
                        self.ts_learned = self.model.timestep # Updates the time-step that this occurred during
                        self.transmission_method = self.model.transmission_mode # record the transmission mode
                    
                    else:pass
                else:pass
            
            
            elif self.model.transmission_mode == "inherited":
                
                    if x < 85 and self.tool_trait is True:

                        self.tool_user = True # updates the tool user status to True
                        self.age_learned_tool_use = self.age # record the age at which tool use is expressed
                        self.learned_tool_use = True # Makes sure the original tool-user at the beginning of the simulation
                        self.ts_learned = self.model.timestep # Updates the time-step that this occurred during
                        self.transmission_method = self.model.transmission_mode # record the transmission mode
                    
                    else:
                        pass

            else: # For debugging
                print("Warning! No transmission mode selected! Debug Model")
                self.model.running = False
        else:
            pass

    def grow(self):
        self.age += 1 # Agents grow an age of 1 each time step

        # determines the probability of an individual dying at a given timestep the chances of dying increases as an
        # individual ages

        death_prob = .0001 + self.age/10000

        # Detemines if the individual dies this timestep, drawn from a binomial distribution with the chances of success
        # dependent on the death_prob

        die = numpy.random.binomial(1,death_prob, 1)

        if die == 1: # If the individiaul dies.

            # Update living to false    
            self.living = False 

            # All information recorded and exported
            node_dat = {"id": self.unique_id,
                        "run_id": self.model.run_id,
                        "living": self.living,
                        "tool_user": self.tool_user,
                        "learned_tool_use": self.tool_user,
                        "tool_user_encounters": self.tool_user_encounters,
                        "age_learned_tool_use": self.age_learned_tool_use,
                        "time_step_learned": self.ts_learned,
                        "learning_method": self.transmission_method,
                        "age": self.age,
                        "mother": self.mother,
                        "mother_tool_user": self.mother_tool_user,
                        "hair": self.hairpattern}

            # Appended to the nodes dataframe for export.
            self.model.node_data.append(node_dat)
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            pass

    def step(self):

        #Move
        self.move()

        #Interact Socially
        mates = self.social_interaction()
        if mates is not None:

            #Repoduce
            if len(self.model.schedule.agents) < self.model.Na:

                self.reproduce(mate=mates)

            else: pass

        else:pass
        #learn
        self.learn(friend=mates)

        #Age and Grow
        self.grow()


