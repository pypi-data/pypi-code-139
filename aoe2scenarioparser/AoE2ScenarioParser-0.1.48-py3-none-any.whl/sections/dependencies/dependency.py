import math
from uuid import UUID

from AoE2ScenarioParser.scenarios.scenario_store import getters
from AoE2ScenarioParser.sections.dependencies.dependency_action import DependencyAction
from AoE2ScenarioParser.sections.retrievers.retriever import Retriever


def refresh_targets(retriever_event, section, uuid):
    for target in retriever_event.dependency_target.targets:
        selected_retriever = select_retriever(target, section, uuid)
        execute_refresh_action(selected_retriever, section, uuid)


def execute_refresh_action(retriever, section, uuid):
    handle_retriever_dependency(retriever, "refresh", section, uuid)


def handle_retriever_dependency(retriever: Retriever, state, section, uuid: UUID):
    on_x = f'on_{state}'
    if not hasattr(retriever, on_x):
        return

    retriever_event = getattr(retriever, on_x)  # construct, push or refresh

    action = retriever_event.dependency_action

    if action == DependencyAction.REFRESH_SELF:
        execute_refresh_action(retriever, section, uuid)
    elif action == DependencyAction.REFRESH:
        refresh_targets(retriever_event, section, uuid)
    elif action in [DependencyAction.SET_VALUE, DependencyAction.SET_REPEAT]:
        value = execute_dependency_eval(retriever_event, section, uuid)
        if action == DependencyAction.SET_VALUE:
            retriever.set_data(value, affect_dirty=False)
        elif action == DependencyAction.SET_REPEAT:
            retriever.datatype.repeat = value


def execute_dependency_eval(retriever_event, section, uuid):
    eval_code = retriever_event.dependency_eval.eval_code
    eval_locals = retriever_event.dependency_eval.eval_locals
    targets = retriever_event.dependency_target.targets

    values = []
    for target in targets:
        values.append(select_retriever(target, section, uuid).data)

    for index, target in enumerate(targets):
        eval_locals[target[1]] = values[index]
    eval_locals['math'] = math

    return eval(eval_code, {}, eval_locals)


def select_retriever(target, section, uuid):
    if target[0] == "self":
        return section.retriever_map[target[1]]
    else:
        sections = getters.get_sections(uuid)
        return sections[target[0]].retriever_map[target[1]]
