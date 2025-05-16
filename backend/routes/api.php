<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\Auth\AuthController;
use App\Http\Controllers\Api\PatientController;
use App\Http\Controllers\Api\MedicalImageController;

// Public routes
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

// Authenticated routes
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', function (Request $request) {
        return $request->user();
    });

    Route::post('/logout', [AuthController::class, 'logout']);

    // Resource routes
    Route::apiResource('patients', PatientController::class);
    Route::apiResource('medical-images', MedicalImageController::class);

    // Custom diagnostic route for a patient
    Route::post('patients/{patientId}/diagnostics', [MedicalImageController::class, 'store']);
    Route::get('medical-images/filters', [MedicalImageController::class, 'filters']);
});
