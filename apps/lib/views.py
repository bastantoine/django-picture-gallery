from django.conf import settings
from django.views import View
from django.shortcuts import render


class BaseView(View):
    pagetitle = ''

    def get_context_data(self, **kwargs):
        """Base function to get the context of a view. Useful to share some values across all views
        or at least a bunch of views.
        """
        base_titlepage = settings.PAGETITLE if settings.PAGETITLE else ''
        if self.pagetitle.strip():
            base_titlepage = ' | %s' % base_titlepage
        context = {
            "base_pagetitle": base_titlepage,
            'pagetitle': self.pagetitle.strip(),
        }
        return context

    def render(self, request, template, *args, **kwargs):
        """Helper used mainly to ensure that the shared data added by self.get_context_data are
        there, and set the missing values.

        Note that if a shared value (ie. one added by self.get_context_data) has changed in the
        current context, it WON'T be changed to the default value.
        """
        base_context = self.get_context_data()
        context = kwargs.pop('context', {})
        for key, value in base_context.items():
            if key not in context:
                context[key] = value
        return render(request, template, context=context, *args, **kwargs)

