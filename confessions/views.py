import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from decouple import config
import google.generativeai as genai

@csrf_exempt
@require_POST
def summarize_comments(request, pk):
    """
    Summarizes comments for a given confession using the Gemini AI model.
    Expects a POST request with a JSON body containing 'comments_text'.
    """
    # Ensure the API key is configured in settings
    api_key = config('GEMINI_API_KEY', default=None)
    if not api_key:
        return JsonResponse({'error': 'Gemini API key not configured.'}, status=500)

    try:
        # Configure the Gemini client
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

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

def hello_world(request):
    return render(request, "confessions/helloworld.html")
