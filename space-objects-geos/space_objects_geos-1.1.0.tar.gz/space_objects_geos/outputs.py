from geojson import Feature, FeatureCollection
from shapely.geometry import LineString, MultiLineString, MultiPoint, Point
from space_objects.base.outputs import ForecastListObject, OrbitObject, PositionObject


class PositionObjectGeos:
    """
    Provide shapely geometries objects for a PositionObject and add a geojson property.
    """

    def __init__(self, position: PositionObject) -> None:
        self.position = position
        self.geometry = Point(position.longitude, position.latitude)

    @property
    def geojson(self):
        return FeatureCollection(
            [Feature(geometry=self.geometry, properties=self.position.to_dict())]
        )


class OrbitObjectGeos:
    """
    Provide geometries objects for a OrbitObject and add a geojson property.
    """

    def __init__(self, orbit: OrbitObject) -> None:
        self.orbit = orbit

        self.part_one_geometry = (
            LineString(
                [(i.longitude, i.latitude, i.altitude_kms) for i in orbit.part_one]
            )
            if orbit.part_one
            else None
        )
        self.part_two_geometry = (
            LineString(
                [(i.longitude, i.latitude, i.altitude_kms) for i in orbit.part_two]
            )
            if orbit.part_two
            else None
        )
        self.geometry = MultiLineString(
            list(filter(None, [self.part_one_geometry, self.part_two_geometry]))
        )

    @property
    def geojson(self):
        return FeatureCollection(
            [
                Feature(
                    geometry=self.geometry,
                    properties={
                        "direction": self.orbit.direction,
                        "date_start": self.orbit.date_start,
                        "date_end": self.orbit.date_end,
                    },
                )
            ]
        )


class ForecastListObjectGeos:
    """
    Provide geometries objects for a ForecastListObject and add a geojson property.
    """

    def __init__(self, forecast: ForecastListObject) -> None:
        self.forecast = forecast
        self.geometry = MultiPoint(
            [Point(p.position.longitude, p.position.latitude) for p in forecast]
        )

    @property
    def geojson(self):
        return FeatureCollection(
            [
                Feature(
                    geometry=Point(p.position.longitude, p.position.latitude),
                    properties=p.to_dict(),
                )
                for p in self.forecast
            ]
        )
