from django.urls import path
from .views import LoginView, TutorSignupView, LearnerSignupView, CustomTokenRefreshView, TutorsListView, ProfileView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    path("signup/tutor/", TutorSignupView.as_view(), name="tutor-signup"),
    path("signup/learner/", LearnerSignupView.as_view(), name="learner-signup"),
    path("tutors", TutorsListView.as_view(), name="tutors-list"),
    path("profile/<str:username>/", ProfileView.as_view(), name="tutors-list"),
]
