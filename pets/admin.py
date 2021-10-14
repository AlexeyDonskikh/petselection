from django.contrib import admin

from pets.models import Breed, ImagePet, Pet, Species


class PetAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'age', 'weight', 'species', 'breed', 'description', 'master'
    )
    fields = (
        'name', 'age', 'weight', 'species', 'breed', 'description', 'master'
    )
    raw_id_fields = ('species', 'breed', 'master',)
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


class ImagePetAdmin(admin.ModelAdmin):
    list_display = (
        'pet', 'image', 'image_name',
    )
    fields = (
        'pet', 'image', 'image_name',
    )
    raw_id_fields = ('pet',)
    search_fields = ('pet',)
    list_filter = ('pet',)
    empty_value_display = '-пусто-'


admin.site.register(Pet, PetAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Breed, BreedAdmin)
admin.site.register(ImagePet, ImagePetAdmin)
