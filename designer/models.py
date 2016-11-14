from django.core.validators import RegexValidator
from django.db import models
from uuslug import uuslug
from smart_selects.db_fields import ChainedManyToManyField


# Create your models here.


class Schema(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100, unique=True)
    slug = models.CharField(max_length=100)
    description = models.CharField(blank=True, null=True, max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Schema, self).save(*args, **kwargs)


PROPERTY_TYPE_CHOICES = (
    ('Smallint', 'Smallint'),
    ('Int', 'Int'),
    ('Bigint', 'Bigint'),
    ('Varint', 'Varint'),
    ('Float', 'Float'),
    ('Double', 'Double'),
    ('Decimal', 'Decimal'),
    ('Boolean', 'Boolean'),
    ('Text', 'Text'),
    ('Uuid', 'Uuid'),
    ('Timestamp', 'Timestamp'),
    ('Duration', 'Duration'),
    ('Linestring', 'Linestring'),
    ('Polygon', 'Polygon'),
    ('Inet', 'Inet'),
    ('Blob', 'Blob'),
)


class Property(models.Model):
    name = models.CharField(blank=False, null=False,  max_length=50, validators=[
            RegexValidator(
                regex='^[a-zA-Z_$][a-zA-Z_$0-9]*$',
                message='Property name doesn\'t comply',
            ),
        ])
    description = models.CharField(blank=True, null=True, max_length=100)
    schema = models.ForeignKey(Schema, related_name='properties')
    property_type = models.CharField(max_length=10,
                                     choices=PROPERTY_TYPE_CHOICES,
                                     default='Text')
    multiple_cardinality = models.BooleanField(default=False,
                                              help_text='Property with multiple values [Single cardinality is default]')
    meta_properties = models.ManyToManyField('Property', blank=True)

    def __str__(self):
        return u'%s --> %s (%s):[%s]' % (self.schema.name, self.name, self.property_type, self.meta_properties.count())

    class Meta:
        verbose_name_plural = "properties"
        unique_together = ('schema', 'name')


class VertexLabel(models.Model):
    label = models.CharField(blank=False, null=False, max_length=50, validators=[
        RegexValidator(
            regex='^[a-zA-Z_$][a-zA-Z_$0-9]*$',
            message='Vertex label doesn\'t comply',
        ),
    ])
    description = models.CharField(blank=True, null=True, max_length=100)
    schema = models.ForeignKey(Schema, related_name='vertices')
    properties = models.ManyToManyField(Property, blank=True, related_name="vertex_labels")

    def __str__(self):
        return u'%s --> %s' % (self.schema.name, self.label)

    class Meta:
        unique_together = ('schema', 'label')


class EdgeLabel(models.Model):
    label = models.CharField(blank=False, null=False, max_length=50, validators=[
        RegexValidator(
            regex='^[a-zA-Z_$][a-zA-Z_$0-9]*$',
            message='Vertex label doesn\'t comply',
        ),
    ])

    description = models.CharField(blank=True, null=True, max_length=100)
    schema = models.ForeignKey(Schema, related_name='edges')
    properties = models.ManyToManyField(Property, blank=True)

    multiple_cardinality = models.BooleanField(default=False,
                                              help_text='Edge cardinality [Single cardinality is default]')

    def __str__(self):
        return u'%s --> %s' % (self.schema.name, self.label)

    class Meta:
        unique_together = ('schema', 'label')


class EdgeConnection(models.Model):
    from_vertex = models.ForeignKey(VertexLabel, related_name='from_connections')
    to_vertex = models.ForeignKey(VertexLabel, related_name='to_connections')
    edge = models.ForeignKey(EdgeLabel, related_name='connections')


INDEX_TYPE_CHOICES = (
    ('materialized', 'Materialized'),
    ('secondary', 'Secondary'),
    ('search', 'Search'),
)


class VertexIndex(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50, validators=[
        RegexValidator(
            regex='^[a-zA-Z_$][a-zA-Z_$0-9]*$',
            message='Index Name doesn\'t comply',
        ),
    ])
    vertex = models.ForeignKey(VertexLabel, related_name='vertex_indexes')
    description = models.CharField(blank=True, null=True, max_length=100)
    property_type = models.CharField(max_length=12,
                                     choices=INDEX_TYPE_CHOICES)
    properties = ChainedManyToManyField(
        Property,
        chained_field="vertex",
        chained_model_field="vertex_labels",
    )


    class Meta:
        unique_together = ('vertex', 'name')