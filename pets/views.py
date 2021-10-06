from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from pets.forms import ImagePetFormSet, PetForm
from pets.models import ImagePet, Pet
from petselection import settings


class MyPetListView(ListView):
    model = Pet
    template_name = 'pets/my_pets.html'
    paginate_by = settings.PAGINATION_PAGE_SIZE
    context_object_name = 'my_pets'

    def get_queryset(self):
        return Pet.objects.filter(master=self.request.user)


class PetDetailView(DetailView):
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'


class PetAddView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_add.html'

    def get_context_data(self, **kwargs):
        data = super(PetAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['image_pet'] = ImagePetFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=ImagePet.objects.none()
            )
        else:
            data['image_pet'] = ImagePetFormSet()
        return data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        image_formset = ImagePetFormSet(self.request.POST, self.request.FILES,
                                        queryset=ImagePet.objects.none())

        if form.is_valid() and image_formset.is_valid():
            return self.form_valid(form, image_formset)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, image_formset):
        pet = form.save(commit=False)
        pet.master = self.request.user
        pet.save()

        for image_form in image_formset.cleaned_data:
            if image_form:
                image = image_form['image']
                photo = ImagePet(pet=pet, image=image)
                photo.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('my_pets')


class PetUpdateView(UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_update.html'

    # def get_context_data(self, **kwargs):
    #     data = super(PetUpdateView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         data['image_pet'] = ImagePetFormSet(
    #             self.request.POST,
    #             self.request.FILES,
    #             queryset=ImagePet.objects.none()
    #         )
    #     else:
    #         data['image_pet'] = ImagePetFormSet()
    #     return data

    def get_context_data(self, **kwargs):
        context = super(PetUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_pet'] = ImagePetFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['image_pet'].full_clean()
        else:
            context['image_pet'] = ImagePetFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['image_pet']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     image_formset = ImagePetFormSet(self.request.POST, self.request.FILES,
    #                                     queryset=ImagePet.objects.none())
    #
    #     if form.is_valid() and image_formset.is_valid():
    #         return self.form_valid(form, image_formset)
    #     else:
    #         return self.form_invalid(form)
    #
    # def form_valid(self, form, image_formset):
    #     self.object = form.save(commit=False)
    #     self.object.master = self.request.user
    #     self.object.save()
    #     for image_form in image_formset.cleaned_data:
    #         if image_form:
    #             image = image_form['image']
    #             photo = ImagePet(pet=self.object, image=image)
    #             photo.save()
    #     return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('pet_detail', kwargs={'slug': self.object.slug})
