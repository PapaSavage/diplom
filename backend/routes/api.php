<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\Auth\AuthController;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

Route::post('/register', [AuthController::class, 'register']);


Route::post('/login', [AuthController::class, 'login']);

// Route::post('/logout', [AuthController::class, 'logout']);
Route::post('/logout', [AuthController::class, 'logout'])->middleware('auth:sanctum');
// Route::middleware('auth:sanctum')->group(function () {
//     Route::post('/create-order', [OrderCreatingController::class, 'store']);

//     Route::apiResources([
//         '/pizzas' => PizzaController::class,
//         '/categories' => PizzaCategoriesController::class,
//         '/clients' => ClientsController::class,
//         '/orders' => OrdersController::class,
//     ]);
// });
