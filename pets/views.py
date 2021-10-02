from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from pets.forms import ImagePetFormSet, PetForm
from pets.models import Pet, ImagePet


class PetAddView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_add.html'

    def get_context_data(self, **kwargs):
        data = super(PetAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['imagepet'] = ImagePetFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=ImagePet.objects.none()
            )
        else:
            data['imagepet'] = ImagePetFormSet()
        return data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # Add as many formsets here as you want
        image_formset = ImagePetFormSet(self.request.POST, self.request.FILES,
                                        queryset=ImagePet.objects.none())

        # Now validate both the form and any formsets
        if form.is_valid():  # and image_formset.is_valid():
            # Note - we are passing the education_formset to form_valid. If you had more formsets
            # you would pass these as well.
            if image_formset.is_valid():
                print('image_formset.is_valid()')
            print(image_formset.non_form_errors())
            return self.form_valid(form, image_formset)
        else:
            print(image_formset)
            if image_formset.is_valid():
                print('image_formset.is_valid()')
            print("INValid")
            return self.form_invalid(form)

    def form_valid(self, form, image_formset):
        pet = form.save(commit=False)
        pet.master = self.request.user
        pet.save()

        for form1 in image_formset.cleaned_data:
            # this helps to not crash if the user
            # do not upload all the photos
            if form1:
                image = form1['image']
                photo = ImagePet(pet=pet, image=image)
                photo.save()
        # images = image_formset.save(commit=False)
        # for image in images:
        #     image.save()
        # with transaction.atomic():
            # form.instance.pet.master = self.request.user
            # form.save()
            # Now we process the education formset
            # images = image_formset.save(commit=False)
            # for image in images:
            #     image.instance = pet
            #     image.save()
            # If you had more formsets, you would accept additional arguments and
            # process them as with the one above.
        # Don't call the super() method here - you will end up saving the form twice. Instead handle the redirect yourself.
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')
