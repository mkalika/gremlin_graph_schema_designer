from django.contrib import admin
from django.db.models import Count

from designer.models import Property, VertexLabel, EdgeLabel, Schema, EdgeConnection, VertexIndex

# Register your models here.


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'schema', 'multiple_cardinality', 'meta_properties_count',)
    list_filter = (('schema', admin.RelatedFieldListFilter), 'multiple_cardinality', )
    ordering = ('schema', 'name',)
    filter_horizontal = ('meta_properties',)

    def get_queryset(self, *args, **kwargs):
        qs = super(PropertyAdmin, self).get_queryset(*args, **kwargs)
        return qs.annotate(num_meta_properties=Count('meta_properties'))

    def meta_properties_count(self, obj):
        return obj.meta_properties.count()
    meta_properties_count.short_description = "Meta Properties Count"
    meta_properties_count.admin_order_field = 'num_meta_properties'

    def get_object(self, request, object_id, from_field=None):
        # Hook obj for use in formfield_for_manytomany
        self.obj = super(PropertyAdmin, self).get_object(request, object_id)
        return self.obj

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "meta_properties":
            if getattr(self, 'obj', None):
                kwargs["queryset"] = Property.objects.exclude(pk=self.obj.id).annotate(num_meta_properties=Count('meta_properties')).\
                    filter(num_meta_properties=0).filter(multiple_cardinality=False)
            else:
                kwargs["queryset"] = Property.objects.annotate(
                    num_meta_properties=Count('meta_properties')). \
                    filter(num_meta_properties=0).filter(multiple_cardinality=False)
        return super(PropertyAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class VertexIndexInline(admin.TabularInline):
    model = VertexIndex


class VertexIndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    # filter_horizontal = ('properties',)
    ordering = ('name',)


class VertexLabelAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'schema',)
    list_filter = (('schema', admin.RelatedFieldListFilter),)
    filter_horizontal = ('properties',)
    ordering = ('label',)
    inlines = [VertexIndexInline, ]


class EdgeConnectionInline(admin.TabularInline):
    model = EdgeConnection


class EdgeLabelAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'schema', 'multiple_cardinality',)
    list_filter = (('schema', admin.RelatedFieldListFilter), 'multiple_cardinality',)
    inlines = [EdgeConnectionInline, ]
    filter_horizontal = ('properties',)
    ordering = ('label',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "properties":
            kwargs["queryset"] = Property.objects.annotate(num_meta_properties=Count('meta_properties')).\
                filter(num_meta_properties=0).filter(multiple_cardinality=False)
        return super(EdgeLabelAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class SchemaAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('name', 'description',)
    ordering = ('name',)


admin.site.register(Schema, SchemaAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(VertexLabel, VertexLabelAdmin)
admin.site.register(EdgeLabel, EdgeLabelAdmin)
#admin.site.register(VertexIndex , VertexIndexAdmin)