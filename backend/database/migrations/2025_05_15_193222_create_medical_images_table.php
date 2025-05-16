<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('medical_images', function (Blueprint $table) {
            $table->id();
            $table->foreignId('patient_id')->constrained()->onDelete('cascade');
            $table->string('image_url'); // путь к изображению
            $table->string('image_type'); // тип исследования (Рентген, МРТ и т.д.)
            $table->date('capture_date'); // дата съемки
            $table->string('diagnosis')->nullable(); // диагноз
            $table->json('confidence_score')->nullable(); // уверенность ИИ в процентах
            $table->json('detected_features')->nullable(); // обнаруженные признаки
            $table->json('ai_suggestions')->nullable(); // рекомендации ИИ
            $table->string('status')->default('pending'); // статус диагностики (pending, confirmed, rejected)
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('medical_images');
    }
};
