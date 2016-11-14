from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from designer.models import Schema


class SchemaDetailView(DetailView):
    model = Schema

    def get_context_data(self, **kwargs):
        context = super(SchemaDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class SchemaListView(ListView):
    model = Schema
