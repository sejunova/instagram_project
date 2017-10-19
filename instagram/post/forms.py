from django import forms


class PostForm(forms.Form):
    photo = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    text = forms.CharField(
        max_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_text(self):
        data = self.cleaned_data['text']
        if data != data.upper():
            raise forms.ValidationError('Text must be uppercase')
        return data


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'comment-form'
            }
        )
    )
