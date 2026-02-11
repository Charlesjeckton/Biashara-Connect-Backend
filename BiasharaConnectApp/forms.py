from django import forms
import cloudinary.uploader
from .models import SellerProfile, Listing, ListingImage


# =========================
# Seller Profile Form
# =========================
class SellerProfileForm(forms.ModelForm):
    upload_profile_image = forms.ImageField(required=False, label="Upload Profile Image")

    class Meta:
        model = SellerProfile
        fields = [
            "business_name",
            "business_type",
            "business_category",
            "business_location",
            "bio",
            "upload_profile_image",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get("upload_profile_image")
        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="BiasharaConnect/profile_image",
                quality="auto",
                fetch_format="auto",
            )
            instance.profile_image = upload_result.get("secure_url")
        if commit:
            instance.save()
        return instance


# =========================
# Listing Form
# =========================
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "price",
            "category",
            "condition",
            "location",
            "area",
        ]


# =========================
# Listing Image Form
# =========================
class ListingImageForm(forms.ModelForm):
    upload_image = forms.ImageField(required=True, label="Upload Listing Image")

    class Meta:
        model = ListingImage
        fields = ["upload_image", "is_primary"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get("upload_image")
        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="BiasharaConnect/listing",
                quality="auto",
                fetch_format="auto",
            )
            instance.image = upload_result.get("secure_url")
        if commit:
            instance.save()
        return instance
