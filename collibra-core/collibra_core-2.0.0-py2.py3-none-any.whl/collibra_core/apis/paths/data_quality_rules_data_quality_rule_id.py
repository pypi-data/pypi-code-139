from collibra_core.paths.data_quality_rules_data_quality_rule_id.get import ApiForget
from collibra_core.paths.data_quality_rules_data_quality_rule_id.delete import ApiFordelete
from collibra_core.paths.data_quality_rules_data_quality_rule_id.patch import ApiForpatch


class DataQualityRulesDataQualityRuleId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
