from django.contrib import admin

from pets.models import Pet, Species, Breed


class PetAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'age', 'weight', 'species', 'breed', 'description', 'master'
    )
    fields = (
        'name', 'age', 'weight', 'species', 'breed', 'description', 'master'
    )
    search_fields = ('name', 'species', 'breed', 'master', 'age')
    list_filter = ('species', 'name')
    empty_value_display = '-пусто-'


class SpeciesAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug',
    )
    fields = (
        'name', 'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class BreedAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'species', 'slug',
    )
    fields = (
        'name', 'species', 'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Pet, PetAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Breed, BreedAdmin)
