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
import time
from typing import Any

import gql
from qctrlclient import GraphQLClient

from .action_status import ActionStatus

# pylint:disable=unsubscriptable-object


class FireOpalClient(GraphQLClient):
    """Client for accessing the Fire Opal API."""

    _COMPLETED_STATES = (ActionStatus.SUCCESS.value, ActionStatus.FAILURE.value)

    def poll_for_completion(
        self, action_id: str, status: str, result: Any, errors: Any
    ) -> Any:
        """Polls the API waiting for the action to be completed.
        When completed, the `result` is returned.
        """

        _query = gql.gql(
            """
            query($modelId: String!) {
                action(modelId: $modelId) {
                    action {
                        status
                        errors {
                            exception
                            traceback
                        }
                        result
                    }
                    errors {
                        message
                    }
                }
            }
        """
        )

        while status not in self._COMPLETED_STATES:
            time.sleep(2)  # FIXME use progressive polling
            response = self.execute(_query, {"modelId": action_id})
            status = response["action"]["action"]["status"]
            result = response["action"]["action"]["result"]
            errors = response["action"]["action"]["errors"]

        if status == ActionStatus.FAILURE.value:
            raise RuntimeError(errors)

        if result is not None:
            result = json.loads(result)

        return result
