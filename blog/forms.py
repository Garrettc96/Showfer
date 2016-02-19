from django import forms

from .models import Post
from .models import Anime

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class AnimeForm(forms.ModelForm):

	class Meta:
		model = Anime
		exclude = ['title','crunchy','hulu','funi','netflix', 'image','year']