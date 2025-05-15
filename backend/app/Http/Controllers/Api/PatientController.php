<?php

namespace App\Http\Controllers\Api;

use Illuminate\Http\Request;
use App\Models\Patient;
use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Auth;

class PatientController extends Controller
{
    public function index()
    {
        return Patient::where('owner_id', Auth::id())->get();
    }

    public function store(Request $request)
    {
        $validatedData = $request->validate([
            'name' => 'required|string|max:255',
            'age' => 'required|integer|min:0',
            'weight' => 'nullable|numeric|min:0',
            'gender' => 'required|string|in:male,female,other',
            'medical_history' => 'nullable|string',
        ]);

        $patient = Patient::create($validatedData);

        return response()->json($patient, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        $patient = Patient::find($id);

        if (!$patient) {
            return response()->json(['message' => 'patient not found'], 404);
        }
        return response()->json($patient);
    }
    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        // Найти пациента по ID
        $patient = Patient::find($id);

        // Если пациент не найден, вернуть ошибку 404
        if (!$patient) {
            return response()->json(['message' => 'Patient not found'], 404);
        }

        // Валидация входных данных
        $validatedData = $request->validate([
            'name' => 'sometimes|required|string|max:255',
            'age' => 'sometimes|required|integer|min:0',
            'weight' => 'nullable|numeric|min:0',
            'gender' => 'sometimes|required|string|in:male,female,other',
            'medical_history' => 'nullable|string',
        ]);

        // Обновление данных пациента
        $patient->update($validatedData);

        // Вернуть обновленного пациента
        return response()->json($patient, 200);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        //
    }
}
