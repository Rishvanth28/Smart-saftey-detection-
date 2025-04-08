import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from ultralytics import YOLO

# Load YOLO model
model = YOLO(r"C:\Projects\Smart-saftey-detection-\ppe_proj\ppe_proj\yolo_model\best.pt")

@csrf_exempt
def detect_ppe(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']

        # Save original uploaded image
        os.makedirs("media", exist_ok=True)
        image_path = f"media/{uploaded_image.name}"
        with open(image_path, 'wb') as f:
            f.write(uploaded_image.read())

        # Run YOLO inference
        results = model(image_path)
        detected_classes = [model.names[int(box.cls[0])] for result in results for box in result.boxes]

        # Determine status
        status = "denied" if "not_helmet" in detected_classes or "not_reflectives" in detected_classes else "allowed"

        # Save detected image
        output_path = f"media/detected_{uploaded_image.name}"
        results[0].save(output_path)

        return JsonResponse({
            "status": status,
            "uploaded_image": image_path,
            "output_image": output_path
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

def upload_page(request):
    return render(request, 'upload.html')
