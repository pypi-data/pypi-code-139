# Copyright 2022 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

import json
from functools import wraps
from typing import Callable

import gql

from fireopal.globals import get_client

_REGISTRY = "FIRE_OPAL"


def start_core_workflow(workflow: str):
    """Decorator for function which invokes a core workflow. The decorated
    function should return a dictionary which will be used as the `data` field
    in the request to `startCoreWorkflow`. The `workflow` name must match the
    name the workflow is registered under in the Fire Opal workflow registry.
    """

    def decorator(func: Callable):
        @wraps(func)
        def customized_decorator(*args, **kwargs):
            data = func(*args, **kwargs)

            query = gql.gql(
                """
                mutation ($input: StartCoreWorkflowInput!) {
                    startCoreWorkflow(input: $input) {
                        action {
                            modelId
                            status
                            result
                            errors {
                                exception
                                traceback
                            }
                        }
                        errors {
                            message
                            fields
                        }
                    }
                }
            """
            )

            input_ = {
                "registry": _REGISTRY,
                "workflow": workflow,
                "data": json.dumps(data),
            }

            client = get_client()
            response = client.execute(query, {"input": input_})

            # pylint:disable=unsubscriptable-object

            action_id = response["startCoreWorkflow"]["action"]["modelId"]
            status = response["startCoreWorkflow"]["action"]["status"]
            result = response["startCoreWorkflow"]["action"]["result"]
            errors = response["startCoreWorkflow"]["action"]["errors"]

            result = client.poll_for_completion(action_id, status, result, errors)
            return result

        return customized_decorator

    return decorator
