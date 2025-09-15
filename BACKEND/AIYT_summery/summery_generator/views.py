from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
import json
import os
from openai import OpenAI, RateLimitError, AuthenticationError
from django.views.decorators.csrf import csrf_exempt
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re
from .models import BlogArticle
import logging
from gtts import gTTS
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__) 

# Create your views here.
@login_required
@never_cache
def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                return redirect('/')
            except:
                error_message = "error in creating user"
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            error_message = "Password do not match"
            return render(request, 'signup.html', {'error_message': error_message})
            
        
    return render(request, 'signup.html')   

def user_logout(request):
    logout(request)
    return redirect('/')

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        logger.error(f"Error getting transcript: {e}")
        return None

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            link = data.get('link')

            def get_video_id_from_url(url):
                """
                Extracts the YouTube video ID from a URL.
                Handles standard, shortened, and embed URLs.
                """
                video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
                return video_id_match.group(1) if video_id_match else None

            video_id = get_video_id_from_url(link)

            if not video_id:
                return JsonResponse({'error': 'Invalid YouTube link'}, status=400)
            transcript = get_transcript(video_id)

            if not transcript:
                return JsonResponse({'error': 'Could not retrieve a transcript for the video. Please check the video link and try again.'}, status=400)

            client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

            prompt = f"Please generate a blog post based on the following transcript:\n\n{transcript}"

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that writes blog posts."},
                        {"role": "user", "content": prompt}
                    ]
                )
                blog_post = response.choices[0].message.content
            except RateLimitError:
                logger.error("OpenAI API rate limit exceeded.")
                return JsonResponse({'error': 'API rate limit exceeded. Please try again later.'}, status=429)
            except AuthenticationError:
                logger.error("OpenAI API authentication error.")
                return JsonResponse({'error': 'API authentication error. Please check your API key.'}, status=401)
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                return JsonResponse({'error': 'An error occurred with the AI service. Please try again later.'}, status=500)

            try:
                tts = gTTS(blog_post)
                audio_file = ContentFile(b"")
                tts.write_to_fp(audio_file)
                
                blog_article = BlogArticle.objects.create(
                    user=request.user,
                    youtube_title="Generated Blog Post",  # You might want to get the real title
                    youtube_link=link,
                    generated_content=blog_post
                )
                blog_article.audio_file.save(f"{video_id}.mp3", audio_file)
            except Exception as e:
                logger.error(f"Database error: {e}")
                return JsonResponse({'error': 'An error occurred while saving the blog post.'}, status=500)
            
            return JsonResponse({'content': blog_post})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def blog_list(request):
    blog_articles = BlogArticle.objects.filter(user=request.user)
    return render(request, 'all_summary.html', {'blog_articles': blog_articles})

@login_required
def blog_details(request, pk):
    try:
        blog_article_detail = BlogArticle.objects.get(pk=pk, user=request.user)
    except BlogArticle.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'summary-details.html', {'blog_article_detail': blog_article_detail})

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)
