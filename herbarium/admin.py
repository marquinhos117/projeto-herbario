from django.contrib import admin # <--- Certifique-se que NÃO tem o .gis aqui
from .models import Person, Taxonomy, Collection, CollectionEvent, Occurrence, IdentificationHistory, SpecimenImage

# Se você usou admin.GISModelAdmin, mude para admin.ModelAdmin
@admin.register(CollectionEvent)
class CollectionEventAdmin(admin.ModelAdmin): # <--- Aqui era GISModelAdmin, mude para ModelAdmin
    list_display = ('municipality', 'state_province', 'collection_date')

@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = ('catalog_number', 'field_number', 'submission_status')

admin.site.register(Person)
admin.site.register(Taxonomy)
admin.site.register(Collection)
admin.site.register(IdentificationHistory)
admin.site.register(SpecimenImage)