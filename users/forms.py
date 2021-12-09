from django import forms
from users.models import Users


class UserRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = [
            "name",
            "email",
            "age",
            "gender",
            "country",
            "city",
        ]

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user
