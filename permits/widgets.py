from django.forms import widgets

class RemoteAutocompleteWidget(widgets.TextInput):
    template_name = 'remoteautocomplete/remoteautocomplete_multiform.html'
