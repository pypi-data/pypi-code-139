from collibra_core.paths.complex_relations_complex_relation_id.get import ApiForget
from collibra_core.paths.complex_relations_complex_relation_id.delete import ApiFordelete
from collibra_core.paths.complex_relations_complex_relation_id.patch import ApiForpatch


class ComplexRelationsComplexRelationId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
