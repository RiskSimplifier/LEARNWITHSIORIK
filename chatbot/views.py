from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from SiorikLearn.settings import *
from openai import OpenAI
import openai
from chatbot.models import Chat
from django.utils import timezone



client = OpenAI(
    # This is the default and can be omitted
    api_key=openai_api_key,
)

# Create your views here.
def ask_openai(message):

    response =  client.chat.completions.create(
    model="gpt-3.5-turbo", #this is where you put model
    
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
        
    )

    answer = response.choices[0].message.content.strip()
    return answer


@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot/chatbot.html', {'chats': chats})



