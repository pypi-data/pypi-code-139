from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


filename = "OUTPUT"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario", name="222")


def duplicate_trigger(trigger: Trigger):
    tm = trigger.get_scenario().trigger_manager

