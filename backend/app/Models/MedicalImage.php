<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Storage;

class MedicalImage extends Model
{
    use HasFactory;

    // image_types
    public const Xray = "x-ray";

    protected $fillable = [
        'patient_id',
        'image_url',
        'image_type',
        'capture_date',
        'diagnosis',
        'confidence_score',
        'detected_features',
        'ai_suggestions',
        'status'
    ];

    protected static function boot()
    {
        parent::boot();

        static::deleting(function ($model) {
            if (Storage::disk('public')->exists($model->image_url)) {
                Storage::disk('public')->delete($model->image_url);
            }
        });
    }

    public function patient()
    {
        return $this->belongsTo(Patient::class);
    }

    // Дополнительный метод для удобства
    public function getStatusIconClass()
    {
        return match ($this->status) {
            'confirmed' => 'text-green-500',
            'rejected' => 'text-red-500',
            default => 'text-yellow-500',
        };
    }

    public function getConfidenceColorClass()
    {
        if ($this->confidence_score >= 85) return 'text-green-600';
        if ($this->confidence_score >= 70) return 'text-yellow-600';
        return 'text-red-600';
    }

    public static function getImageTypeOptions()
    {
        return [
            "image_types" => [
                self::Xray,
            ]
        ];
    }
}
