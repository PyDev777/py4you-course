from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages

from .models import *
from .forms import ReviewForm


class IndexView(TemplateView):
    template_name = "home.html"


class EssayDetailView(DetailView):
    template_name = 'essay.html'
    model = Essay

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['reviews'] = Review.objects.filter(essay=self.object, moderated=True).order_by('-published')
        return context

    def post(self, *args, **kwargs):

        self.object = self.get_object()
        self.form = ReviewForm(self.request.POST)

        context = self.get_context_data(**kwargs)

        if self.form.is_valid():
            Review.objects.create(**self.form.cleaned_data)
            messages.add_message(self.request, messages.INFO, 'Thanks! Your review is on moderation.')
        else:
            context['form'] = self.form
            messages.add_message(self.request, messages.ERROR, 'Error! Your review is not send!')

        return self.render_to_response(context)


class ResultListView(ListView):
    template_name = 'result.html'
    paginate_by = 5

    def get_queryset(self):

        q_params = {}

        qi = self.request.GET.get('search_input', '')
        if qi:
            q_params.update(name__contains=qi)

        cat = self.request.GET.get('category', '')
        cat = int(cat) if cat.isdigit() else 0
        if cat:
            q_params.update(cat__id=cat)

        tag = self.request.GET.get('tag', '')
        tag = int(tag) if tag.isdigit() else 0
        if tag:
            q_params.update(tag__id=tag)

        essays = Essay.objects.filter(**q_params).order_by('-published')
        return essays

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q_get = self.request.GET.copy()
        q_get.pop('page', None)
        context['q_get'] = q_get.urlencode()

        return context


def robots_view(request):
    return render(request, 'robots.txt', {}, content_type="text/plain")
