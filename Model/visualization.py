from model_definition import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


h = 25
w = 25

def agent_portrayal(agent):

    portrayal = {"Shape": "circle",
                 "Color": "blue",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 1}

    if agent.tool_user is True:
        portrayal["Color"] = "red"

    if agent.learned_tool_use is True:
        portrayal["Color"] = "orange"

    return portrayal


grid = CanvasGrid(agent_portrayal, h, w)

server = ModularServer(Mendelian_Monkeys,
                       [grid],
                       "Mendelian Monkeys",
                       {"height": h,
                        "width": w,
                        "Na": 100,
                        "N_Starting_Tool_users": 1,
                        "runs_path" : "Viz",
                        "trans_mode": "social"})

server.port = 2345 # The default

server.launch()