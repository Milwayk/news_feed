from django import forms
from feed.models import Comments, News


class NewsForm(forms.Form):
    header = forms.CharField(label='Заголовок')
    theme = forms.CharField(label='Тема')
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Напишите свой текст'}))

    def save(self, user):
        News(
            author=user, 
             header=self.cleaned_data['header'],
            content=self.cleaned_data['content'],
            ).save()

class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Напишите свой комментарий', 'class': 'add-comment-input-anyline'}))

    def save(self, news_id, user):
        Comments(
            author=user,
            comment=self.cleaned_data['comment'],
            news_id=news_id,
            ).save()