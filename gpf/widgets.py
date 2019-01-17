from django.forms import widgets

class RemoteAutocompleteWidget(widgets.TextInput):
    template_name = 'remoteautocomplete/remoteautocomplete.html'
    pass
