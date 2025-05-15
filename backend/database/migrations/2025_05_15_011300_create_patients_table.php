<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('patients', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->integer('age')->unsigned(); // Возраст
            $table->decimal('weight', 8, 2)->nullable(); // Вес
            $table->string('gender'); // Пол: male, female, other
            $table->text('medical_history')->nullable(); // Медицинская история
            $table->unsignedBigInteger('owner_id'); // Добавляем owner_id
            $table->foreign('owner_id')->references('id')->on('users')->onDelete('cascade');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('patients');
    }
};
