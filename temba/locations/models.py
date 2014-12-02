import logging
from smartmin.models import SmartModel

logger = logging.getLogger(__name__)

from django.contrib.gis.db import models
import geojson

COUNTRY_LEVEL = 0
STATE_LEVEL = 1
DISTRICT_LEVEL = 2

class AdminBoundary(models.Model):
    """
    Represents a single administrative boundary (like a country, state or district)
    """
    osm_id = models.CharField(max_length=15, unique=True,
                              help_text="This is the OSM id for this administrative boundary")

    name = models.CharField(max_length=128,
                            help_text="The name of our administrative boundary")

    level = models.IntegerField(help_text="The level of the boundary, 0 for country, 1 for state, 2 for district")

    parent = models.ForeignKey('locations.AdminBoundary', null=True, related_name='children',
                               help_text="The parent to this political boundary if any")

    geometry = models.MultiPolygonField(null=True,
                                        help_text="The full geometry of this administrative boundary")

    simplified_geometry = models.MultiPolygonField(null=True,
                                                   help_text="The simplified geometry of this administrative boundary")

    objects = models.GeoManager()

    @staticmethod
    def get_geojson_dump(features):
        # build a feature collection
        feature_collection = geojson.FeatureCollection(features)
        return geojson.dumps(feature_collection)

    def as_json(self):
        result = dict(osm_id=self.osm_id, name=self.name, level=self.level, aliases='')

        if self.parent:
            result['parent_osm_id'] = self.parent.osm_id

        aliases = '\n'.join([alias.name for alias in self.aliases.all()])
        result['aliases'] = aliases
        return result

    def get_geojson_feature(self):
        return geojson.Feature(properties=dict(name=self.name, osm_id=self.osm_id, id=self.pk, level=self.level),
                               geometry=geojson.loads(self.simplified_geometry.geojson))

    def get_geojson(self):
        return AdminBoundary.get_geojson_dump([self.get_geojson_feature()])

    def get_children_geojson(self):
        children = []
        for child in self.children.all():
            children.append(child.get_geojson_feature())
        return AdminBoundary.get_geojson_dump(children)

    def __unicode__(self):
        return "%s" % self.name


class BoundaryAlias(SmartModel):

    """
    Alternative names for a boundaries
    """

    name = models.CharField(max_length=128, help_text="The name for our alias")

    boundary = models.ForeignKey(AdminBoundary, help_text='The admin boundary this alias applies to', related_name='aliases')

    org = models.ForeignKey('orgs.Org', help_text="The org that owns this alias")








