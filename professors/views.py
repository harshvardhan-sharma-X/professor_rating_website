from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Avg 
import json
from .models import Professor, Rating
from rapidfuzz import process, fuzz 

# Create your views here.
def reviews_view(request):
    return render(request, 'reviews.html')

def rate_view(request):
    return render(request, 'rate.html')

@csrf_exempt  # For demo only; use CSRF tokens in production!
def login_view(request):
    if request.method == 'POST':
        vit_email = request.POST.get('vitEmail')
        reg_no = request.POST.get('registrationNumber')
        # Replace this with your actual authentication logic
        if vit_email == 'test@vitstudent.ac.in' and reg_no == '21BCE1234':
            return JsonResponse({'success': True, 'message': 'Verification successful! Redirecting to reviews...'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid VIT Email ID or Registration Number.'})
    return render(request, 'login.html')


@csrf_exempt
def submit_rating(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            teaching = int(data.get('teaching'))
            evaluation = int(data.get('evaluation'))
            behaviour = int(data.get('behaviour'))
            internals = int(data.get('internals'))

            if not all(1 <= rating <= 5 for rating in [teaching, evaluation, behaviour, internals]):
                return JsonResponse({'error' : 'All ratings must be between 1 and 5'}, status=400)

            professor, _ = Professor.objects.get_or_create(name=name)

            Rating.objects.create(
                professor = professor,
                teaching = teaching,
                evaluation = evaluation,
                behaviour = behaviour,
                internals = internals,
            ) 

            return JsonResponse({'message' : 'Rating submitted succesfully!'})
        
        except ValueError:
            return JsonResponse({'error' : 'Invalid rating values'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Invalid Request'}, status=400) 


def search_professors(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    all_names = list(Professor.objects.values_list('name', flat=True))
    # Using RapidFuzz for fuzzy matching
    matches = process.extract(query, all_names, scorer=fuzz.WRatio, limit=5, score_cutoff=75)

    suggestions = [name for name, score, _ in matches if score > 60] 

    return JsonResponse({'suggestions': suggestions}) 

def get_professor_ratings(request):
    name = request.GET.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Professor name is required'}, status=400)
    
    try:
        professor = Professor.objects.get(name=name)
        ratings = Rating.objects.filter(professor=professor)

        # Fixed: Changed 'exist()' to 'exists()'
        if not ratings.exists():
            return JsonResponse({'error': 'no ratings found for this professor'}, status=404)
        
        #cal_avg
        avg_ratings = ratings.aggregate(
            teaching = Avg('teaching'),
            evaluation = Avg('evaluation'),
            behaviour = Avg('behaviour'),
            internals = Avg('internals')
        )

        overall = (avg_ratings['teaching'] + avg_ratings['evaluation'] + avg_ratings['behaviour'] + avg_ratings['internals']) / 4

        return JsonResponse({
            'name' : professor.name,
            'total_ratings' : ratings.count(),
            'ratings': {
                'teaching' : round(avg_ratings['teaching'], 1),
                'evaluation' : round(avg_ratings['evaluation'], 1),
                'behaviour' : round(avg_ratings['behaviour'], 1),
                'internals' : round(avg_ratings['internals'], 1),
                'overall' : round(overall, 1)
            }
        })
    
    except Professor.DoesNotExist:
        return JsonResponse({'error' : 'Professor not found'}, status=404)


def get_all_professors(request):
    """Return all professors for dropdown menu"""
    try:
        professors = Professor.objects.all().values_list('name', flat=True).order_by('name')
        return JsonResponse({'professors': list(professors)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 
    

