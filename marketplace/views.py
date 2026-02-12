from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import UserProfile
from payments.models import Payment

from .models import Quest


@login_required
def client_dashboard(request: HttpRequest) -> HttpResponse:
    profile = UserProfile.objects.get(user=request.user)
    quests = Quest.objects.filter(client=request.user).order_by("-created_at")
    total_quests = quests.count()
    open_quests = quests.filter(status=Quest.STATUS_OPEN).count()
    in_progress = quests.filter(status=Quest.STATUS_ASSIGNED).count()
    completed = quests.filter(status__in=[Quest.STATUS_COMPLETED, Quest.STATUS_PAID]).count()
    return render(
        request,
        "marketplace/client_dashboard.html",
        {
            "profile": profile,
            "quests": quests,
            "total_quests": total_quests,
            "open_quests": open_quests,
            "in_progress": in_progress,
            "completed": completed,
        },
    )


@login_required
def worker_dashboard(request: HttpRequest) -> HttpResponse:
    profile = UserProfile.objects.get(user=request.user)
    assigned = Quest.objects.filter(worker=request.user).order_by("-created_at")
    open_quests = (
        Quest.objects.filter(status=Quest.STATUS_OPEN)
        .exclude(client=request.user)
        .order_by("-created_at")
    )
    return render(
        request,
        "marketplace/worker_dashboard.html",
        {
            "profile": profile,
            "assigned_quests": assigned,
            "open_quests": open_quests,
        },
    )


@login_required
def quest_list(request: HttpRequest) -> HttpResponse:
    qs = Quest.objects.filter(status=Quest.STATUS_OPEN).order_by("-created_at")
    q = request.GET.get("q")
    location = request.GET.get("location")
    service_type = request.GET.get("service_type")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if q:
        qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)
    if location:
        qs = qs.filter(location__icontains=location)
    if service_type:
        qs = qs.filter(service_type=service_type)
    if min_price:
        qs = qs.filter(price__gte=min_price)
    if max_price:
        qs = qs.filter(price__lte=max_price)

    return render(request, "marketplace/quest_list.html", {"quests": qs})


@login_required
def quest_create(request: HttpRequest) -> HttpResponse:
    profile = UserProfile.objects.get(user=request.user)
    if profile.role == UserProfile.ROLE_WORKER:
        return redirect("marketplace:worker_dashboard")
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price") or "0"
        location = request.POST.get("location", "")
        lat = request.POST.get("latitude")
        lon = request.POST.get("longitude")
        category = request.POST.get("category", "")
        service_type = request.POST.get("service_type")
        if title and description and service_type:
            Quest.objects.create(
                client=request.user,
                title=title,
                description=description,
                price=price,
                location=location,
                category=category,
                service_type=service_type,
                latitude=(float(lat) if lat else None),
                longitude=(float(lon) if lon else None),
            )
            return redirect("marketplace:client_dashboard")
    return render(request, "marketplace/quest_create.html")


@login_required
def quest_detail(request: HttpRequest, pk: int) -> HttpResponse:
    quest = get_object_or_404(Quest, pk=pk)
    profile = UserProfile.objects.get(user=request.user)
    can_accept = profile.role != UserProfile.ROLE_CLIENT and quest.can_be_accepted_by(
        profile
    )
    return render(
        request,
        "marketplace/quest_detail.html",
        {"quest": quest, "profile": profile, "can_accept": can_accept},
    )


@login_required
def accept_quest_api(request: HttpRequest, pk: int) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)
    quest = get_object_or_404(Quest, pk=pk)
    profile = UserProfile.objects.get(user=request.user)
    # Disallow accepting your own quest
    if quest.client == request.user:
        return JsonResponse({"error": "You cannot accept your own quest."}, status=400)
    if not quest.can_be_accepted_by(profile):
        return JsonResponse({"error": "You cannot accept this quest (service type, limits, or distance)."}, status=400)
    quest.worker = request.user
    quest.status = Quest.STATUS_ASSIGNED
    quest.save(update_fields=["worker", "status"])
    return JsonResponse(
        {
            "message": "Quest accepted.",
            "status": quest.status,
            "worker": request.user.username,
        }
    )


@login_required
def complete_quest_api(request: HttpRequest, pk: int) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)
    quest = get_object_or_404(Quest, pk=pk)
    if quest.worker != request.user:
        return JsonResponse({"error": "Only the assigned worker can complete."}, status=403)
    if quest.status != Quest.STATUS_ASSIGNED:
        return JsonResponse({"error": "Quest is not in an assignable state."}, status=400)
    quest.status = Quest.STATUS_COMPLETED
    quest.save(update_fields=["status"])
    # Grant EXP
    worker_profile = UserProfile.objects.get(user=request.user)
    worker_profile.add_exp_for_completed_quest()
    # Create payment record
    Payment.objects.get_or_create(
        quest=quest,
        defaults={
            "client": quest.client,
            "worker": quest.worker,
            "amount": quest.price,
        },
    )
    return JsonResponse(
        {
            "message": "Quest marked as completed.",
            "status": quest.status,
            "worker_exp": worker_profile.exp,
            "worker_rank": worker_profile.rank,
        }
    )


@login_required
def review_quest_api(request: HttpRequest, pk: int) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)
    quest = get_object_or_404(Quest, pk=pk)
    if quest.client != request.user:
        return JsonResponse({"error": "Only the client can review."}, status=403)
    if quest.status not in (Quest.STATUS_COMPLETED, Quest.STATUS_PAID):
        return JsonResponse({"error": "Quest must be completed before review."}, status=400)
    rating = int(request.POST.get("rating", 0))
    review = request.POST.get("review", "")
    if rating < 1 or rating > 5:
        return JsonResponse({"error": "Rating must be between 1 and 5."}, status=400)
    quest.rating = rating
    quest.review = review
    quest.save(update_fields=["rating", "review"])
    return JsonResponse(
        {"message": "Review submitted.", "rating": quest.rating, "review": quest.review}
    )

