import typing_extensions

from collibra_core.paths import PathValues
from collibra_core.apis.paths.activities import Activities
from collibra_core.apis.paths.application_info import ApplicationInfo
from collibra_core.apis.paths.assignments import Assignments
from collibra_core.apis.paths.assignments_assignment_id import AssignmentsAssignmentId
from collibra_core.apis.paths.assignments_for_resource import AssignmentsForResource
from collibra_core.apis.paths.assignments_asset_asset_id import AssignmentsAssetAssetId
from collibra_core.apis.paths.assignments_asset_type_asset_type_id import AssignmentsAssetTypeAssetTypeId
from collibra_core.apis.paths.assignments_domain_domain_id_asset_types import AssignmentsDomainDomainIdAssetTypes
from collibra_core.apis.paths.assignments_asset_asset_id_attribute_types import AssignmentsAssetAssetIdAttributeTypes
from collibra_core.apis.paths.assignments_asset_asset_id_complex_relation_types import AssignmentsAssetAssetIdComplexRelationTypes
from collibra_core.apis.paths.assignments_asset_asset_id_relation_types import AssignmentsAssetAssetIdRelationTypes
from collibra_core.apis.paths.scopes import Scopes
from collibra_core.apis.paths.scopes_scope_id import ScopesScopeId
from collibra_core.apis.paths.diagram_pictures import DiagramPictures
from collibra_core.apis.paths.files import Files
from collibra_core.apis.paths.files_file_id import FilesFileId
from collibra_core.apis.paths.files_file_id_info import FilesFileIdInfo
from collibra_core.apis.paths.assets import Assets
from collibra_core.apis.paths.assets_bulk import AssetsBulk
from collibra_core.apis.paths.assets_asset_id_tags import AssetsAssetIdTags
from collibra_core.apis.paths.assets_asset_id import AssetsAssetId
from collibra_core.apis.paths.assets_asset_id_breadcrumb import AssetsAssetIdBreadcrumb
from collibra_core.apis.paths.assets_asset_id_attributes import AssetsAssetIdAttributes
from collibra_core.apis.paths.assets_asset_id_relations import AssetsAssetIdRelations
from collibra_core.apis.paths.assets_asset_id_responsibilities import AssetsAssetIdResponsibilities
from collibra_core.apis.paths.attachments import Attachments
from collibra_core.apis.paths.attachments_attachment_id import AttachmentsAttachmentId
from collibra_core.apis.paths.attachments_attachment_id_file import AttachmentsAttachmentIdFile
from collibra_core.apis.paths.attributes import Attributes
from collibra_core.apis.paths.attributes_bulk import AttributesBulk
from collibra_core.apis.paths.attributes_attribute_id import AttributesAttributeId
from collibra_core.apis.paths.comments import Comments
from collibra_core.apis.paths.comments_comment_id import CommentsCommentId
from collibra_core.apis.paths.communities_bulk import CommunitiesBulk
from collibra_core.apis.paths.communities import Communities
from collibra_core.apis.paths.communities_community_id import CommunitiesCommunityId
from collibra_core.apis.paths.communities_community_id_root import CommunitiesCommunityIdRoot
from collibra_core.apis.paths.communities_community_id_breadcrumb import CommunitiesCommunityIdBreadcrumb
from collibra_core.apis.paths.communities_removal_jobs import CommunitiesRemovalJobs
from collibra_core.apis.paths.complex_relations import ComplexRelations
from collibra_core.apis.paths.complex_relations_complex_relation_id import ComplexRelationsComplexRelationId
from collibra_core.apis.paths.complex_relations_export_csv_job import ComplexRelationsExportCsvJob
from collibra_core.apis.paths.complex_relations_export_csv import ComplexRelationsExportCsv
from collibra_core.apis.paths.complex_relations_export_csv_file import ComplexRelationsExportCsvFile
from collibra_core.apis.paths.complex_relations_export_excel_job import ComplexRelationsExportExcelJob
from collibra_core.apis.paths.complex_relations_export_excel_file import ComplexRelationsExportExcelFile
from collibra_core.apis.paths.domains import Domains
from collibra_core.apis.paths.domains_bulk import DomainsBulk
from collibra_core.apis.paths.domains_domain_id import DomainsDomainId
from collibra_core.apis.paths.domains_domain_id_breadcrumb import DomainsDomainIdBreadcrumb
from collibra_core.apis.paths.domains_removal_jobs import DomainsRemovalJobs
from collibra_core.apis.paths.issues import Issues
from collibra_core.apis.paths.issues_issue_id_community_community_id import IssuesIssueIdCommunityCommunityId
from collibra_core.apis.paths.jdbc import Jdbc
from collibra_core.apis.paths.ratings import Ratings
from collibra_core.apis.paths.ratings_rating_id import RatingsRatingId
from collibra_core.apis.paths.relations import Relations
from collibra_core.apis.paths.relations_bulk import RelationsBulk
from collibra_core.apis.paths.relations_relation_id import RelationsRelationId
from collibra_core.apis.paths.responsibilities_bulk import ResponsibilitiesBulk
from collibra_core.apis.paths.responsibilities import Responsibilities
from collibra_core.apis.paths.responsibilities_responsibility_id import ResponsibilitiesResponsibilityId
from collibra_core.apis.paths.tags_tag_id import TagsTagId
from collibra_core.apis.paths.tags_exists_tag_name import TagsExistsTagName
from collibra_core.apis.paths.tags import Tags
from collibra_core.apis.paths.tags_asset_asset_id import TagsAssetAssetId
from collibra_core.apis.paths.tags_merge import TagsMerge
from collibra_core.apis.paths.tags_bulk import TagsBulk
from collibra_core.apis.paths.jobs_job_id_canceled import JobsJobIdCanceled
from collibra_core.apis.paths.jobs import Jobs
from collibra_core.apis.paths.jobs_job_id import JobsJobId
from collibra_core.apis.paths.mappings import Mappings
from collibra_core.apis.paths.mappings_bulk import MappingsBulk
from collibra_core.apis.paths.mappings_mapping_id import MappingsMappingId
from collibra_core.apis.paths.mappings_external_system_external_system_id_external_entity_external_entity_id import MappingsExternalSystemExternalSystemIdExternalEntityExternalEntityId
from collibra_core.apis.paths.mappings_external_system_external_system_id_mapped_resource_mapped_resource_id import MappingsExternalSystemExternalSystemIdMappedResourceMappedResourceId
from collibra_core.apis.paths.mappings_external_system_external_entity_bulk import MappingsExternalSystemExternalEntityBulk
from collibra_core.apis.paths.mappings_external_system_mapped_resource_bulk import MappingsExternalSystemMappedResourceBulk
from collibra_core.apis.paths.mappings_external_system_external_system_id_removal_jobs import MappingsExternalSystemExternalSystemIdRemovalJobs
from collibra_core.apis.paths.mappings_removal_jobs import MappingsRemovalJobs
from collibra_core.apis.paths.asset_types import AssetTypes
from collibra_core.apis.paths.asset_types_bulk import AssetTypesBulk
from collibra_core.apis.paths.asset_types_asset_type_id import AssetTypesAssetTypeId
from collibra_core.apis.paths.asset_types_asset_type_id_parents import AssetTypesAssetTypeIdParents
from collibra_core.apis.paths.asset_types_asset_type_id_sub_types import AssetTypesAssetTypeIdSubTypes
from collibra_core.apis.paths.attribute_types import AttributeTypes
from collibra_core.apis.paths.attribute_types_bulk import AttributeTypesBulk
from collibra_core.apis.paths.attribute_types_attribute_type_id import AttributeTypesAttributeTypeId
from collibra_core.apis.paths.attribute_types_name_attribute_type_name import AttributeTypesNameAttributeTypeName
from collibra_core.apis.paths.complex_relation_types import ComplexRelationTypes
from collibra_core.apis.paths.complex_relation_types_complex_relation_type_id import ComplexRelationTypesComplexRelationTypeId
from collibra_core.apis.paths.domain_types import DomainTypes
from collibra_core.apis.paths.domain_types_bulk import DomainTypesBulk
from collibra_core.apis.paths.domain_types_domain_type_id import DomainTypesDomainTypeId
from collibra_core.apis.paths.domain_types_domain_type_id_sub_types import DomainTypesDomainTypeIdSubTypes
from collibra_core.apis.paths.relation_types import RelationTypes
from collibra_core.apis.paths.relation_types_bulk import RelationTypesBulk
from collibra_core.apis.paths.relation_types_relation_type_id import RelationTypesRelationTypeId
from collibra_core.apis.paths.statuses import Statuses
from collibra_core.apis.paths.statuses_bulk import StatusesBulk
from collibra_core.apis.paths.statuses_status_id import StatusesStatusId
from collibra_core.apis.paths.statuses_name_status_name import StatusesNameStatusName
from collibra_core.apis.paths.navigation_most_viewed import NavigationMostViewed
from collibra_core.apis.paths.navigation_recently_viewed import NavigationRecentlyViewed
from collibra_core.apis.paths.data_quality_rules import DataQualityRules
from collibra_core.apis.paths.data_quality_rules_data_quality_rule_id import DataQualityRulesDataQualityRuleId
from collibra_core.apis.paths.output_module_export_csv import OutputModuleExportCsv
from collibra_core.apis.paths.output_module_export_csv_job import OutputModuleExportCsvJob
from collibra_core.apis.paths.output_module_export_csv_file import OutputModuleExportCsvFile
from collibra_core.apis.paths.output_module_export_excel_job import OutputModuleExportExcelJob
from collibra_core.apis.paths.output_module_export_excel_file import OutputModuleExportExcelFile
from collibra_core.apis.paths.output_module_export_json import OutputModuleExportJson
from collibra_core.apis.paths.output_module_export_json_job import OutputModuleExportJsonJob
from collibra_core.apis.paths.output_module_export_json_file import OutputModuleExportJsonFile
from collibra_core.apis.paths.output_module_export_xml import OutputModuleExportXml
from collibra_core.apis.paths.output_module_export_xml_job import OutputModuleExportXmlJob
from collibra_core.apis.paths.output_module_export_xml_file import OutputModuleExportXmlFile
from collibra_core.apis.paths.output_module_table_view_configs_view_id_view_id import OutputModuleTableViewConfigsViewIdViewId
from collibra_core.apis.paths.reporting_insights_download import ReportingInsightsDownload
from collibra_core.apis.paths.roles import Roles
from collibra_core.apis.paths.roles_role_id import RolesRoleId
from collibra_core.apis.paths.security_saml_certificate_type import SecuritySamlCertificateType
from collibra_core.apis.paths.security_saml import SecuritySaml
from collibra_core.apis.paths.auth_sessions_current import AuthSessionsCurrent
from collibra_core.apis.paths.auth_sessions_heartbeat import AuthSessionsHeartbeat
from collibra_core.apis.paths.auth_sessions import AuthSessions
from collibra_core.apis.paths.users import Users
from collibra_core.apis.paths.users_user_id_user_groups import UsersUserIdUserGroups
from collibra_core.apis.paths.users_bulk import UsersBulk
from collibra_core.apis.paths.users_user_id import UsersUserId
from collibra_core.apis.paths.users_user_id_avatar import UsersUserIdAvatar
from collibra_core.apis.paths.users_current import UsersCurrent
from collibra_core.apis.paths.users_current_permissions import UsersCurrentPermissions
from collibra_core.apis.paths.users_email_email_address import UsersEmailEmailAddress
from collibra_core.apis.paths.users_user_id_license_type import UsersUserIdLicenseType
from collibra_core.apis.paths.user_groups import UserGroups
from collibra_core.apis.paths.user_groups_user_group_id_users import UserGroupsUserGroupIdUsers
from collibra_core.apis.paths.user_groups_user_group_id import UserGroupsUserGroupId
from collibra_core.apis.paths.validation import Validation
from collibra_core.apis.paths.validation_asset_id import ValidationAssetId
from collibra_core.apis.paths.validation_bulk import ValidationBulk
from collibra_core.apis.paths.view_permissions import ViewPermissions
from collibra_core.apis.paths.view_permissions_view_permission_id import ViewPermissionsViewPermissionId
from collibra_core.apis.paths.workflow_definitions_workflow_definition_id_asset_type_assignment_rules import WorkflowDefinitionsWorkflowDefinitionIdAssetTypeAssignmentRules
from collibra_core.apis.paths.workflow_definitions_workflow_definition_id_domain_type_assignment_rules import WorkflowDefinitionsWorkflowDefinitionIdDomainTypeAssignmentRules
from collibra_core.apis.paths.workflow_definitions_workflow_definition_id_asset_type_assignment_rules_rule_id import WorkflowDefinitionsWorkflowDefinitionIdAssetTypeAssignmentRulesRuleId
from collibra_core.apis.paths.workflow_definitions_workflow_definition_id_domain_type_assignment_rules_rule_id import WorkflowDefinitionsWorkflowDefinitionIdDomainTypeAssignmentRulesRuleId
from collibra_core.apis.paths.workflow_definitions_workflow_definition_id import WorkflowDefinitionsWorkflowDefinitionId
from collibra_core.apis.paths.workflow_definitions import WorkflowDefinitions
from collibra_core.apis.paths.workflow_definitions_workflow_definition_workflow_definition_id_configuration_start_form_data import WorkflowDefinitionsWorkflowDefinitionWorkflowDefinitionIdConfigurationStartFormData
from collibra_core.apis.paths.workflow_definitions_start_events import WorkflowDefinitionsStartEvents
from collibra_core.apis.paths.workflow_definitions_workflow_definition_workflow_definition_id_start_form_data import WorkflowDefinitionsWorkflowDefinitionWorkflowDefinitionIdStartFormData
from collibra_core.apis.paths.workflow_definitions_process_process_id import WorkflowDefinitionsProcessProcessId
from collibra_core.apis.paths.workflow_definitions_workflow_definition_id_diagram import WorkflowDefinitionsWorkflowDefinitionIdDiagram
from collibra_core.apis.paths.workflow_definitions_workflow_definition_id_xml import WorkflowDefinitionsWorkflowDefinitionIdXml
from collibra_core.apis.paths.workflow_definitions_workflow_definition_id_assignment_rules_rule_id import WorkflowDefinitionsWorkflowDefinitionIdAssignmentRulesRuleId
from collibra_core.apis.paths.workflow_definitions_removal_jobs import WorkflowDefinitionsRemovalJobs
from collibra_core.apis.paths.workflow_instances_workflow_instance_id_canceled import WorkflowInstancesWorkflowInstanceIdCanceled
from collibra_core.apis.paths.workflow_instances import WorkflowInstances
from collibra_core.apis.paths.workflow_instances_workflow_instance_id_diagram import WorkflowInstancesWorkflowInstanceIdDiagram
from collibra_core.apis.paths.workflow_instances_process_instance_id_message_events_message_name import WorkflowInstancesProcessInstanceIdMessageEventsMessageName
from collibra_core.apis.paths.workflow_instances_start_jobs import WorkflowInstancesStartJobs
from collibra_core.apis.paths.workflow_tasks_workflow_task_id_canceled import WorkflowTasksWorkflowTaskIdCanceled
from collibra_core.apis.paths.workflow_tasks_completed import WorkflowTasksCompleted
from collibra_core.apis.paths.workflow_tasks import WorkflowTasks
from collibra_core.apis.paths.workflow_tasks_workflow_task_id_task_form_data import WorkflowTasksWorkflowTaskIdTaskFormData
from collibra_core.apis.paths.workflow_tasks_workflow_task_id import WorkflowTasksWorkflowTaskId
from collibra_core.apis.paths.workflow_tasks_workflow_task_id_reassign import WorkflowTasksWorkflowTaskIdReassign

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.ACTIVITIES: Activities,
        PathValues.APPLICATION_INFO: ApplicationInfo,
        PathValues.ASSIGNMENTS: Assignments,
        PathValues.ASSIGNMENTS_ASSIGNMENT_ID: AssignmentsAssignmentId,
        PathValues.ASSIGNMENTS_FOR_RESOURCE: AssignmentsForResource,
        PathValues.ASSIGNMENTS_ASSET_ASSET_ID: AssignmentsAssetAssetId,
        PathValues.ASSIGNMENTS_ASSET_TYPE_ASSET_TYPE_ID: AssignmentsAssetTypeAssetTypeId,
        PathValues.ASSIGNMENTS_DOMAIN_DOMAIN_ID_ASSET_TYPES: AssignmentsDomainDomainIdAssetTypes,
        PathValues.ASSIGNMENTS_ASSET_ASSET_ID_ATTRIBUTE_TYPES: AssignmentsAssetAssetIdAttributeTypes,
        PathValues.ASSIGNMENTS_ASSET_ASSET_ID_COMPLEX_RELATION_TYPES: AssignmentsAssetAssetIdComplexRelationTypes,
        PathValues.ASSIGNMENTS_ASSET_ASSET_ID_RELATION_TYPES: AssignmentsAssetAssetIdRelationTypes,
        PathValues.SCOPES: Scopes,
        PathValues.SCOPES_SCOPE_ID: ScopesScopeId,
        PathValues.DIAGRAM_PICTURES: DiagramPictures,
        PathValues.FILES: Files,
        PathValues.FILES_FILE_ID: FilesFileId,
        PathValues.FILES_FILE_ID_INFO: FilesFileIdInfo,
        PathValues.ASSETS: Assets,
        PathValues.ASSETS_BULK: AssetsBulk,
        PathValues.ASSETS_ASSET_ID_TAGS: AssetsAssetIdTags,
        PathValues.ASSETS_ASSET_ID: AssetsAssetId,
        PathValues.ASSETS_ASSET_ID_BREADCRUMB: AssetsAssetIdBreadcrumb,
        PathValues.ASSETS_ASSET_ID_ATTRIBUTES: AssetsAssetIdAttributes,
        PathValues.ASSETS_ASSET_ID_RELATIONS: AssetsAssetIdRelations,
        PathValues.ASSETS_ASSET_ID_RESPONSIBILITIES: AssetsAssetIdResponsibilities,
        PathValues.ATTACHMENTS: Attachments,
        PathValues.ATTACHMENTS_ATTACHMENT_ID: AttachmentsAttachmentId,
        PathValues.ATTACHMENTS_ATTACHMENT_ID_FILE: AttachmentsAttachmentIdFile,
        PathValues.ATTRIBUTES: Attributes,
        PathValues.ATTRIBUTES_BULK: AttributesBulk,
        PathValues.ATTRIBUTES_ATTRIBUTE_ID: AttributesAttributeId,
        PathValues.COMMENTS: Comments,
        PathValues.COMMENTS_COMMENT_ID: CommentsCommentId,
        PathValues.COMMUNITIES_BULK: CommunitiesBulk,
        PathValues.COMMUNITIES: Communities,
        PathValues.COMMUNITIES_COMMUNITY_ID: CommunitiesCommunityId,
        PathValues.COMMUNITIES_COMMUNITY_ID_ROOT: CommunitiesCommunityIdRoot,
        PathValues.COMMUNITIES_COMMUNITY_ID_BREADCRUMB: CommunitiesCommunityIdBreadcrumb,
        PathValues.COMMUNITIES_REMOVAL_JOBS: CommunitiesRemovalJobs,
        PathValues.COMPLEX_RELATIONS: ComplexRelations,
        PathValues.COMPLEX_RELATIONS_COMPLEX_RELATION_ID: ComplexRelationsComplexRelationId,
        PathValues.COMPLEX_RELATIONS_EXPORT_CSVJOB: ComplexRelationsExportCsvJob,
        PathValues.COMPLEX_RELATIONS_EXPORT_CSV: ComplexRelationsExportCsv,
        PathValues.COMPLEX_RELATIONS_EXPORT_CSVFILE: ComplexRelationsExportCsvFile,
        PathValues.COMPLEX_RELATIONS_EXPORT_EXCELJOB: ComplexRelationsExportExcelJob,
        PathValues.COMPLEX_RELATIONS_EXPORT_EXCELFILE: ComplexRelationsExportExcelFile,
        PathValues.DOMAINS: Domains,
        PathValues.DOMAINS_BULK: DomainsBulk,
        PathValues.DOMAINS_DOMAIN_ID: DomainsDomainId,
        PathValues.DOMAINS_DOMAIN_ID_BREADCRUMB: DomainsDomainIdBreadcrumb,
        PathValues.DOMAINS_REMOVAL_JOBS: DomainsRemovalJobs,
        PathValues.ISSUES: Issues,
        PathValues.ISSUES_ISSUE_ID_COMMUNITY_COMMUNITY_ID: IssuesIssueIdCommunityCommunityId,
        PathValues.JDBC: Jdbc,
        PathValues.RATINGS: Ratings,
        PathValues.RATINGS_RATING_ID: RatingsRatingId,
        PathValues.RELATIONS: Relations,
        PathValues.RELATIONS_BULK: RelationsBulk,
        PathValues.RELATIONS_RELATION_ID: RelationsRelationId,
        PathValues.RESPONSIBILITIES_BULK: ResponsibilitiesBulk,
        PathValues.RESPONSIBILITIES: Responsibilities,
        PathValues.RESPONSIBILITIES_RESPONSIBILITY_ID: ResponsibilitiesResponsibilityId,
        PathValues.TAGS_TAG_ID: TagsTagId,
        PathValues.TAGS_EXISTS_TAG_NAME: TagsExistsTagName,
        PathValues.TAGS: Tags,
        PathValues.TAGS_ASSET_ASSET_ID: TagsAssetAssetId,
        PathValues.TAGS_MERGE: TagsMerge,
        PathValues.TAGS_BULK: TagsBulk,
        PathValues.JOBS_JOB_ID_CANCELED: JobsJobIdCanceled,
        PathValues.JOBS: Jobs,
        PathValues.JOBS_JOB_ID: JobsJobId,
        PathValues.MAPPINGS: Mappings,
        PathValues.MAPPINGS_BULK: MappingsBulk,
        PathValues.MAPPINGS_MAPPING_ID: MappingsMappingId,
        PathValues.MAPPINGS_EXTERNAL_SYSTEM_EXTERNAL_SYSTEM_ID_EXTERNAL_ENTITY_EXTERNAL_ENTITY_ID: MappingsExternalSystemExternalSystemIdExternalEntityExternalEntityId,
        PathValues.MAPPINGS_EXTERNAL_SYSTEM_EXTERNAL_SYSTEM_ID_MAPPED_RESOURCE_MAPPED_RESOURCE_ID: MappingsExternalSystemExternalSystemIdMappedResourceMappedResourceId,
        PathValues.MAPPINGS_EXTERNAL_SYSTEM_EXTERNAL_ENTITY_BULK: MappingsExternalSystemExternalEntityBulk,
        PathValues.MAPPINGS_EXTERNAL_SYSTEM_MAPPED_RESOURCE_BULK: MappingsExternalSystemMappedResourceBulk,
        PathValues.MAPPINGS_EXTERNAL_SYSTEM_EXTERNAL_SYSTEM_ID_REMOVAL_JOBS: MappingsExternalSystemExternalSystemIdRemovalJobs,
        PathValues.MAPPINGS_REMOVAL_JOBS: MappingsRemovalJobs,
        PathValues.ASSET_TYPES: AssetTypes,
        PathValues.ASSET_TYPES_BULK: AssetTypesBulk,
        PathValues.ASSET_TYPES_ASSET_TYPE_ID: AssetTypesAssetTypeId,
        PathValues.ASSET_TYPES_ASSET_TYPE_ID_PARENTS: AssetTypesAssetTypeIdParents,
        PathValues.ASSET_TYPES_ASSET_TYPE_ID_SUB_TYPES: AssetTypesAssetTypeIdSubTypes,
        PathValues.ATTRIBUTE_TYPES: AttributeTypes,
        PathValues.ATTRIBUTE_TYPES_BULK: AttributeTypesBulk,
        PathValues.ATTRIBUTE_TYPES_ATTRIBUTE_TYPE_ID: AttributeTypesAttributeTypeId,
        PathValues.ATTRIBUTE_TYPES_NAME_ATTRIBUTE_TYPE_NAME: AttributeTypesNameAttributeTypeName,
        PathValues.COMPLEX_RELATION_TYPES: ComplexRelationTypes,
        PathValues.COMPLEX_RELATION_TYPES_COMPLEX_RELATION_TYPE_ID: ComplexRelationTypesComplexRelationTypeId,
        PathValues.DOMAIN_TYPES: DomainTypes,
        PathValues.DOMAIN_TYPES_BULK: DomainTypesBulk,
        PathValues.DOMAIN_TYPES_DOMAIN_TYPE_ID: DomainTypesDomainTypeId,
        PathValues.DOMAIN_TYPES_DOMAIN_TYPE_ID_SUB_TYPES: DomainTypesDomainTypeIdSubTypes,
        PathValues.RELATION_TYPES: RelationTypes,
        PathValues.RELATION_TYPES_BULK: RelationTypesBulk,
        PathValues.RELATION_TYPES_RELATION_TYPE_ID: RelationTypesRelationTypeId,
        PathValues.STATUSES: Statuses,
        PathValues.STATUSES_BULK: StatusesBulk,
        PathValues.STATUSES_STATUS_ID: StatusesStatusId,
        PathValues.STATUSES_NAME_STATUS_NAME: StatusesNameStatusName,
        PathValues.NAVIGATION_MOST_VIEWED: NavigationMostViewed,
        PathValues.NAVIGATION_RECENTLY_VIEWED: NavigationRecentlyViewed,
        PathValues.DATA_QUALITY_RULES: DataQualityRules,
        PathValues.DATA_QUALITY_RULES_DATA_QUALITY_RULE_ID: DataQualityRulesDataQualityRuleId,
        PathValues.OUTPUT_MODULE_EXPORT_CSV: OutputModuleExportCsv,
        PathValues.OUTPUT_MODULE_EXPORT_CSVJOB: OutputModuleExportCsvJob,
        PathValues.OUTPUT_MODULE_EXPORT_CSVFILE: OutputModuleExportCsvFile,
        PathValues.OUTPUT_MODULE_EXPORT_EXCELJOB: OutputModuleExportExcelJob,
        PathValues.OUTPUT_MODULE_EXPORT_EXCELFILE: OutputModuleExportExcelFile,
        PathValues.OUTPUT_MODULE_EXPORT_JSON: OutputModuleExportJson,
        PathValues.OUTPUT_MODULE_EXPORT_JSONJOB: OutputModuleExportJsonJob,
        PathValues.OUTPUT_MODULE_EXPORT_JSONFILE: OutputModuleExportJsonFile,
        PathValues.OUTPUT_MODULE_EXPORT_XML: OutputModuleExportXml,
        PathValues.OUTPUT_MODULE_EXPORT_XMLJOB: OutputModuleExportXmlJob,
        PathValues.OUTPUT_MODULE_EXPORT_XMLFILE: OutputModuleExportXmlFile,
        PathValues.OUTPUT_MODULE_TABLE_VIEW_CONFIGS_VIEW_ID_VIEW_ID: OutputModuleTableViewConfigsViewIdViewId,
        PathValues.REPORTING_INSIGHTS_DOWNLOAD: ReportingInsightsDownload,
        PathValues.ROLES: Roles,
        PathValues.ROLES_ROLE_ID: RolesRoleId,
        PathValues.SECURITY_SAML_CERTIFICATE_TYPE: SecuritySamlCertificateType,
        PathValues.SECURITY_SAML: SecuritySaml,
        PathValues.AUTH_SESSIONS_CURRENT: AuthSessionsCurrent,
        PathValues.AUTH_SESSIONS_HEARTBEAT: AuthSessionsHeartbeat,
        PathValues.AUTH_SESSIONS: AuthSessions,
        PathValues.USERS: Users,
        PathValues.USERS_USER_ID_USER_GROUPS: UsersUserIdUserGroups,
        PathValues.USERS_BULK: UsersBulk,
        PathValues.USERS_USER_ID: UsersUserId,
        PathValues.USERS_USER_ID_AVATAR: UsersUserIdAvatar,
        PathValues.USERS_CURRENT: UsersCurrent,
        PathValues.USERS_CURRENT_PERMISSIONS: UsersCurrentPermissions,
        PathValues.USERS_EMAIL_EMAIL_ADDRESS: UsersEmailEmailAddress,
        PathValues.USERS_USER_ID_LICENSE_TYPE: UsersUserIdLicenseType,
        PathValues.USER_GROUPS: UserGroups,
        PathValues.USER_GROUPS_USER_GROUP_ID_USERS: UserGroupsUserGroupIdUsers,
        PathValues.USER_GROUPS_USER_GROUP_ID: UserGroupsUserGroupId,
        PathValues.VALIDATION: Validation,
        PathValues.VALIDATION_ASSET_ID: ValidationAssetId,
        PathValues.VALIDATION_BULK: ValidationBulk,
        PathValues.VIEW_PERMISSIONS: ViewPermissions,
        PathValues.VIEW_PERMISSIONS_VIEW_PERMISSION_ID: ViewPermissionsViewPermissionId,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_ASSET_TYPE_ASSIGNMENT_RULES: WorkflowDefinitionsWorkflowDefinitionIdAssetTypeAssignmentRules,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_DOMAIN_TYPE_ASSIGNMENT_RULES: WorkflowDefinitionsWorkflowDefinitionIdDomainTypeAssignmentRules,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_ASSET_TYPE_ASSIGNMENT_RULES_RULE_ID: WorkflowDefinitionsWorkflowDefinitionIdAssetTypeAssignmentRulesRuleId,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_DOMAIN_TYPE_ASSIGNMENT_RULES_RULE_ID: WorkflowDefinitionsWorkflowDefinitionIdDomainTypeAssignmentRulesRuleId,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID: WorkflowDefinitionsWorkflowDefinitionId,
        PathValues.WORKFLOW_DEFINITIONS: WorkflowDefinitions,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_WORKFLOW_DEFINITION_ID_CONFIGURATION_START_FORM_DATA: WorkflowDefinitionsWorkflowDefinitionWorkflowDefinitionIdConfigurationStartFormData,
        PathValues.WORKFLOW_DEFINITIONS_START_EVENTS: WorkflowDefinitionsStartEvents,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_WORKFLOW_DEFINITION_ID_START_FORM_DATA: WorkflowDefinitionsWorkflowDefinitionWorkflowDefinitionIdStartFormData,
        PathValues.WORKFLOW_DEFINITIONS_PROCESS_PROCESS_ID: WorkflowDefinitionsProcessProcessId,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_DIAGRAM: WorkflowDefinitionsWorkflowDefinitionIdDiagram,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_XML: WorkflowDefinitionsWorkflowDefinitionIdXml,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_ASSIGNMENT_RULES_RULE_ID: WorkflowDefinitionsWorkflowDefinitionIdAssignmentRulesRuleId,
        PathValues.WORKFLOW_DEFINITIONS_REMOVAL_JOBS: WorkflowDefinitionsRemovalJobs,
        PathValues.WORKFLOW_INSTANCES_WORKFLOW_INSTANCE_ID_CANCELED: WorkflowInstancesWorkflowInstanceIdCanceled,
        PathValues.WORKFLOW_INSTANCES: WorkflowInstances,
        PathValues.WORKFLOW_INSTANCES_WORKFLOW_INSTANCE_ID_DIAGRAM: WorkflowInstancesWorkflowInstanceIdDiagram,
        PathValues.WORKFLOW_INSTANCES_PROCESS_INSTANCE_ID_MESSAGE_EVENTS_MESSAGE_NAME: WorkflowInstancesProcessInstanceIdMessageEventsMessageName,
        PathValues.WORKFLOW_INSTANCES_START_JOBS: WorkflowInstancesStartJobs,
        PathValues.WORKFLOW_TASKS_WORKFLOW_TASK_ID_CANCELED: WorkflowTasksWorkflowTaskIdCanceled,
        PathValues.WORKFLOW_TASKS_COMPLETED: WorkflowTasksCompleted,
        PathValues.WORKFLOW_TASKS: WorkflowTasks,
        PathValues.WORKFLOW_TASKS_WORKFLOW_TASK_ID_TASK_FORM_DATA: WorkflowTasksWorkflowTaskIdTaskFormData,
        PathValues.WORKFLOW_TASKS_WORKFLOW_TASK_ID: WorkflowTasksWorkflowTaskId,
        PathValues.WORKFLOW_TASKS_WORKFLOW_TASK_ID_REASSIGN: WorkflowTasksWorkflowTaskIdReassign,
    }
)

path_to_api = PathToApi(
    {
        PathValues.ACTIVITIES: Activities,
        PathValues.APPLICATION_INFO: ApplicationInfo,
        PathValues.ASSIGNMENTS: Assignments,
        PathValues.ASSIGNMENTS_ASSIGNMENT_ID: AssignmentsAssignmentId,
        PathValues.ASSIGNMENTS_FOR_RESOURCE: AssignmentsForResource,
        PathValues.ASSIGNMENTS_ASSET_ASSET_ID: AssignmentsAssetAssetId,
        PathValues.ASSIGNMENTS_ASSET_TYPE_ASSET_TYPE_ID: AssignmentsAssetTypeAssetTypeId,
        PathValues.ASSIGNMENTS_DOMAIN_DOMAIN_ID_ASSET_TYPES: AssignmentsDomainDomainIdAssetTypes,
        PathValues.ASSIGNMENTS_ASSET_ASSET_ID_ATTRIBUTE_TYPES: AssignmentsAssetAssetIdAttributeTypes,
        PathValues.ASSIGNMENTS_ASSET_ASSET_ID_COMPLEX_RELATION_TYPES: AssignmentsAssetAssetIdComplexRelationTypes,
        PathValues.ASSIGNMENTS_ASSET_ASSET_ID_RELATION_TYPES: AssignmentsAssetAssetIdRelationTypes,
        PathValues.SCOPES: Scopes,
        PathValues.SCOPES_SCOPE_ID: ScopesScopeId,
        PathValues.DIAGRAM_PICTURES: DiagramPictures,
        PathValues.FILES: Files,
        PathValues.FILES_FILE_ID: FilesFileId,
        PathValues.FILES_FILE_ID_INFO: FilesFileIdInfo,
        PathValues.ASSETS: Assets,
        PathValues.ASSETS_BULK: AssetsBulk,
        PathValues.ASSETS_ASSET_ID_TAGS: AssetsAssetIdTags,
        PathValues.ASSETS_ASSET_ID: AssetsAssetId,
        PathValues.ASSETS_ASSET_ID_BREADCRUMB: AssetsAssetIdBreadcrumb,
        PathValues.ASSETS_ASSET_ID_ATTRIBUTES: AssetsAssetIdAttributes,
        PathValues.ASSETS_ASSET_ID_RELATIONS: AssetsAssetIdRelations,
        PathValues.ASSETS_ASSET_ID_RESPONSIBILITIES: AssetsAssetIdResponsibilities,
        PathValues.ATTACHMENTS: Attachments,
        PathValues.ATTACHMENTS_ATTACHMENT_ID: AttachmentsAttachmentId,
        PathValues.ATTACHMENTS_ATTACHMENT_ID_FILE: AttachmentsAttachmentIdFile,
        PathValues.ATTRIBUTES: Attributes,
        PathValues.ATTRIBUTES_BULK: AttributesBulk,
        PathValues.ATTRIBUTES_ATTRIBUTE_ID: AttributesAttributeId,
        PathValues.COMMENTS: Comments,
        PathValues.COMMENTS_COMMENT_ID: CommentsCommentId,
        PathValues.COMMUNITIES_BULK: CommunitiesBulk,
        PathValues.COMMUNITIES: Communities,
        PathValues.COMMUNITIES_COMMUNITY_ID: CommunitiesCommunityId,
        PathValues.COMMUNITIES_COMMUNITY_ID_ROOT: CommunitiesCommunityIdRoot,
        PathValues.COMMUNITIES_COMMUNITY_ID_BREADCRUMB: CommunitiesCommunityIdBreadcrumb,
        PathValues.COMMUNITIES_REMOVAL_JOBS: CommunitiesRemovalJobs,
        PathValues.COMPLEX_RELATIONS: ComplexRelations,
        PathValues.COMPLEX_RELATIONS_COMPLEX_RELATION_ID: ComplexRelationsComplexRelationId,
        PathValues.COMPLEX_RELATIONS_EXPORT_CSVJOB: ComplexRelationsExportCsvJob,
        PathValues.COMPLEX_RELATIONS_EXPORT_CSV: ComplexRelationsExportCsv,
        PathValues.COMPLEX_RELATIONS_EXPORT_CSVFILE: ComplexRelationsExportCsvFile,
        PathValues.COMPLEX_RELATIONS_EXPORT_EXCELJOB: ComplexRelationsExportExcelJob,
        PathValues.COMPLEX_RELATIONS_EXPORT_EXCELFILE: ComplexRelationsExportExcelFile,
        PathValues.DOMAINS: Domains,
        PathValues.DOMAINS_BULK: DomainsBulk,
        PathValues.DOMAINS_DOMAIN_ID: DomainsDomainId,
        PathValues.DOMAINS_DOMAIN_ID_BREADCRUMB: DomainsDomainIdBreadcrumb,
        PathValues.DOMAINS_REMOVAL_JOBS: DomainsRemovalJobs,
        PathValues.ISSUES: Issues,
        PathValues.ISSUES_ISSUE_ID_COMMUNITY_COMMUNITY_ID: IssuesIssueIdCommunityCommunityId,
        PathValues.JDBC: Jdbc,
        PathValues.RATINGS: Ratings,
        PathValues.RATINGS_RATING_ID: RatingsRatingId,
        PathValues.RELATIONS: Relations,
        PathValues.RELATIONS_BULK: RelationsBulk,
        PathValues.RELATIONS_RELATION_ID: RelationsRelationId,
        PathValues.RESPONSIBILITIES_BULK: ResponsibilitiesBulk,
        PathValues.RESPONSIBILITIES: Responsibilities,
        PathValues.RESPONSIBILITIES_RESPONSIBILITY_ID: ResponsibilitiesResponsibilityId,
        PathValues.TAGS_TAG_ID: TagsTagId,
        PathValues.TAGS_EXISTS_TAG_NAME: TagsExistsTagName,
        PathValues.TAGS: Tags,
        PathValues.TAGS_ASSET_ASSET_ID: TagsAssetAssetId,
        PathValues.TAGS_MERGE: TagsMerge,
        PathValues.TAGS_BULK: TagsBulk,
        PathValues.JOBS_JOB_ID_CANCELED: JobsJobIdCanceled,
        PathValues.JOBS: Jobs,
        PathValues.JOBS_JOB_ID: JobsJobId,
        PathValues.MAPPINGS: Mappings,
        PathValues.MAPPINGS_BULK: MappingsBulk,
        PathValues.MAPPINGS_MAPPING_ID: MappingsMappingId,
        PathValues.MAPPINGS_EXTERNAL_SYSTEM_EXTERNAL_SYSTEM_ID_EXTERNAL_ENTITY_EXTERNAL_ENTITY_ID: MappingsExternalSystemExternalSystemIdExternalEntityExternalEntityId,
        PathValues.MAPPINGS_EXTERNAL_SYSTEM_EXTERNAL_SYSTEM_ID_MAPPED_RESOURCE_MAPPED_RESOURCE_ID: MappingsExternalSystemExternalSystemIdMappedResourceMappedResourceId,
        PathValues.MAPPINGS_EXTERNAL_SYSTEM_EXTERNAL_ENTITY_BULK: MappingsExternalSystemExternalEntityBulk,
        PathValues.MAPPINGS_EXTERNAL_SYSTEM_MAPPED_RESOURCE_BULK: MappingsExternalSystemMappedResourceBulk,
        PathValues.MAPPINGS_EXTERNAL_SYSTEM_EXTERNAL_SYSTEM_ID_REMOVAL_JOBS: MappingsExternalSystemExternalSystemIdRemovalJobs,
        PathValues.MAPPINGS_REMOVAL_JOBS: MappingsRemovalJobs,
        PathValues.ASSET_TYPES: AssetTypes,
        PathValues.ASSET_TYPES_BULK: AssetTypesBulk,
        PathValues.ASSET_TYPES_ASSET_TYPE_ID: AssetTypesAssetTypeId,
        PathValues.ASSET_TYPES_ASSET_TYPE_ID_PARENTS: AssetTypesAssetTypeIdParents,
        PathValues.ASSET_TYPES_ASSET_TYPE_ID_SUB_TYPES: AssetTypesAssetTypeIdSubTypes,
        PathValues.ATTRIBUTE_TYPES: AttributeTypes,
        PathValues.ATTRIBUTE_TYPES_BULK: AttributeTypesBulk,
        PathValues.ATTRIBUTE_TYPES_ATTRIBUTE_TYPE_ID: AttributeTypesAttributeTypeId,
        PathValues.ATTRIBUTE_TYPES_NAME_ATTRIBUTE_TYPE_NAME: AttributeTypesNameAttributeTypeName,
        PathValues.COMPLEX_RELATION_TYPES: ComplexRelationTypes,
        PathValues.COMPLEX_RELATION_TYPES_COMPLEX_RELATION_TYPE_ID: ComplexRelationTypesComplexRelationTypeId,
        PathValues.DOMAIN_TYPES: DomainTypes,
        PathValues.DOMAIN_TYPES_BULK: DomainTypesBulk,
        PathValues.DOMAIN_TYPES_DOMAIN_TYPE_ID: DomainTypesDomainTypeId,
        PathValues.DOMAIN_TYPES_DOMAIN_TYPE_ID_SUB_TYPES: DomainTypesDomainTypeIdSubTypes,
        PathValues.RELATION_TYPES: RelationTypes,
        PathValues.RELATION_TYPES_BULK: RelationTypesBulk,
        PathValues.RELATION_TYPES_RELATION_TYPE_ID: RelationTypesRelationTypeId,
        PathValues.STATUSES: Statuses,
        PathValues.STATUSES_BULK: StatusesBulk,
        PathValues.STATUSES_STATUS_ID: StatusesStatusId,
        PathValues.STATUSES_NAME_STATUS_NAME: StatusesNameStatusName,
        PathValues.NAVIGATION_MOST_VIEWED: NavigationMostViewed,
        PathValues.NAVIGATION_RECENTLY_VIEWED: NavigationRecentlyViewed,
        PathValues.DATA_QUALITY_RULES: DataQualityRules,
        PathValues.DATA_QUALITY_RULES_DATA_QUALITY_RULE_ID: DataQualityRulesDataQualityRuleId,
        PathValues.OUTPUT_MODULE_EXPORT_CSV: OutputModuleExportCsv,
        PathValues.OUTPUT_MODULE_EXPORT_CSVJOB: OutputModuleExportCsvJob,
        PathValues.OUTPUT_MODULE_EXPORT_CSVFILE: OutputModuleExportCsvFile,
        PathValues.OUTPUT_MODULE_EXPORT_EXCELJOB: OutputModuleExportExcelJob,
        PathValues.OUTPUT_MODULE_EXPORT_EXCELFILE: OutputModuleExportExcelFile,
        PathValues.OUTPUT_MODULE_EXPORT_JSON: OutputModuleExportJson,
        PathValues.OUTPUT_MODULE_EXPORT_JSONJOB: OutputModuleExportJsonJob,
        PathValues.OUTPUT_MODULE_EXPORT_JSONFILE: OutputModuleExportJsonFile,
        PathValues.OUTPUT_MODULE_EXPORT_XML: OutputModuleExportXml,
        PathValues.OUTPUT_MODULE_EXPORT_XMLJOB: OutputModuleExportXmlJob,
        PathValues.OUTPUT_MODULE_EXPORT_XMLFILE: OutputModuleExportXmlFile,
        PathValues.OUTPUT_MODULE_TABLE_VIEW_CONFIGS_VIEW_ID_VIEW_ID: OutputModuleTableViewConfigsViewIdViewId,
        PathValues.REPORTING_INSIGHTS_DOWNLOAD: ReportingInsightsDownload,
        PathValues.ROLES: Roles,
        PathValues.ROLES_ROLE_ID: RolesRoleId,
        PathValues.SECURITY_SAML_CERTIFICATE_TYPE: SecuritySamlCertificateType,
        PathValues.SECURITY_SAML: SecuritySaml,
        PathValues.AUTH_SESSIONS_CURRENT: AuthSessionsCurrent,
        PathValues.AUTH_SESSIONS_HEARTBEAT: AuthSessionsHeartbeat,
        PathValues.AUTH_SESSIONS: AuthSessions,
        PathValues.USERS: Users,
        PathValues.USERS_USER_ID_USER_GROUPS: UsersUserIdUserGroups,
        PathValues.USERS_BULK: UsersBulk,
        PathValues.USERS_USER_ID: UsersUserId,
        PathValues.USERS_USER_ID_AVATAR: UsersUserIdAvatar,
        PathValues.USERS_CURRENT: UsersCurrent,
        PathValues.USERS_CURRENT_PERMISSIONS: UsersCurrentPermissions,
        PathValues.USERS_EMAIL_EMAIL_ADDRESS: UsersEmailEmailAddress,
        PathValues.USERS_USER_ID_LICENSE_TYPE: UsersUserIdLicenseType,
        PathValues.USER_GROUPS: UserGroups,
        PathValues.USER_GROUPS_USER_GROUP_ID_USERS: UserGroupsUserGroupIdUsers,
        PathValues.USER_GROUPS_USER_GROUP_ID: UserGroupsUserGroupId,
        PathValues.VALIDATION: Validation,
        PathValues.VALIDATION_ASSET_ID: ValidationAssetId,
        PathValues.VALIDATION_BULK: ValidationBulk,
        PathValues.VIEW_PERMISSIONS: ViewPermissions,
        PathValues.VIEW_PERMISSIONS_VIEW_PERMISSION_ID: ViewPermissionsViewPermissionId,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_ASSET_TYPE_ASSIGNMENT_RULES: WorkflowDefinitionsWorkflowDefinitionIdAssetTypeAssignmentRules,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_DOMAIN_TYPE_ASSIGNMENT_RULES: WorkflowDefinitionsWorkflowDefinitionIdDomainTypeAssignmentRules,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_ASSET_TYPE_ASSIGNMENT_RULES_RULE_ID: WorkflowDefinitionsWorkflowDefinitionIdAssetTypeAssignmentRulesRuleId,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_DOMAIN_TYPE_ASSIGNMENT_RULES_RULE_ID: WorkflowDefinitionsWorkflowDefinitionIdDomainTypeAssignmentRulesRuleId,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID: WorkflowDefinitionsWorkflowDefinitionId,
        PathValues.WORKFLOW_DEFINITIONS: WorkflowDefinitions,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_WORKFLOW_DEFINITION_ID_CONFIGURATION_START_FORM_DATA: WorkflowDefinitionsWorkflowDefinitionWorkflowDefinitionIdConfigurationStartFormData,
        PathValues.WORKFLOW_DEFINITIONS_START_EVENTS: WorkflowDefinitionsStartEvents,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_WORKFLOW_DEFINITION_ID_START_FORM_DATA: WorkflowDefinitionsWorkflowDefinitionWorkflowDefinitionIdStartFormData,
        PathValues.WORKFLOW_DEFINITIONS_PROCESS_PROCESS_ID: WorkflowDefinitionsProcessProcessId,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_DIAGRAM: WorkflowDefinitionsWorkflowDefinitionIdDiagram,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_XML: WorkflowDefinitionsWorkflowDefinitionIdXml,
        PathValues.WORKFLOW_DEFINITIONS_WORKFLOW_DEFINITION_ID_ASSIGNMENT_RULES_RULE_ID: WorkflowDefinitionsWorkflowDefinitionIdAssignmentRulesRuleId,
        PathValues.WORKFLOW_DEFINITIONS_REMOVAL_JOBS: WorkflowDefinitionsRemovalJobs,
        PathValues.WORKFLOW_INSTANCES_WORKFLOW_INSTANCE_ID_CANCELED: WorkflowInstancesWorkflowInstanceIdCanceled,
        PathValues.WORKFLOW_INSTANCES: WorkflowInstances,
        PathValues.WORKFLOW_INSTANCES_WORKFLOW_INSTANCE_ID_DIAGRAM: WorkflowInstancesWorkflowInstanceIdDiagram,
        PathValues.WORKFLOW_INSTANCES_PROCESS_INSTANCE_ID_MESSAGE_EVENTS_MESSAGE_NAME: WorkflowInstancesProcessInstanceIdMessageEventsMessageName,
        PathValues.WORKFLOW_INSTANCES_START_JOBS: WorkflowInstancesStartJobs,
        PathValues.WORKFLOW_TASKS_WORKFLOW_TASK_ID_CANCELED: WorkflowTasksWorkflowTaskIdCanceled,
        PathValues.WORKFLOW_TASKS_COMPLETED: WorkflowTasksCompleted,
        PathValues.WORKFLOW_TASKS: WorkflowTasks,
        PathValues.WORKFLOW_TASKS_WORKFLOW_TASK_ID_TASK_FORM_DATA: WorkflowTasksWorkflowTaskIdTaskFormData,
        PathValues.WORKFLOW_TASKS_WORKFLOW_TASK_ID: WorkflowTasksWorkflowTaskId,
        PathValues.WORKFLOW_TASKS_WORKFLOW_TASK_ID_REASSIGN: WorkflowTasksWorkflowTaskIdReassign,
    }
)
