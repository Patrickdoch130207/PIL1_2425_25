from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q, Max
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()



@login_required
def chat_room(request, room_name):
    search_query = request.GET.get('search', '') 
    users = User.objects.exclude(id=request.user.id) 
    chats = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=room_name)) |
        (Q(receiver=request.user) & Q(sender__username=room_name))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))  

    chats = chats.order_by('timestamp') 
    user_last_messages = []

    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    # Sort user_last_messages by the timestamp of the last_message in descending order
    user_last_messages.sort(
        key=lambda x: x['last_message'].timestamp if x['last_message'] else None,
        reverse=True
    )

    return render(request, 'chat.html', {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })



def get_user_info(request, username):
    user = User.objects.get(username=username)
    return JsonResponse({
       'email': user.email,
        'nom': user.nom,
        'prenom': user.prenom,
        })


@login_required
def user_search(request):
    q = request.GET.get('q', '')
    users = User.objects.filter(email__icontains=q).exclude(id=request.user.id)[:10]
    users = User.objects.filter(
    Q(email__icontains=q) | Q(nom__icontains=q) | Q(prenom__icontains=q)).exclude(id=request.user.id)[:10]
    results = [
        {"nom": u.nom, "prenom": u.prenom, "email": u.email}
        for u in users
    ]
    return JsonResponse({"results": results})


@login_required
def conversation_list(request):
    user = request.user
    # Récupère tous les utilisateurs avec qui j'ai échangé un message
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))
    # On veut la liste des correspondants uniques
    correspondants_ids = set()
    for msg in messages:
        if msg.sender != user:
            correspondants_ids.add(msg.sender.id)
        if msg.receiver != user:
            correspondants_ids.add(msg.receiver.id)
    correspondants = User.objects.filter(id__in=correspondants_ids)
    # Pour chaque correspondant, récupère le dernier message échangé
    conversations = []
    for correspondant in correspondants:
        last_message = Message.objects.filter(
            (Q(sender=user) & Q(receiver=correspondant)) |
            (Q(sender=correspondant) & Q(receiver=user))
        ).order_by('-timestamp').first()
        conversations.append({
            'user': correspondant,
            'last_message': last_message
        })
    # Trie par date du dernier message
    conversations.sort(key=lambda x: x['last_message'].timestamp if x['last_message'] else None, reverse=True)
    return render(request, "chat/conversation_list.html", {"conversations": conversations})

@login_required
def conversation_detail(request, email):
    user = request.user
    receiver = get_object_or_404(User, email=email)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(sender=user, receiver=receiver, content=content)
            return redirect('conversation_detail', email=receiver.email)
    messages = Message.objects.filter(
        (Q(sender=user) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=user))
    ).order_by('timestamp')
    return render(request, "chat/conversation_detail.html", {
        "receiver": receiver,
        "messages": messages,
        "user": user,
    })