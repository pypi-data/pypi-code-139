import copy

from libcove2.common import fields_present_generator


class JSONToGeoJSONConverter:
    def __init__(self):
        self._nodes_geojson_features: list = []
        self._spans_geojson_features: list = []

    def process_package(self, package_data: dict) -> None:
        for network in package_data.get("networks", []):
            self._process_network(network)

    def _process_network(self, network_data: dict) -> None:
        nodes = network_data.pop("nodes", [])
        spans = network_data.pop("spans", [])
        phases = network_data.pop("phases", [])
        organisations = network_data.pop("organisations", [])

        # Dereference `contracts.relatedPhases`
        if "contracts" in network_data and isinstance(network_data["contracts"], list):
            for contract in network_data["contracts"]:
                if "relatedPhases" in contract and isinstance(
                    contract["relatedPhases"], list
                ):
                    contract["relatedPhases"] = [
                        self._dereference_object(phase, phases)
                        for phase in contract["relatedPhases"]
                    ]

        # Convert nodes to features
        for node in nodes:
            self._nodes_geojson_features.append(
                self._convert_node_to_feature(node, network_data, organisations, phases)
            )

        # Convert spans to features
        for span in spans:
            self._spans_geojson_features.append(
                self._convert_span_to_feature(
                    span, network_data, organisations, phases, nodes
                )
            )

    def get_nodes_geojson(self) -> dict:
        return {"type": "FeatureCollection", "features": self._nodes_geojson_features}

    def get_spans_geojson(self) -> dict:
        return {"type": "FeatureCollection", "features": self._spans_geojson_features}

    def get_meta_json(self) -> dict:
        out: dict = {
            "nodes_output_field_coverage": {},
            "spans_output_field_coverage": {},
        }
        # nodes field coverage
        for key, value in fields_present_generator(self.get_nodes_geojson()):
            if key not in out["nodes_output_field_coverage"]:
                out["nodes_output_field_coverage"][key] = {"count": 1}
            else:
                out["nodes_output_field_coverage"][key]["count"] += 1
        # spans field coverage
        for key, value in fields_present_generator(self.get_spans_geojson()):
            if key not in out["spans_output_field_coverage"]:
                out["spans_output_field_coverage"][key] = {"count": 1}
            else:
                out["spans_output_field_coverage"][key]["count"] += 1
        # return
        return out

    def _dereference_object(self, ref, list):
        """
        Return from list the object referenced by ref. Otherwise, return ref.
        """

        if "id" in ref:
            for item in list:
                if item.get("id") == ref["id"]:
                    return item

        return ref

    def _convert_node_to_feature(
        self,
        node_data: dict,
        reduced_network_data: dict,
        organisations: list,
        phases: list,
    ) -> dict:

        reduced_node_data = copy.deepcopy(node_data)

        feature = {
            "type": "Feature",
            "geometry": reduced_node_data.pop("location")
            if isinstance(reduced_node_data.get("location"), dict)
            else None,
        }

        # Dereference organisation references
        for organisationReference in [
            "physicalInfrastructureProvider",
            "networkProvider",
        ]:
            if organisationReference in reduced_node_data:
                reduced_node_data[organisationReference] = self._dereference_object(
                    reduced_node_data[organisationReference], organisations
                )

        # Dereference phase references
        if "phase" in reduced_node_data:
            reduced_node_data["phase"] = self._dereference_object(
                reduced_node_data["phase"], phases
            )

        feature["properties"] = reduced_node_data
        feature["properties"]["network"] = reduced_network_data

        return feature

    def _convert_span_to_feature(
        self,
        span_data: dict,
        reduced_network_data: dict,
        organisations: list,
        phases: list,
        nodes: list,
    ) -> dict:

        reduced_span_data = copy.deepcopy(span_data)

        feature = {
            "type": "Feature",
            "geometry": reduced_span_data.pop("route")
            if isinstance(reduced_span_data.get("route"), dict)
            else None,
        }

        # Dereference organisation references
        for organisationReference in [
            "physicalInfrastructureProvider",
            "networkProvider",
        ]:
            if organisationReference in reduced_span_data:
                reduced_span_data[organisationReference] = self._dereference_object(
                    reduced_span_data[organisationReference], organisations
                )

        # Dereference phase references
        if "phase" in reduced_span_data:
            reduced_span_data["phase"] = self._dereference_object(
                reduced_span_data["phase"], phases
            )

        # Dereference endpoints
        for endpoint in ["start", "end"]:
            if endpoint in reduced_span_data:
                for node in nodes:
                    if "id" in node and node["id"] == reduced_span_data[endpoint]:
                        reduced_span_data[endpoint] = node

        feature["properties"] = reduced_span_data
        feature["properties"]["network"] = reduced_network_data

        return feature


class GeoJSONToJSONConverter:
    def __init__(self):
        self._networks: dict = {}

    def process_data(self, nodes_data: dict, spans_data: dict) -> None:
        # Network
        for geojson_feature in nodes_data.get("features", []):
            self._process_network(geojson_feature)
        for geojson_feature in spans_data.get("features", []):
            self._process_network(geojson_feature)

        # Nodes
        for geojson_feature in nodes_data.get("features", []):
            self._process_node(geojson_feature)

        # Spans
        for geojson_feature in spans_data.get("features", []):
            self._process_span(geojson_feature)

    def _process_network(self, geojson_feature_node_or_span: dict) -> None:
        if (
            "properties" in geojson_feature_node_or_span
            and "network" in geojson_feature_node_or_span["properties"]
        ):
            network = geojson_feature_node_or_span["properties"]["network"]
            if network.get("id"):
                # TODO check for inconsistent data here!
                self._networks[network.get("id")] = copy.deepcopy(network)
                self._networks[network.get("id")]["nodes"] = []
                self._networks[network.get("id")]["spans"] = []
                self._networks[network.get("id")]["phases"] = {}
                self._networks[network.get("id")]["organisations"] = {}

                # Sort references to phases in contracts
                if "contracts" in self._networks[network.get("id")] and isinstance(
                    self._networks[network.get("id")]["contracts"], list
                ):
                    for contract in self._networks[network.get("id")]["contracts"]:
                        if "relatedPhases" in contract and isinstance(
                            contract["relatedPhases"], list
                        ):
                            out: list = []
                            for phase_reference in contract["relatedPhases"]:
                                phase_id = self._process_phase(
                                    network.get("id"), phase_reference
                                )
                                if phase_id:
                                    out.append({"id": phase_id})
                                else:
                                    out.append(phase_reference)
                            contract["relatedPhases"] = out

    def _process_node(self, geojson_feature_node: dict) -> None:
        node = copy.deepcopy(geojson_feature_node.get("properties", {}))
        for key_to_remove in ["network"]:
            if key_to_remove in node:
                del node[key_to_remove]
        network_id = (
            geojson_feature_node.get("properties", {}).get("network", {}).get("id")
        )
        if network_id not in self._networks.keys():
            # TODO log error
            return

        # sort organisations
        for field in ["physicalInfrastructureProvider", "networkProvider"]:
            if isinstance(node.get(field), dict) and node.get(field):
                organisation_id = self._process_organisation(network_id, node[field])
                if organisation_id:
                    node[field] = {"id": organisation_id}

        # sort phase
        if isinstance(node.get("phase"), dict) and node.get("phase"):
            phase_id = self._process_phase(network_id, node["phase"])
            if phase_id:
                node["phase"] = {"id": phase_id}

        if geojson_feature_node.get("geometry"):
            node["location"] = geojson_feature_node["geometry"]

        self._networks[network_id]["nodes"].append(node)

    def _process_span(self, geojson_feature_span: dict) -> None:
        span = copy.deepcopy(geojson_feature_span.get("properties", {}))
        for key_to_remove in ["network"]:
            if key_to_remove in span:
                del span[key_to_remove]
        network_id = (
            geojson_feature_span.get("properties", {}).get("network", {}).get("id")
        )
        if network_id not in self._networks.keys():
            # TODO log error
            return

        # sort organisations
        for field in ["physicalInfrastructureProvider", "networkProvider", "supplier"]:
            if isinstance(span.get(field), dict) and span.get(field):
                organisation_id = self._process_organisation(network_id, span[field])
                if organisation_id:
                    span[field] = {"id": organisation_id}

        # sort phase
        if isinstance(span.get("phase"), dict) and span.get("phase"):
            phase_id = self._process_phase(network_id, span["phase"])
            if phase_id:
                span["phase"] = {"id": phase_id}

        if geojson_feature_span.get("geometry"):
            span["route"] = geojson_feature_span["geometry"]

        span["start"] = span.get("start", {}).get("id")
        span["end"] = span.get("end", {}).get("id")

        self._networks[network_id]["spans"].append(span)

    def _process_phase(self, network_id: str, phase: dict) -> str:
        phase_id = phase.get("id")
        if phase_id:
            if phase_id in self._networks[network_id]["phases"]:
                # TODO check value is same, add error if not
                pass
            else:
                self._networks[network_id]["phases"][phase_id] = phase
            return phase_id
        return ""

    def _process_organisation(self, network_id: str, organisation: dict) -> str:
        organisation_id = organisation.get("id")
        if organisation_id:
            if organisation_id in self._networks[network_id]["organisations"]:
                # TODO check value is same, add error if not
                pass
            else:
                self._networks[network_id]["organisations"][
                    organisation_id
                ] = organisation
            return organisation_id
        return ""

    def get_json(self) -> dict:
        out: dict = {"networks": []}
        for network in self._networks.values():
            # We are going to change network, so we need to take a copy
            network = copy.deepcopy(network)
            # Arrays have minItems: 1 set - so if no content, remove the empty array
            for key in ["nodes", "spans", "phases", "organisations", "contracts"]:
                if key in network and not network[key]:
                    del network[key]
            # Sometimes we store these things in dicts - turn to lists
            for key in ["phases", "organisations"]:
                if key in network:
                    network[key] = list(network[key].values())
            out["networks"].append(network)
        return out

    def get_meta_json(self) -> dict:
        out: dict = {"output_field_coverage": {}}
        # field coverage
        for key, value in fields_present_generator(self.get_json()):
            if key not in out["output_field_coverage"]:
                out["output_field_coverage"][key] = {"count": 1}
            else:
                out["output_field_coverage"][key]["count"] += 1
        # return
        return out
