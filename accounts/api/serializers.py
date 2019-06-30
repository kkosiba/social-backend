from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer, UserDetailsSerializer

try:
    from allauth.utils import email_address_exists
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"})


class CustomRegisterSerializer(serializers.Serializer):
    """
    Modified RegisterSerializer class from rest_auth
    """

    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(
                "A user is already registered with this e-mail address."
            )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def get_cleaned_data(self):
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user


# Profiles
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """Custom user detail serializer with profile information"""

    picture = serializers.CharField(source="profile.picture", allow_null=True)
    date_of_birth = serializers.DateField(
        source="profile.date_of_birth", allow_null=True
    )
    bio = serializers.CharField(source="profile.bio", allow_blank=True)
    website = serializers.CharField(source="profile.website", allow_blank=True)
    location = serializers.CharField(source="profile.location", allow_blank=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "picture",
            "date_of_birth",
            "bio",
            "website",
            "location",
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})

        picture = profile_data.get("picture")
        date_of_birth = profile_data.get("date_of_birth")
        bio = profile_data.get("bio")
        website = profile_data.get("website")
        location = profile_data.get("location")

        instance = super().update(instance, validated_data)

        # get and update user profile
        profile = instance.profile
        if profile_data:
            profile.picture = picture
            profile.date_of_birth = date_of_birth
            profile.bio = bio
            profile.website = website
            profile.location = location
            profile.save()
        return instance
