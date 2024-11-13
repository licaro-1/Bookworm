from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from bookworm.settings import EMAIL_FEEDBACK_RECIPIENT
from feedback.forms import FeedbackCreationForm
from feedback.service import feedback_service
from feedback.models import Feedback
from logger.log import logger
from utils.email_sender import send_single_email


@login_required
def feedback_create(request):
    creation_form = FeedbackCreationForm(author=request.user)
    if request.method == "POST":
        logger.info(f"Received request for creating feedback")
        logger.info(f"Received POST data: {request.POST}")
        creation_form = FeedbackCreationForm(
            request.POST,
            request.FILES,
            author=request.user
        )
        if creation_form.is_valid():
            logger.info(f"Feedback form is valid, start creating feedback")
            feedback = creation_form.save()
            logger.info(f"Feedback created, {feedback=}")
            subject = (feedback.get_theme_display()
                       + f" от {feedback.author.email}"
                       + f" Идентификатор - {feedback.uuid}"
                       )
            send_single_email(
                subject=subject,
                message=feedback.text,
                send_to=EMAIL_FEEDBACK_RECIPIENT,
                file=request.FILES.get("file")
            )
            return redirect("feedback:feedback_created", uuid=feedback.uuid)
    context = {
        "feedback_creation_form": creation_form,
    }
    return render(request, "feedback/feedback_form.html", context)


@login_required
def feedback_created(request, uuid):
    feedback = feedback_service.get_feedback_by_uuid(uuid)
    if not feedback or feedback.author != request.user:
        raise Http404()
    context = {
        "feedback": feedback
    }
    return render(request, "feedback/feedback_created.html", context)
