<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Storage;

class MedicalImage extends Model
{
    use HasFactory;

    // image_types
    public const Xray = "Рентген лёгких";

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

    protected $appends = ['status_icon_class', 'score', 'bg_score'];

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

    public function getScoreAttribute()
    {
        $rawConfidence = $this->attributes['confidence_score'];

        // Если данные уже являются массивом — используем их напрямую
        if (is_array($rawConfidence)) {
            return max(array_values($rawConfidence));
        }

        // Проверяем, что поле не пустое и является строкой
        if (!is_string($rawConfidence) || empty($rawConfidence)) {
            return null; // или 0, или любое другое значение по умолчанию
        }

        // Декодируем JSON
        $confidence = json_decode($rawConfidence, true);

        // Проверяем успешность декодирования и тип результата
        if (json_last_error() !== JSON_ERROR_NONE || !is_array($confidence)) {
            return null;
        }

        // Возвращаем максимальное значение из массива
        return max(array_values($confidence));
    }

    public function getBgScoreAttribute()
    {
        if ($this->score >= 85) {
            return 'bg-green-500';
        } elseif ($this->score >= 70) {
            return 'bg-yellow-500';
        } else {
            return 'bg-red-500';
        }
    }

    // Дополнительный метод для удобства
    public function getStatusIconClassAttribute()
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
                ["id" => 1, "name" => self::Xray,]
            ]
        ];
    }
}
