from model_definition import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


h = 25
w = 25

def agent_portrayal(agent):

    portrayal = {"Shape": "circle",
                 "Color": "blue",
                 "Filled": "true",
                 "Layer": 1,
                 "r": 1}
    if isinstance(agent, Monkey):

        if agent.tool_user is True:
            portrayal["Color"] = "red"

        if agent.learned_tool_use is True:
            portrayal["Color"] = "orange"

    elif isinstance(agent, ToolResource):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0


    return portrayal


grid = CanvasGrid(agent_portrayal, h, w)

server = ModularServer(Mendelian_Monkeys,
                       [grid],
                       "Mendelian Monkeys",
                       {"height": h,
                        "width": w,
                        "Na": 100,
                        "N_Starting_Tool_users": 1,
                        "attraction": 90,
                        "N_Resources": 1,
                        "runs_path" : "Viz",
                        "trans_mode": "resource_attraction"})

server.port = 2345 # The default

server.launch()