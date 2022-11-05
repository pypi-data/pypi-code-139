from __future__ import annotations

from datetime import date, datetime
import json
import random
import string
from typing import Dict, List, Optional, Type, TypeVar, Union

from benchling_api_client.v2.beta.models.base_manifest_config import BaseManifestConfig
from benchling_api_client.v2.beta.models.benchling_app_manifest import BenchlingAppManifest
from benchling_api_client.v2.beta.models.dropdown_dependency import DropdownDependency
from benchling_api_client.v2.beta.models.entity_schema_dependency import EntitySchemaDependency
from benchling_api_client.v2.beta.models.manifest_scalar_config import ManifestScalarConfig
from benchling_api_client.v2.beta.models.resource_dependency import ResourceDependency
from benchling_api_client.v2.beta.models.scalar_config_types import ScalarConfigTypes
from benchling_api_client.v2.beta.models.schema_dependency import SchemaDependency
from benchling_api_client.v2.beta.models.workflow_task_schema_dependency import WorkflowTaskSchemaDependency
from benchling_api_client.v2.extensions import UnknownType
from benchling_api_client.v2.stable.types import UNSET
from typing_extensions import Protocol

from benchling_sdk.apps.config.decryption_provider import BaseDecryptionProvider
from benchling_sdk.apps.config.dependencies import (
    _supported_config_item,
    BaseDependencies,
    ConfigurationReference,
    DependencyLinkStore,
    StaticConfigProvider,
)
from benchling_sdk.apps.config.scalars import DateTimeScalar, JsonType
from benchling_sdk.apps.helpers.config_helpers import (
    field_definitions_from_dependency,
    options_from_dependency,
    subtype_from_entity_schema_dependency,
    workflow_task_schema_output_from_dependency,
)
from benchling_sdk.models import (
    AppConfigItem,
    BooleanAppConfigItem,
    BooleanAppConfigItemType,
    DateAppConfigItem,
    DateAppConfigItemType,
    DatetimeAppConfigItem,
    DatetimeAppConfigItemType,
    EntitySchemaAppConfigItem,
    FieldAppConfigItem,
    FieldAppConfigItemType,
    FloatAppConfigItem,
    FloatAppConfigItemType,
    GenericApiIdentifiedAppConfigItem,
    GenericApiIdentifiedAppConfigItemType,
    IntegerAppConfigItem,
    IntegerAppConfigItemType,
    JsonAppConfigItem,
    JsonAppConfigItemType,
    LinkedAppConfigResourceSummary,
    SecureTextAppConfigItem,
    SecureTextAppConfigItemType,
    TextAppConfigItem,
    TextAppConfigItemType,
)

ManifestDependencies = Union[
    DropdownDependency,
    EntitySchemaDependency,
    ManifestScalarConfig,
    ResourceDependency,
    SchemaDependency,
    WorkflowTaskSchemaDependency,
    UnknownType,
]

D = TypeVar("D", bound=BaseDependencies)


class MockDecryptionFunction(Protocol):
    """Mock out a decryption function for use with secure text."""

    def __call__(self, ciphertext: str) -> str:
        """Return a string representing plaintext given input ciphertext."""


class MockDecryptionProvider(BaseDecryptionProvider):
    """
    Mock Decryption Provider.

    A generic class mocking a BaseDecryptionProvider. Can be passed a function to mock arbitrary decryption.

    It's recommended to extend this class or use a specific implementation instead of initializing an instance.
    """

    _mock_decryption_function: MockDecryptionFunction

    def __init__(self, mock_decryption_function: MockDecryptionFunction):
        """
        Init Mock Decryption Provider.

        Pass a function that returns desired mocked plaintext given ciphertext.
        """
        self._mock_decryption_function = mock_decryption_function

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt.

        Invokes the mocked decryption function provided when instantiating the class to return a "decrypted" value.
        """
        return self._mock_decryption_function(ciphertext)


class MockBenchlingAppConfig:
    """
    Mock App Config.

    A helper class for easily mocking app config in various permutations.

    Easily mock all config items from a manifest model (which can be loaded from
    `benchling_sdk.apps.helpers.manifest_helpers.manifest_from_file()`.
    """

    _config_items: List[AppConfigItem]
    _decryption_provider: Optional[MockDecryptionProvider]

    def __init__(
        self, config_items: List[AppConfigItem], decryption_provider: Optional[MockDecryptionProvider]
    ):
        """
        Init Mock Benchling App Config.

        The class can be initialized by providing a list of AppConfigItem, but the recommended
        usage is to mock directly from a manifest, like `MockBenchlingAppConfig.from_manifest()`
        """
        self._config_items = config_items
        self._decryption_provider = decryption_provider

    @classmethod
    def from_manifest(
        cls, manifest: BenchlingAppManifest, decryption_provider: Optional[MockDecryptionProvider] = None
    ) -> MockBenchlingAppConfig:
        """
        From Manifest.

        Reads a manifest amd mocks out all dependencies.
        """
        config_items = mock_app_config_items_from_manifest(manifest)
        return cls(config_items, decryption_provider)

    def to_dependencies(self, target_dependencies: Type[D]) -> D:
        """
        To Dependencies.

        Convenience method for providing mocked app config to a target class extending BaseDependencies.
        """
        link_store = DependencyLinkStore(StaticConfigProvider(self.config_items))
        return target_dependencies.from_store(link_store, decryption_provider=self._decryption_provider)

    def with_replacement(self, replacement: ConfigurationReference) -> MockBenchlingAppConfig:
        """
        With Replacement.

        Returns a new MockBenchlingAppConfig with the app config item at the specified path replaced.
        """
        replaced_app_config = replace_mocked_config_item_by_path(
            self.config_items, replacement.path, replacement
        )
        return MockBenchlingAppConfig(replaced_app_config, self._decryption_provider)

    def with_replacements(self, replacements: List[ConfigurationReference]) -> MockBenchlingAppConfig:
        """
        With Replacement.

        Returns a new MockBenchlingAppConfig with the app config item at the specified path replaced.
        """
        replaced_app_config = self.config_items
        for replacement in replacements:
            replaced_app_config = replace_mocked_config_item_by_path(
                replaced_app_config, replacement.path, replacement
            )
        return MockBenchlingAppConfig(replaced_app_config, self._decryption_provider)

    @property
    def config_items(self) -> List[ConfigurationReference]:
        """List the config items in the mock app config, excluding any unknown types."""
        return [_supported_config_item(config_item) for config_item in self._config_items]

    @property
    def config_items_with_unknown(self) -> List[AppConfigItem]:
        """List the config items in the mock app config, including any unknown types."""
        return self._config_items


class MockDecryptionProviderStatic(MockDecryptionProvider):
    """
    Mock Decryption Provider Static.

    Always return the same "decrypted" value regardless of what ciphertext is passed.
    Useful if you only have a single secret value.
    """

    def __init__(self, decrypt_value: str):
        """
        Init Mock Decryption Provider Static.

        Supply the string to always be returned.
        """

        def decrypt(ciphertext: str) -> str:
            return decrypt_value

        super().__init__(decrypt)


class MockDecryptionProviderMapped(MockDecryptionProvider):
    """
    Mock Decryption Provider Mapped.

    Returns a "decrypted" value based on the input ciphertext.
    Useful if you have multiple secrets to mock simultaneously.
    """

    def __init__(self, decrypt_mapping: Dict[str, str]):
        """
        Init Mock Decryption Provider Mapped.

        Supply the dictionary mapping with ciphertext as keys and plaintext as values.
        Any ciphertext decrypted without a corresponding value will result in a KeyError.
        """

        def decrypt(ciphertext: str) -> str:
            return decrypt_mapping[ciphertext]

        super().__init__(decrypt)


def mock_app_config_items_from_manifest(manifest: BenchlingAppManifest) -> List[AppConfigItem]:
    """
    Mock Benchling App Config Items.

    This method accepts an app manifest model and creates mocked values for app the app config.

    The concrete mocked out values, such as API Ids and schema names are nonsensical and random,
    but are valid.

    Code should avoid relying on specific values or conventions (such as API prefixes). If
    specific dependency values need to be tested in isolation, the caller can selectively
    override the randomized values with replace_mocked_config_item_by_path().
    """
    root_config_items = [_mock_dependency(dependency) for dependency in manifest.configuration]
    return [config_item for sub_config_items in root_config_items for config_item in sub_config_items]


def replace_mocked_config_item_by_path(
    original_config: List[AppConfigItem], replacement_path: List[str], replacement_item: AppConfigItem
) -> List[AppConfigItem]:
    """Return an updated list of app config items with a specific config item replaced with the provided mock."""
    replaced_config = [config for config in original_config if config.path != replacement_path]
    replaced_config.append(replacement_item)
    return replaced_config


def mock_bool_app_config_item(path: List[str], value: Optional[bool]) -> BooleanAppConfigItem:
    """Mock a bool app config item with a path and specified value."""
    return BooleanAppConfigItem(
        path=path,
        value=value,
        type=BooleanAppConfigItemType.BOOLEAN,
        id=_random_string("aci_"),
    )


def mock_date_app_config_item(path: List[str], value: Optional[date]) -> DateAppConfigItem:
    """Mock a date app config item with a path and specified value."""
    return DateAppConfigItem(
        path=path,
        value=value,
        type=DateAppConfigItemType.DATE,
        id=_random_string("aci_"),
    )


def mock_datetime_app_config_item(path: List[str], value: Optional[datetime]) -> DatetimeAppConfigItem:
    """Mock a datetime app config item with a path and specified value."""
    return DatetimeAppConfigItem(
        path=path,
        value=value.strftime(DateTimeScalar.expected_format()) if isinstance(value, datetime) else value,
        type=DatetimeAppConfigItemType.DATETIME,
        id=_random_string("aci_"),
    )


def mock_float_app_config_item(path: List[str], value: Optional[float]) -> FloatAppConfigItem:
    """Mock a float app config item with a path and specified value."""
    return FloatAppConfigItem(
        path=path,
        value=value,
        type=FloatAppConfigItemType.FLOAT,
        id=_random_string("aci_"),
    )


def mock_int_app_config_item(path: List[str], value: Optional[int]) -> IntegerAppConfigItem:
    """Mock an int app config item with a path and specified value."""
    return IntegerAppConfigItem(
        path=path,
        value=value,
        type=IntegerAppConfigItemType.INTEGER,
        id=_random_string("aci_"),
    )


def mock_json_app_config_item(path: List[str], value: Optional[JsonType]) -> JsonAppConfigItem:
    """Mock an int app config item with a path and specified value."""
    return JsonAppConfigItem(
        path=path,
        value=json.dumps(value) if value is not None else None,
        type=JsonAppConfigItemType.JSON,
        id=_random_string("aci_"),
    )


def mock_secure_text_app_config_item(path: List[str], value: Optional[str]) -> SecureTextAppConfigItem:
    """Mock a secure text app config item with a path and specified value."""
    return SecureTextAppConfigItem(
        path=path,
        value=value,
        type=SecureTextAppConfigItemType.SECURE_TEXT,
        id=_random_string("aci_"),
    )


def mock_text_app_config_item(path: List[str], value: Optional[str]) -> TextAppConfigItem:
    """Mock a text app config item with a path and specified value."""
    return TextAppConfigItem(
        path=path,
        value=value,
        type=TextAppConfigItemType.TEXT,
        id=_random_string("aci_"),
    )


def _mock_dependency(
    dependency: ManifestDependencies,
) -> List[AppConfigItem]:
    """Mock a dependency from its manifest definition."""
    if isinstance(dependency, DropdownDependency):
        linked_resource_id = _random_string("val_")
        config_item = GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=[dependency.name],
            type=GenericApiIdentifiedAppConfigItemType.DROPDOWN,
            value=_random_string("val_"),
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency)
            for subdependency in options_from_dependency(dependency)
        ]
        return [config_item] + sub_items
    elif isinstance(dependency, EntitySchemaDependency):
        linked_resource_id = _random_string("val_")
        subtype = subtype_from_entity_schema_dependency(dependency)
        optional_subtype = subtype if subtype else UNSET
        config_item = EntitySchemaAppConfigItem(
            id=_random_string("aci_"),
            path=[dependency.name],
            type=optional_subtype,
            value=_random_string("val_"),
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency)
            for subdependency in field_definitions_from_dependency(dependency)
        ]
        return [config_item] + sub_items
    elif isinstance(dependency, SchemaDependency):
        linked_resource_id = _random_string("val_")
        config_item = GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=[dependency.name],
            type=GenericApiIdentifiedAppConfigItemType(dependency.type),
            value=_random_string("val_"),
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency)
            for subdependency in field_definitions_from_dependency(dependency)
        ]
        return [config_item] + sub_items
    elif isinstance(dependency, WorkflowTaskSchemaDependency):
        linked_resource_id = _random_string("val_")
        config_item = GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=[dependency.name],
            type=GenericApiIdentifiedAppConfigItemType.WORKFLOW_TASK_SCHEMA,
            value=linked_resource_id,
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency)
            for subdependency in field_definitions_from_dependency(dependency)
        ]
        workflow_task_output = workflow_task_schema_output_from_dependency(dependency)
        if workflow_task_output:
            output_fields = field_definitions_from_dependency(workflow_task_output)
            output_items = [
                _mock_workflow_output_subdependency(subdependency, dependency)
                for subdependency in output_fields
            ]
            sub_items += output_items
        return [config_item] + sub_items
    elif isinstance(dependency, ManifestScalarConfig):
        return [_mock_scalar_dependency(dependency)]
    elif isinstance(dependency, UnknownType):
        return UnknownType(value="Unknown")
    else:
        linked_resource_id = _random_string("val_")
        return [
            GenericApiIdentifiedAppConfigItem(
                id=_random_string("aci_"),
                path=[dependency.name],
                type=GenericApiIdentifiedAppConfigItemType(dependency.type),
                value=linked_resource_id,
                linked_resource=_mock_linked_resource(linked_resource_id),
            )
        ]


def _mock_scalar_dependency(dependency: ManifestScalarConfig) -> AppConfigItem:
    if dependency.type == ScalarConfigTypes.BOOLEAN:
        return mock_bool_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    elif dependency.type == ScalarConfigTypes.DATE:
        return mock_date_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    elif dependency.type == ScalarConfigTypes.DATETIME:
        return mock_datetime_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    elif dependency.type == ScalarConfigTypes.FLOAT:
        return mock_float_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    elif dependency.type == ScalarConfigTypes.INTEGER:
        return mock_int_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    elif dependency.type == ScalarConfigTypes.JSON:
        # _mock_scalar_value returns str so convert back to JSON
        json_value = json.loads(_mock_scalar_value(dependency.type))
        return mock_json_app_config_item([dependency.name], json_value)
    elif dependency.type == ScalarConfigTypes.SECURE_TEXT:
        return mock_secure_text_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    else:
        return mock_text_app_config_item([dependency.name], _mock_scalar_value(dependency.type))


def _mock_subdependency(subdependency: BaseManifestConfig, parent_config) -> AppConfigItem:
    if isinstance(parent_config, DropdownDependency):
        linked_resource_id = _random_string("opt_")
        return GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=[parent_config.name, subdependency.name],
            type=GenericApiIdentifiedAppConfigItemType.DROPDOWN_OPTION,
            value=linked_resource_id,
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
    elif isinstance(parent_config, (EntitySchemaDependency, SchemaDependency, WorkflowTaskSchemaDependency)):
        path = [parent_config.name, subdependency.name]
        linked_resource_id = _random_string("tsf_")
        app_config = FieldAppConfigItem(
            id=_random_string("aci_"),
            path=path,
            type=FieldAppConfigItemType.FIELD,
            value=linked_resource_id,
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        return app_config


def _mock_workflow_output_subdependency(subdependency: BaseManifestConfig, parent_config) -> AppConfigItem:
    linked_resource_id = _random_string("tsf_")
    app_config = FieldAppConfigItem(
        id=_random_string("aci_"),
        path=[parent_config.name, "output", subdependency.name],
        type=FieldAppConfigItemType.FIELD,
        value=linked_resource_id,
        linked_resource=_mock_linked_resource(linked_resource_id),
    )
    return app_config


def _mock_linked_resource(id: str, name: Optional[str] = None) -> LinkedAppConfigResourceSummary:
    return LinkedAppConfigResourceSummary(id=id, name=name if name else _random_string("Resource Name"))


def _mock_scalar_value(scalar_type: ScalarConfigTypes) -> Optional[str]:
    """Mock a scalar config value from its manifest definition."""
    if scalar_type == scalar_type.BOOLEAN:
        return "true"
    elif scalar_type == scalar_type.DATE:
        return date.today().strftime("%Y-%m-%d")
    elif scalar_type == scalar_type.DATETIME:
        return datetime.now().strftime(DateTimeScalar.expected_format())
    elif scalar_type == scalar_type.FLOAT:
        return str(random.random())
    elif scalar_type == scalar_type.INTEGER:
        return str(random.randint(-1000, 1000))
    elif scalar_type == scalar_type.JSON:
        return json.dumps(
            {_random_string(): [_random_string(), _random_string()], _random_string(): random.random()}
        )
    return _random_string()


def _random_string(prefix: str = "", random_length: int = 20) -> str:
    """Generate a randomized string up to a specified length with an optional prefix."""
    delimited_prefix = f"{prefix}-" if prefix else ""
    return f"{delimited_prefix}{''.join(random.choice(string.ascii_letters) for i in range(random_length))}"
