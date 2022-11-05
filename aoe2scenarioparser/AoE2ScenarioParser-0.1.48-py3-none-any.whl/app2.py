from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

filename = "empty2p"
scenario = AoE2DEScenario\
    .from_file(f"{folder_de}{filename}.aoe2scenario")\
    .name("saomething")

tm, mm, um, xm, pm = scenario.trigger_manager, scenario.map_manager, scenario.unit_manager, \
                     scenario.xs_manager, scenario.player_manager

# Code here

scenario.write_to_file(f"{folder_de}{filename}_output.aoe2scenario")
