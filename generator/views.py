import torch
from diffusers import DiffusionPipeline
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

# --- 1. Load the AI model ---
# This is loaded once when the server starts.
print("Loading Stable Diffusion model...")
pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)

# Move the model to GPU if available, otherwise CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)
print(f"Model loaded on {device}.")


# --- 2. Create Views ---

def index(request):
    """Serves the main HTML page."""
    return render(request, 'index.html')


@csrf_exempt  # For simplicity in this example; use proper CSRF handling in production
def generate_image(request):
    """
    Generates an image based on a text prompt from a POST request.
    """
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        print(f"Generating image for prompt: {prompt}")

        image = pipe(prompt).images[0]

        image_path = "static/generated_image.png"
        image.save(image_path)

        return JsonResponse({'image_url': f'/{image_path}'})
    return JsonResponse({'error': 'Invalid request'}, status=400)