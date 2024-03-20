from userauths.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import shortuuid
from django.conf import settings
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from userauths.serializers import (
    UserSerializer,
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


def generate_otp(length=7):
    uuid_key = shortuuid.uuid()
    unique_key = uuid_key[:length]
    return unique_key


class PasswordResetEmailVerifyView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        if user:
            user.otp = generate_otp()
            user.save()

            uidb64 = user.pk
            otp = user.otp

            link = "http://localhost:3000/password-create?"
            link += f"uidb64={uidb64}&otp={otp}/"
            ctx = {
                "link": link,
                "username": user.username,
            }

            subject = "Password Reset Request"
            text_body = render_to_string("email/password_reset.txt", ctx)
            html_body = render_to_string("email/password_reset.html", ctx)

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[user.email],
                body=text_body,
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
        return user


class PasswordChangeView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        payload = request.data

        otp = payload["otp"]
        uidb64 = payload["uidb64"]
        password = payload["password"]

        user = User.objects.get(id=uidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.reset_token = ""
            user.save()

            return Response(
                {"message": "Password Changed Successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "An Error Occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
