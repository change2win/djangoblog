from django import forms

class LoginForm(forms.Form):    
    username = forms.CharField(max_length = 150, label = "Kullanıcı Adı  ")
    password = forms.CharField(max_length = 128, label = "Şifre  ", widget = forms.PasswordInput)

class RegisterForm(forms.Form): 
    username = forms.CharField(max_length = 150, label = "Kullanıcı Adı  ")
    password = forms.CharField(max_length = 128, label = "Şifre  ", widget = forms.PasswordInput)
    confirm = forms.CharField(max_length = 128, label = "Şifreyi Onayla  ", widget = forms.PasswordInput)

    def clean(self):    
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and password != confirm:    
            raise forms.ValidationError("Şifre alanıyla eşleşmiyor.")

        values={
            "username":username,
            "password":password
        }

        return values
