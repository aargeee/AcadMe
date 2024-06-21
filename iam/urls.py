from django.urls import path
from .views import LoginView, TutorSignupView, LearnerSignupView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/tutor/", TutorSignupView.as_view(), name="tutor-signup"),
    path("signup/learner/", LearnerSignupView.as_view(), name="learner-signup"),
]
