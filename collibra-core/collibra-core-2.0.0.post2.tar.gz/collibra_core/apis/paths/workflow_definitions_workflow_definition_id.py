from collibra_core.paths.workflow_definitions_workflow_definition_id.get import ApiForget
from collibra_core.paths.workflow_definitions_workflow_definition_id.delete import ApiFordelete
from collibra_core.paths.workflow_definitions_workflow_definition_id.patch import ApiForpatch


class WorkflowDefinitionsWorkflowDefinitionId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
