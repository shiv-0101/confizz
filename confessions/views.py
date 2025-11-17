"""Views for handling confessions, comments, and user authentication with AI summarization."""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
import google.generativeai as genai
from django.conf import settings
from .models import Confession, Comment, Community
from .forms import ConfessionForm, CommentForm, SignUpForm, CommunityForm

@csrf_exempt
@require_POST
def summarize_comments(request, pk):
    """
    Summarizes comments for a given confession using the Gemini AI model.
    Expects a POST request with a JSON body containing 'comments_text'.
    """
    # Ensure the API key is configured in settings
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        return JsonResponse({'error': 'Gemini API key not configured. Please set GEMINI_API_KEY in your environment.'}, status=500)

    try:
        # Configure the Gemini client
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Get comments from the request
        data = json.loads(request.body)
        comments_text = data.get('comments_text', '')

        if not comments_text.strip():
            return JsonResponse({'error': 'No comments provided.'}, status=400)

        prompt = f"Please provide a concise, one-paragraph summary of the following user comments for a confession:\n\n---\n{comments_text}\n---"
        response = model.generate_content(prompt)

        # The response might be blocked for safety reasons. It's good practice to check.
        if response.parts:
            return JsonResponse({'summary': response.text})
        else:
            return JsonResponse({'error': 'The response from the AI was empty. This might be due to safety settings or an issue with the prompt.'}, status=500)
    except Exception as e:
        # A generic error handler for API or other issues
        return JsonResponse({'error': str(e)}, status=500)

def confession_list(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Confession.objects.create(content=content)  # Anonymous, no author
            messages.success(request, 'Your anonymous confession has been posted!')
            return redirect('confessions:confession_list')

    confessions = Confession.objects.all().order_by('-created_at')
    
    # Filter by search query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        confessions = confessions.filter(content__icontains=search_query)
    
    # Filter by date
    date_filter = request.GET.get('date_filter', '')
    if date_filter:
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()
        if date_filter == 'today':
            confessions = confessions.filter(created_at__date=now.date())
        elif date_filter == 'week':
            confessions = confessions.filter(created_at__gte=now - timedelta(days=7))
        elif date_filter == 'month':
            confessions = confessions.filter(created_at__gte=now - timedelta(days=30))
        elif date_filter == 'all':
            pass  # No additional filter
    
    comment_form = CommentForm()
    return render(request, 'confessions/confession_list.html', {
        'confessions': confessions,
        'comment_form': comment_form,
        'search_query': search_query,
        'date_filter': date_filter,
    })

@login_required
def user_dashboard(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Confession.objects.create(content=content, author=request.user)
            messages.success(request, 'Your confession has been posted!')
            return redirect('confessions:user_dashboard')
    
    user_confessions = Confession.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'confessions/user_dashboard.html', {
        'user_confessions': user_confessions,
    })

def add_comment(request, pk):
    confession = get_object_or_404(Confession, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.confession = confession
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()
            return redirect('confessions:confession_list')
    return redirect('confessions:confession_list')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('confessions:confession_list')
    else:
        form = SignUpForm()
    return render(request, 'confessions/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('confessions:confession_list')
    else:
        form = AuthenticationForm()
    return render(request, 'confessions/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect('confessions:confession_list')

def hello_world(request):
    return render(request, "confessions/helloworld.html")

def fizzzones(request):
    return render(request, 'confessions/fizzzones.html')

# Community Views

def community_list(request):
    """Display all communities with an option to create a new one."""
    communities = Community.objects.all().order_by('-created_at')
    return render(request, 'confessions/community_list.html', {
        'communities': communities,
    })

@login_required
def community_create(request):
    """Create a new community (login required)."""
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.save()
            messages.success(request, 'Community created successfully!')
            return redirect('confessions:community_detail', slug=community.slug)
    else:
        form = CommunityForm()
    return render(request, 'confessions/community_form.html', {'form': form})

def community_detail(request, slug):
    """Display community details and list confessions in that community."""
    community = get_object_or_404(Community, slug=slug)
    confessions = community.confessions.all().order_by('-created_at')
    comment_form = CommentForm()
    return render(request, 'confessions/community_detail.html', {
        'community': community,
        'confessions': confessions,
        'comment_form': comment_form,
    })

@login_required
def community_delete(request, slug):
    """Delete a community (only creator can delete)."""
    community = get_object_or_404(Community, slug=slug)
    
    # Check if the current user is the creator
    if community.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this community.')
        return redirect('confessions:community_detail', slug=slug)
    
    if request.method == 'POST':
        community.delete()
        messages.success(request, 'Community deleted successfully!')
        return redirect('confessions:community_list')
    
    return render(request, 'confessions/community_confirm_delete.html', {
        'community': community,
    })

