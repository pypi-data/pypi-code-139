"""
Autogenerated using `pop-create-idem <https://gitlab.com/saltstack/pop/pop-create-idem>`__

hub.exec.boto3.client.iam.create_role
hub.exec.boto3.client.iam.delete_role
hub.exec.boto3.client.iam.get_role
hub.exec.boto3.client.iam.list_roles
hub.exec.boto3.client.iam.tag_role
hub.exec.boto3.client.iam.untag_role
hub.exec.boto3.client.iam.update_role
resource = await hub.tool.boto3.resource.create(ctx, "iam", "Role", name)
hub.tool.boto3.resource.exec(resource, attach_policy, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, delete, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, detach_policy, *args, **kwargs)
"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]
TREQ = {
    "absent": {
        "require": ["aws.iam.role_policy.absent"],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    assume_role_policy_document: Dict or str,
    resource_id: str = None,
    description: str = None,
    max_session_duration: int = None,
    permissions_boundary: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=0)),
                        ("max_attempts", int, field(default=0)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=0)),
                        ("max_attempts", int, field(default=0)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    r"""
    **Autogenerated function**

    Creates a new role for your Amazon Web Services account. For more information about roles, see IAM roles. For
    information about quotas for role names and the number of roles you can create, see IAM and STS quotas in the
    IAM User Guide.

    Args:
        name(Text): The name of the IAM role.
        assume_role_policy_document(Dict or Text): The trust relationship policy document that grants an entity
         permission to assume the role. This can be either a dictionary or a json string.
        resource_id(Text, Optional): AWS IAM Role Name.
        description(Text, Optional): A description of the role. Defaults to None.
        max_session_duration(Integer, Optional): The maximum session duration (in seconds) that you want to set for the
         specified role. If you do not specify a value for this setting, the default maximum of one hour is applied.
          This setting can have a value from 1 hour to 12 hours.
        permissions_boundary(Text, Optional): The ARN of the policy that is used to set the permissions boundary for the role.
        tags(Dict or List, optional): Dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the new role.
            Each tag consists of a key name and an associated value. Defaults to None.
            * (Key): The key name that can be used to look up or retrieve the associated value. For example,
                Department or Cost Center are common choices.
            * (Value): The value associated with this tag. For example, tags with a key name of Department could have
                values such as Human Resources, Accounting, and Support. Tags with a key name of Cost Center
                might have values that consist of the number associated with the different cost centers in your
                company. Typically, many resources have tags with the same key name but with different values.
                Amazon Web Services always interprets the tag Value as a single string. If you need to store an
                array, you can store comma-separated values in the string. However, you must interpret the value
                in your code.
        timeout(Dict, optional): Timeout configuration for create/update/deletion of AWS IAM Policy.
            * create (Dict): Timeout configuration for creating AWS IAM Policy
                * delay (int, Optional): The amount of time in seconds to wait between attempts.
                * max_attempts (int, Optional): Customized timeout configuration containing delay and max attempts.
            * update(Dict, optional): Timeout configuration for updating AWS IAM Policy
                * delay (int, Optional): The amount of time in seconds to wait between attempts.
                * max_attempts: (int, Optional) Customized timeout configuration containing delay and max attempts.
    Request Syntax:
        [iam-role-name]:
          aws.iam.role.present:
          - name: 'string'
          - resource_id: 'string'
          - assume_role_policy_document: 'dict or string'
          - description: 'string'
          - max_session_duration: 'integer'
          - permissions_boundary: 'string'
          - tags:
            - Key: 'string'
              Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            AWSServiceRoleForEC2Spot:
              aws.iam.role.present:
                - assume_role_policy_document:
                  Statement:
                    - Action: sts:AssumeRole
                      Effect: Allow
                      Principal:
                        Service: spot.amazonaws.com
                  Version: '2012-10-17'
                - description: Default EC2 Spot Service Linked Role
                - max_session_duration: 3600
                - tags:
                  - Key: tag-key
                    Value: tag-value
    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    resource_updated = False

    # Standardise on the json format of policy
    assume_role_policy_document = hub.tool.aws.state_comparison_utils.standardise_json(
        assume_role_policy_document
    )
    before = None
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
    if resource_id:
        before = await hub.exec.aws.iam.role.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = copy.deepcopy(before["ret"])
        try:
            plan_state = copy.deepcopy(result["old_state"])
            # Update role
            update_ret = await hub.exec.aws.iam.role.update_role(
                ctx,
                old_state=result["old_state"],
                description=description,
                max_session_duration=max_session_duration,
                timeout=timeout,
            )
            result["comment"] = result["comment"] + update_ret["comment"]
            result["result"] = update_ret["result"]
            resource_updated = resource_updated or bool(update_ret["ret"])
            if update_ret["ret"] and ctx.get("test", False):
                if "max_session_duration" in update_ret["ret"]:
                    plan_state["max_session_duration"] = update_ret["ret"][
                        "max_session_duration"
                    ]
                if "description" in update_ret["ret"]:
                    plan_state["description"] = update_ret["ret"]["description"]

            # Update tags
            if (tags is not None) and tags != result["old_state"].get("tags"):
                update_ret = await hub.exec.aws.iam.role.update_role_tags(
                    ctx,
                    role_name=result["old_state"]["name"],
                    old_tags=result["old_state"].get("tags", []),
                    new_tags=tags,
                )
                result["result"] = result["result"] and update_ret["result"]
                result["comment"] = result["comment"] + update_ret["comment"]
                resource_updated = resource_updated or bool(update_ret["result"])
                if ctx.get("test", False) and update_ret["ret"] is not None:
                    plan_state["tags"] = update_ret["ret"]
            if not resource_updated:
                result["comment"] = result["comment"] + (
                    f"aws.iam.role '{name}' already exists",
                )
            # Update policy which is embedded within the role
            if not hub.tool.aws.state_comparison_utils.is_json_identical(
                result["old_state"]["assume_role_policy_document"],
                assume_role_policy_document,
            ):
                update_ret = await hub.exec.aws.iam.role.update_policy(
                    ctx,
                    role_name=result["old_state"]["resource_id"],
                    policy=assume_role_policy_document,
                )
                result["result"] = result["result"] and update_ret["result"]
                result["comment"] = result["comment"] + update_ret["comment"]
                resource_updated = resource_updated or bool(update_ret["ret"])
                if ctx.get("test", False):
                    plan_state[
                        "assume_role_policy_document"
                    ] = assume_role_policy_document

        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)
            result["result"] = False
    else:
        try:
            if ctx.get("test", False):
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "arn": f"role-{name}-arn",
                        "assume_role_policy_document": assume_role_policy_document,
                        "description": description,
                        "max_session_duration": max_session_duration,
                        "tags": tags,
                    },
                )
                result["comment"] = (f"Would create aws.iam.role '{name}'",)
                return result

            ret = await hub.exec.boto3.client.iam.create_role(
                ctx,
                RoleName=name,
                AssumeRolePolicyDocument=assume_role_policy_document,
                Description=description,
                MaxSessionDuration=max_session_duration,
                PermissionsBoundary=permissions_boundary,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = result["comment"] + ret["comment"]
                return result
            result[
                "new_state"
            ] = hub.tool.aws.iam.conversion_utils.convert_raw_role_to_present(
                raw_resource=ret["ret"]["Role"]
            )
            resource_id = result["new_state"]["resource_id"]
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=1,
                default_max_attempts=40,
                timeout_config=timeout.get("create") if timeout else None,
            )
            hub.log.debug(f"Waiting on creation of aws.iam.role '{name}'")
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "iam",
                    "role_exists",
                    RoleName=result["new_state"]["resource_id"],
                    WaiterConfig=waiter_config,
                )
            except Exception as e:
                result["comment"] = result["comment"] + (str(e),)
                result["result"] = False
            result["comment"] = result["comment"] + (f"Created aws.iam.role '{name}'",)
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)
            result["result"] = False

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.aws.iam.role.get(
                ctx=ctx, name=name, resource_id=resource_id
            )
            if not after["result"] or not after["ret"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] = result["comment"] + (str(e),)
        result["result"] = False
    return result


async def absent(
    hub, ctx, name: str, resource_id: str = None, detach_role_policies: bool = False
) -> Dict[str, Any]:
    r"""
    **Autogenerated function**

    Deletes the specified role. The role must not have any policies attached. For more information about roles, see
    Working with roles.  Make sure that you do not have any Amazon EC2 instances running with the role you are about
    to delete. Deleting a role or instance profile that is associated with a running instance will break any
    applications running on the instance.

    Args:
        name(Text): AWS IAM Role Name.
        resource_id(Text, Optional): AWS IAM Role Name to identify the IAM role on AWS.
        detach_role_policies(Bool, Default: False): if true role is detached from policies before deleted

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws.iam.role.absent:
                - resource_id: value
                - detach_role_policies: True
    """

    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.role", name=name
        )
        return result
    before = await hub.exec.aws.iam.role.get(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.role", name=name
        )
        return result
    elif ctx.get("test", False):
        result["old_state"] = copy.deepcopy(before["ret"])
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.iam.role", name=name
        )
        return result
    else:
        try:
            result["old_state"] = copy.deepcopy(before["ret"])

            # Delete instance profiles for the role
            ret = await hub.exec.boto3.client.iam.list_instance_profiles_for_role(
                ctx, RoleName=result["old_state"]["resource_id"]
            )
            if ret["result"]:
                if ret["ret"] and ret["ret"].get("InstanceProfiles", None):
                    for instance_profile in ret["ret"]["InstanceProfiles"]:
                        ip_name = instance_profile["InstanceProfileName"]
                        hub.log.debug(f"Deleting aws.iam.instance_profile {ip_name}")
                        ret_delete = await hub.exec.boto3.client.iam.remove_role_from_instance_profile(
                            ctx, InstanceProfileName=ip_name, RoleName=name
                        )
                        if not ret_delete["result"]:
                            hub.log.warning(
                                f"Failed to remove role {name} from aws.iam.instance_profile {ip_name}: {ret_delete['comment']}"
                            )
                            continue
                else:
                    hub.log.debug(
                        f"There are no aws.iam.instance_profile(s) for role {name}"
                    )
            else:
                hub.log.warning(
                    f"Failed to list aws.iam.instance_profile for role {name}: {ret['comment']}"
                )

            if detach_role_policies:
                # Delete role's attached policies
                ret = await hub.exec.boto3.client.iam.list_attached_role_policies(
                    ctx=ctx, RoleName=name
                )
                if ret["result"]:
                    if ret["ret"] and ret["ret"].get("AttachedPolicies", None):
                        for rp_attachment in ret["ret"]["AttachedPolicies"]:
                            policy_arn = rp_attachment["PolicyArn"]
                            hub.log.debug(
                                f"Deleting aws.iam.role_policy_attachment {policy_arn} for role {name}"
                            )
                            ret_delete = (
                                await hub.states.aws.iam.role_policy_attachment.absent(
                                    ctx=ctx,
                                    name=name,
                                    role_name=name,
                                    policy_arn=policy_arn,
                                )
                            )
                            if not ret_delete["result"]:
                                hub.log.warning(
                                    f"Failed to delete aws.iam.role_policy_attachment {policy_arn} for role {name}: {ret_delete['comment']}"
                                )
                                continue
                    else:
                        hub.log.debug(
                            f"There are no aws.iam.role_policy_attachment for role {name}"
                        )
                else:
                    hub.log.warning(
                        f"Failed to list attached policies for role {name}: {ret['comment']}"
                    )

                # Delete role's inline policies
                ret = await hub.exec.boto3.client.iam.list_role_policies(
                    ctx, RoleName=name
                )
                if ret["result"]:
                    if ret["ret"] and ret["ret"].get("PolicyNames", None):
                        for policy_name in ret["ret"]["PolicyNames"]:
                            hub.log.debug(
                                f"Deleting aws.iam.role_policy {policy_name} on role {name}"
                            )
                            ret_delete = await hub.states.aws.iam.role_policy.absent(
                                ctx=ctx, name=policy_name, role_name=name
                            )
                            if not ret_delete["result"]:
                                hub.log.warning(
                                    f"Failed to delete aws.iam.role_policy {policy_name} for role {name}: {ret_delete['comment']}"
                                )
                                continue
                    else:
                        hub.log.debug(
                            f"There are no aws.iam.role_policy for role {name}"
                        )
                else:
                    hub.log.warning(
                        f"Failed to list inline policies for role {name}: {ret['comment']}"
                    )

            ret = await hub.exec.boto3.client.iam.delete_role(ctx=ctx, RoleName=name)
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.iam.role", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = (f"{e.__class__.__name__}: {e}",)

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""
    **Autogenerated function**

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function


    Lists the IAM roles that have the specified path prefix. If there are none, the operation returns an empty list.
    For more information about roles, see Working with roles.  IAM resource-listing operations return a subset of
    the available attributes for the resource. For example, this operation does not return tags, even though they
    are an attribute of the returned object. To view all of the information for a role, see GetRole.  You can
    paginate the results using the MaxItems and Marker parameters.


    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws.iam.role
    """

    result = {}
    ret = await hub.exec.boto3.client.iam.list_roles(ctx)

    if not ret["result"]:
        hub.log.debug(f"Could not describe role {ret['comment']}")
        return {}

    for role in ret["ret"]["Roles"]:
        # This is required to get tags for each role
        boto2_resource = await hub.tool.boto3.resource.create(
            ctx, "iam", "Role", role.get("RoleName")
        )
        resource = await hub.tool.boto3.resource.describe(boto2_resource)
        translated_resource = (
            hub.tool.aws.iam.conversion_utils.convert_raw_role_to_present(resource)
        )
        resource_key = f"iam-role-{translated_resource['resource_id']}"
        result[resource_key] = {
            "aws.iam.role.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }

    return result


async def search(hub, ctx, name: str):
    """
    Use an un-managed role as a data-source. Provide role name as input. This function has been deprecated.
    Please use exec.run with aws.iam.role.get instead.

    Args:
        name(string): An Idem name of the IAM role.

    Request Syntax:
        [Idem-state-name]:
          aws.iam.role.search:
          - name: 'string'


    Examples:

        Input state file:
        .. code-block:: bash
            idem-test-role-search:
                aws.iam.role.search:
                  - name: eks-idem-test

    """
    hub.log.warning(
        f"aws.iam.role.search '{name}' state has been deprecated. Please use exec.run with aws.iam.role.get instead."
    )
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    ret = await hub.exec.aws.iam.role.get(ctx, name=name, resource_id=name)
    result["result"] = ret["result"]
    result["comment"] = ret["comment"]
    if result["result"] and ret["ret"]:
        result["old_state"] = ret["ret"]
        # Populate both "old_state" and "new_state" with the same data
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result
