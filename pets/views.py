from django.urls import reverse
from django.views.generic import CreateView

from pets.forms import ImagePetFormSet, PetForm

# class PetAddView(CreateView):
#     model = Pet
#     form_class = ImagePetForm
#     template_name = 'pets/pet_add.html'
#
#     def get_context_data(self, **kwargs):
#         ctx = super(PetAddView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             ctx['form'] = PetForm(self.request.POST)
#             ctx['inlines'] = PetFormSet(self.request.POST)
#         else:
#             ctx['form'] = PetForm()
#             ctx['inlines'] = PetFormSet()
#         return ctx
#
#     def form_valid(self, form):
#         pet = form.save(commit=False)
#         pet.author = self.request.user
#         pet.save()
#         return super().form_valid(form)


class PetAddView(CreateView):
    form_class = PetForm
    template_name = 'pets/pet_add.html'

    def get_context_data(self, **kwargs):
        data = super(PetAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['imagepet'] = ImagePetFormSet(self.request.POST)
        else:
            data['imagepet'] = ImagePetFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        imagepet = context['imagepet']

        pet = form.save(commit=False)
        pet.master = self.request.user
        pet.save()
        imagepet.save()
        return super().form_valid(form)
        # with transaction.commit_on_success():
        #     form.instance.created_by = self.request.user
        #     form.instance.updated_by = self.request.user
        #     pet = form.save(commit=False)
        #     pet.author = self.request.user
        #     pet.save()
            # self.object = form.save()
        # if imagepet.is_valid():
        #     # imagepet.instance = self.object
        #     imagepet.save()

        # return super(PetAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse('index')
