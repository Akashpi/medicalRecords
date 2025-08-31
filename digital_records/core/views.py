from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RecordForm
from .models import Record
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    records = Record.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'records': records})

@login_required
def upload_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return render(request, 'upload.html', {'form': form, 'success': 'Record uploaded successfully!'})
    else:
        form = RecordForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def records(request):
    records = Record.objects.filter(user=request.user)
    return render(request, 'records.html', {'records': records})


@csrf_exempt
def ai_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
        try:
            resp = requests.post(api_url, headers=headers, json=payload, timeout=15)
            print("Status code:", resp.status_code)
            print("Response:", resp.text)
            resp.raise_for_status()
            ai_reply = resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("DeepSeek error:", e)
            ai_reply = "Sorry, I couldn't process your request."
        return JsonResponse({"reply": ai_reply})
    # Always return a response for non-POST requests
    return JsonResponse({"reply": "Invalid request."}, status=400)