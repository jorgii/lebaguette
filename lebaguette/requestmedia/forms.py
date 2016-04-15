from django.forms import ModelForm

from .models import MediaItem


class MediaItemForm(ModelForm):
    class Meta:
        model = MediaItem
        fields = ['title', 'media_type', 'released', 'imdb_rating', 'imdb_id']
