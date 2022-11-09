import typing_extensions

from collibra_core.apis.tags import TagValues
from collibra_core.apis.tags.activities_api import ActivitiesApi
from collibra_core.apis.tags.application_api import ApplicationApi
from collibra_core.apis.tags.asset_types_api import AssetTypesApi
from collibra_core.apis.tags.assets_api import AssetsApi
from collibra_core.apis.tags.assignments_api import AssignmentsApi
from collibra_core.apis.tags.attachments_api import AttachmentsApi
from collibra_core.apis.tags.attribute_types_api import AttributeTypesApi
from collibra_core.apis.tags.attributes_api import AttributesApi
from collibra_core.apis.tags.authentication_sessions_api import AuthenticationSessionsApi
from collibra_core.apis.tags.comments_api import CommentsApi
from collibra_core.apis.tags.communities_api import CommunitiesApi
from collibra_core.apis.tags.complex_relation_types_api import ComplexRelationTypesApi
from collibra_core.apis.tags.complex_relations_api import ComplexRelationsApi
from collibra_core.apis.tags.data_quality_rules_api import DataQualityRulesApi
from collibra_core.apis.tags.diagram_pictures_api import DiagramPicturesApi
from collibra_core.apis.tags.domain_types_api import DomainTypesApi
from collibra_core.apis.tags.domains_api import DomainsApi
from collibra_core.apis.tags.files_api import FilesApi
from collibra_core.apis.tags.issues_api import IssuesApi
from collibra_core.apis.tags.jdbc_driver_api import JDBCDriverApi
from collibra_core.apis.tags.jobs_api import JobsApi
from collibra_core.apis.tags.mappings_api import MappingsApi
from collibra_core.apis.tags.navigation_statistics_api import NavigationStatisticsApi
from collibra_core.apis.tags.output_module_api import OutputModuleApi
from collibra_core.apis.tags.ratings_api import RatingsApi
from collibra_core.apis.tags.relation_types_api import RelationTypesApi
from collibra_core.apis.tags.relations_api import RelationsApi
from collibra_core.apis.tags.reporting_api import ReportingApi
from collibra_core.apis.tags.responsibilities_api import ResponsibilitiesApi
from collibra_core.apis.tags.roles_api import RolesApi
from collibra_core.apis.tags.saml_api import SAMLApi
from collibra_core.apis.tags.scopes_api import ScopesApi
from collibra_core.apis.tags.statuses_api import StatusesApi
from collibra_core.apis.tags.tags_api import TagsApi
from collibra_core.apis.tags.user_groups_api import UserGroupsApi
from collibra_core.apis.tags.users_api import UsersApi
from collibra_core.apis.tags.validation_api import ValidationApi
from collibra_core.apis.tags.view_permissions_api import ViewPermissionsApi
from collibra_core.apis.tags.workflow_definitions_api import WorkflowDefinitionsApi
from collibra_core.apis.tags.workflow_instances_api import WorkflowInstancesApi
from collibra_core.apis.tags.workflow_tasks_api import WorkflowTasksApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ACTIVITIES: ActivitiesApi,
        TagValues.APPLICATION: ApplicationApi,
        TagValues.ASSET_TYPES: AssetTypesApi,
        TagValues.ASSETS: AssetsApi,
        TagValues.ASSIGNMENTS: AssignmentsApi,
        TagValues.ATTACHMENTS: AttachmentsApi,
        TagValues.ATTRIBUTE_TYPES: AttributeTypesApi,
        TagValues.ATTRIBUTES: AttributesApi,
        TagValues.AUTHENTICATION_SESSIONS: AuthenticationSessionsApi,
        TagValues.COMMENTS: CommentsApi,
        TagValues.COMMUNITIES: CommunitiesApi,
        TagValues.COMPLEX_RELATION_TYPES: ComplexRelationTypesApi,
        TagValues.COMPLEX_RELATIONS: ComplexRelationsApi,
        TagValues.DATA_QUALITY_RULES: DataQualityRulesApi,
        TagValues.DIAGRAM_PICTURES: DiagramPicturesApi,
        TagValues.DOMAIN_TYPES: DomainTypesApi,
        TagValues.DOMAINS: DomainsApi,
        TagValues.FILES: FilesApi,
        TagValues.ISSUES: IssuesApi,
        TagValues.JDBC_DRIVER: JDBCDriverApi,
        TagValues.JOBS: JobsApi,
        TagValues.MAPPINGS: MappingsApi,
        TagValues.NAVIGATION_STATISTICS: NavigationStatisticsApi,
        TagValues.OUTPUT_MODULE: OutputModuleApi,
        TagValues.RATINGS: RatingsApi,
        TagValues.RELATION_TYPES: RelationTypesApi,
        TagValues.RELATIONS: RelationsApi,
        TagValues.REPORTING: ReportingApi,
        TagValues.RESPONSIBILITIES: ResponsibilitiesApi,
        TagValues.ROLES: RolesApi,
        TagValues.SAML: SAMLApi,
        TagValues.SCOPES: ScopesApi,
        TagValues.STATUSES: StatusesApi,
        TagValues.TAGS: TagsApi,
        TagValues.USER_GROUPS: UserGroupsApi,
        TagValues.USERS: UsersApi,
        TagValues.VALIDATION: ValidationApi,
        TagValues.VIEW_PERMISSIONS: ViewPermissionsApi,
        TagValues.WORKFLOW_DEFINITIONS: WorkflowDefinitionsApi,
        TagValues.WORKFLOW_INSTANCES: WorkflowInstancesApi,
        TagValues.WORKFLOW_TASKS: WorkflowTasksApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ACTIVITIES: ActivitiesApi,
        TagValues.APPLICATION: ApplicationApi,
        TagValues.ASSET_TYPES: AssetTypesApi,
        TagValues.ASSETS: AssetsApi,
        TagValues.ASSIGNMENTS: AssignmentsApi,
        TagValues.ATTACHMENTS: AttachmentsApi,
        TagValues.ATTRIBUTE_TYPES: AttributeTypesApi,
        TagValues.ATTRIBUTES: AttributesApi,
        TagValues.AUTHENTICATION_SESSIONS: AuthenticationSessionsApi,
        TagValues.COMMENTS: CommentsApi,
        TagValues.COMMUNITIES: CommunitiesApi,
        TagValues.COMPLEX_RELATION_TYPES: ComplexRelationTypesApi,
        TagValues.COMPLEX_RELATIONS: ComplexRelationsApi,
        TagValues.DATA_QUALITY_RULES: DataQualityRulesApi,
        TagValues.DIAGRAM_PICTURES: DiagramPicturesApi,
        TagValues.DOMAIN_TYPES: DomainTypesApi,
        TagValues.DOMAINS: DomainsApi,
        TagValues.FILES: FilesApi,
        TagValues.ISSUES: IssuesApi,
        TagValues.JDBC_DRIVER: JDBCDriverApi,
        TagValues.JOBS: JobsApi,
        TagValues.MAPPINGS: MappingsApi,
        TagValues.NAVIGATION_STATISTICS: NavigationStatisticsApi,
        TagValues.OUTPUT_MODULE: OutputModuleApi,
        TagValues.RATINGS: RatingsApi,
        TagValues.RELATION_TYPES: RelationTypesApi,
        TagValues.RELATIONS: RelationsApi,
        TagValues.REPORTING: ReportingApi,
        TagValues.RESPONSIBILITIES: ResponsibilitiesApi,
        TagValues.ROLES: RolesApi,
        TagValues.SAML: SAMLApi,
        TagValues.SCOPES: ScopesApi,
        TagValues.STATUSES: StatusesApi,
        TagValues.TAGS: TagsApi,
        TagValues.USER_GROUPS: UserGroupsApi,
        TagValues.USERS: UsersApi,
        TagValues.VALIDATION: ValidationApi,
        TagValues.VIEW_PERMISSIONS: ViewPermissionsApi,
        TagValues.WORKFLOW_DEFINITIONS: WorkflowDefinitionsApi,
        TagValues.WORKFLOW_INSTANCES: WorkflowInstancesApi,
        TagValues.WORKFLOW_TASKS: WorkflowTasksApi,
    }
)
