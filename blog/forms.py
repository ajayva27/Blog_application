from django import forms
from .models import Post
from ckeditor.fields import RichTextField  

class PostForm(forms.ModelForm):
    content = RichTextField()

    class Meta:
        model = Post
        fields = ['title', 'content']  
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter post title',
                'class': 'block w-full rounded-md border border-gray-300 p-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'content': forms.Textarea(attrs={
                'style': 'display:none;'  
            }),
        }
