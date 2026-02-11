from django import forms
import cloudinary.uploader
from .models import (
    User,
    BuyerProfile,
    SellerProfile,
    Listing,
    ListingImage,
    SavedListing,
)


# =========================
# Buyer Registration Form
# =========================
class BuyerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


# =========================
# Seller Registration Form
# =========================
class SellerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    upload_profile_image = forms.ImageField(required=False, label="Upload Profile Image")

    class Meta:
        model = SellerProfile
        fields = [
            'business_name', 'business_type', 'business_category',
            'business_location', 'bio', 'upload_profile_image'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get("upload_profile_image")
        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="biashara/sellers",
                quality="auto",
                fetch_format="auto",
            )
            instance.profile_image_url = upload_result.get("secure_url")
        if commit and user:
            instance.user = user
            instance.save()
        return instance


# =========================
# Listing Form
# =========================
class ListingForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        label="Upload Images"
    )

    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'category', 'condition', 'location', 'area', 'images']

    def save(self, commit=True, seller=None):
        instance = super().save(commit=False)
        if commit and seller:
            instance.seller = seller
            instance.save()
        image_files = self.files.getlist('images')
        for image_file in image_files:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="biashara/listings",
                quality="auto",
                fetch_format="auto",
            )
            ListingImage.objects.create(
                listing=instance,
                image_url=upload_result.get("secure_url")
            )
        return instance


# =========================
# Saved Listing Form
# =========================
class SavedListingForm(forms.ModelForm):
    class Meta:
        model = SavedListing
        fields = ['listing']

    def save(self, commit=True, buyer=None):
        instance = super().save(commit=False)
        if buyer:
            instance.buyer = buyer
        if commit:
            instance.save()
        return instance