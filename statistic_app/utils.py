from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


class ObjectUpdateMixin:
    model = None
    form_model = None
    template = None

    def get(self, request, slug):
        object = self.model.objects.get(url__iexact=slug)
        bound_form = self.form_model(instance=object)
        return render(request, self.template, context={
            'form': bound_form,
            self.model.__name__.lower(): object,
        })

    def post(self, request, slug):
        object = self.model.objects.get(url__iexact=slug)
        bound_form = self.form_model(request.POST, instance=object)

        if bound_form.is_valid():
            new_object = bound_form.save()
            return redirect(new_object)
        return render(request, self.template, context={
            'form': bound_form,
            self.model.__name__.lower(): object,
        })


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form_model(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            return render(request, self.template, context={'form': bound_form})