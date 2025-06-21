<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::table('medical_images', function (Blueprint $table) {
            $table->string('grad_cam_url')->nullable()->after('ai_suggestions');
        });
    }

    public function down(): void
    {
        Schema::table('medical_images', function (Blueprint $table) {
            $table->dropColumn('grad_cam_url');
        });
    }
};
