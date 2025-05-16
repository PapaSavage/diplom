<?php

namespace App\Http\Controllers\Api;

use App\Models\Patient;
use App\Models\MedicalImage;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Http;
use App\Http\Controllers\Controller;
use GuzzleHttp\Client;
use Illuminate\Support\Facades\Storage;

class MedicalImageController extends Controller
{
    public function show($patientId)
    {
        $patient = Patient::with('medicalImages')->find($patientId);
        $images = $patient->medicalImages;

        return response()->json(
            $images
        );
    }

    public function store(Request $request, $patientId)
    {
        $validated = $request->validate([
            'image' => 'required|image|mimes:jpeg,png,jpg|max:2048',
            'image_type' => 'required|string',
        ]);

        $patient = Patient::findOrFail($patientId);

        $path = $request->file('image')->store('images', 'public');
        $url = 'images/' . $request->file('image')->hashName();

        // Затем читаем файл через Storage:
        $contents = Storage::disk('public')->get($url);

        $image = $patient->medicalImages()->create([
            'image_url' => $url,
            'image_type' => $validated['image_type'],
            'capture_date' => now(),
            'status' => 'processing',
        ]);

        $client = new Client();

        try {
            $response = $client->post('http://127.0.0.1:9010/diagnosis', [
                'multipart' => [
                    [
                        'name' => 'file',
                        'contents' => $contents,
                        'filename' => $url,
                    ],
                ],
            ]);

            $result = json_decode($response->getBody(), true);

            $image->update([
                'diagnosis' => $result['predicted_class'] ?? null,
                'confidence_score' => $result['probability'] ?? 0,
                'detected_features' => [$result['predicted_class'] ?? 'unknown'],
                'ai_suggestions' => [($result['predicted_class'] ?? 'unknown')],
                'status' => 'completed',
            ]);
        } catch (\Exception $e) {
            // \Log::error("FastAPI Error: " . $e->getMessage());
            // $image->update(['status' => 'failed']);
        }

        return response()->json($image, 201);
    }

    public function update(Request $request, $patientId, $imageId)
    {
        $request->validate([
            'diagnosis' => 'nullable|string',
            'confidence_score' => 'nullable|numeric|min:0|max:100',
            'detected_features' => 'nullable|array',
            'ai_suggestions' => 'nullable|array',
            'status' => 'nullable|string|in:pending,confirmed,rejected',
        ]);

        $patient = Patient::findOrFail($patientId);
        $image = $patient->images()->findOrFail($imageId);

        $image->update($request->only([
            'diagnosis',
            'confidence_score',
            'detected_features',
            'ai_suggestions',
            'status'
        ]));

        return response()->json($image);
    }

    public function destroy($patientId, $imageId)
    {
        $patient = Patient::findOrFail($patientId);
        $image = $patient->images()->findOrFail($imageId);
        $image->delete();

        return response()->json(['message' => 'Image deleted successfully'], 200);
    }

    public function getFilters()
    {
        return response()->json(MedicalImage::getImageTypeOptions(), 201);
    }
}
