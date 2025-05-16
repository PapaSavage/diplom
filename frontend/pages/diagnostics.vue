<template>
  <div class="grid grid-cols-4 gap-4">
    <div class="col-span-4 md:col-span-2">
      <patients-list
        :global="false"
        :from="'diagnostics'"
        @patient-selected="onPatientSelected"
      />
    </div>
    <div class="col-span-4 md:col-span-2" v-if="selectedPatient">
      <Card class="w-full">
        <CardHeader>
          <CardTitle>Медицинские обследования</CardTitle>
          <CardDescription
            >Диагностическая информация для пациента
            <br />
            <strong>
              {{ selectedPatient.name }}
            </strong>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Загрузить изображение
            </label>
            <div
              class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-gray-400 transition-colors"
              @click="$refs.fileInput.click()"
              @dragover.prevent="onDragOver"
              @dragleave.prevent="onDragLeave"
              @drop.prevent="onDrop"
              :class="{ 'border-blue-500 bg-blue-50': isDragging }"
            >
              <input
                type="file"
                ref="fileInput"
                class="hidden"
                accept="image/*"
                @change="handleImageUpload"
              />
              <div
                class="mx-auto h-12 w-12 text-gray-400 flex items-center justify-center rounded-full bg-gray-100"
              >
                <PlusCircle size="24" />
              </div>
              <p class="mt-2 text-sm text-gray-500">
                Перетащите файл сюда или нажмите, чтобы выбрать
              </p>
              <p class="mt-1 text-xs text-gray-400">PNG, JPG до 10MB</p>

              <!-- Информация о загруженном файле -->
              <div v-if="uploadedFile" class="mt-4 text-left">
                <div class="flex justify-between text-sm text-gray-800">
                  <span>Имя файла:</span>
                  <span>{{ uploadedFile.name }}</span>
                </div>
                <div class="flex justify-between text-sm text-gray-800">
                  <span>Размер:</span>
                  <span>{{ formatFileSize(uploadedFile.size) }}</span>
                </div>
                <div class="flex justify-between text-sm text-gray-800">
                  <span>Тип:</span>
                  <span>{{ uploadedFile.type || "Неизвестный тип" }}</span>
                </div>
              </div>
            </div>

            <!-- Превью загруженного изображения -->
            <div v-if="imagePreviewUrl" class="mt-4">
              <h4 class="text-sm font-medium text-gray-700 mb-2">
                Превью изображения:
              </h4>
              <div class="w-full max-w-md mx-auto">
                <img
                  :src="imagePreviewUrl"
                  alt="Предварительный просмотр"
                  class="w-full h-auto rounded-lg shadow-sm"
                />
              </div>
            </div>
          </div>

          <div
            class="flex justify-center items-center min-h-16"
            v-if="isDiagnosticsLoading"
          >
            <div
              class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"
            ></div>
          </div>

          <div v-else-if="diagnosticResults.length == 0">
            <div class="bg-white rounded-lg shadow-sm p-6 text-center">
              <h3 class="text-lg font-medium text-gray-900 mb-2">
                Вы ещё не производили диагностику
              </h3>
              <p class="text-gray-500">
                Загрузите изображение и запустите диагностику
              </p>
            </div>
          </div>
          <div v-else-if="selectedImage != null">
            <div
              class="px-6 py-4 border-b border-gray-200 flex justify-between items-center"
            >
              <div>
                <h2 class="text-lg font-medium text-gray-900">
                  Диагностическая информация
                </h2>
                <p class="mt-1 text-sm text-gray-500">
                  Изображение: ({{
                    new Date(selectedImage.captureDate).toLocaleDateString(
                      "ru-RU"
                    )
                  }})
                </p>
              </div>
              <div v-if="diagnosis" class="flex items-center space-x-1">
                <component
                  :is="getStatusIcon(diagnosis.status)"
                  size="18"
                  :class="{
                    'text-green-500': diagnosis.status === 'confirmed',
                    'text-red-500': diagnosis.status === 'rejected',
                    'text-yellow-500': true,
                  }"
                />
                <span class="text-sm font-medium">{{
                  getStatusText(diagnosis.status)
                }}</span>
              </div>
            </div>
            <div class="p-6">
              <div v-if="diagnosis" class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div
                    v-if="selectedImage"
                    class="relative h-64 bg-gray-100 rounded-lg overflow-hidden"
                  >
                    <img
                      :src="selectedImage.imageUrl"
                      :alt="`${selectedImage.bodyPart} - ${selectedImage.imageType}`"
                      class="w-full h-full object-contain"
                    />
                  </div>
                  <div class="space-y-4">
                    <div>
                      <h3 class="text-lg font-medium text-gray-900">Диагноз</h3>
                      <p class="mt-1 text-xl font-semibold text-[#0070C0]">
                        {{ diagnosis.condition }}
                      </p>
                    </div>
                    <div>
                      <div class="flex items-center justify-between">
                        <h4 class="text-sm font-medium text-gray-500">
                          Достоверность диагноза
                        </h4>
                        <span
                          :class="getConfidenceColor(diagnosis.confidenceScore)"
                          class="text-lg font-bold"
                        >
                          {{ diagnosis.confidenceScore }}%
                        </span>
                      </div>
                      <div
                        class="mt-2 h-2 bg-gray-200 rounded-full overflow-hidden"
                      >
                        <div
                          :class="{
                            'bg-green-500': diagnosis.confidenceScore >= 85,
                            'bg-yellow-500': diagnosis.confidenceScore >= 70,
                            'bg-red-500': true,
                          }"
                          class="h-full"
                          :style="{ width: `${diagnosis.confidenceScore}%` }"
                        ></div>
                      </div>
                    </div>
                    <div>
                      <h4 class="text-sm font-medium text-gray-500">
                        Обнаруженные признаки
                      </h4>
                      <ul class="mt-2 space-y-1">
                        <li
                          v-for="(feature, index) in diagnosis.detectedFeatures"
                          :key="index"
                          class="flex items-start"
                        >
                          <span class="text-[#0070C0] mr-2">•</span>
                          <span class="text-sm text-gray-700">{{
                            feature
                          }}</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
                <div>
                  <h3 class="text-lg font-medium text-gray-900 mb-3">
                    ИИ предлагает рассмотреть
                  </h3>
                  <div
                    class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
                  >
                    <div
                      v-for="(suggestion, index) in diagnosis.aiSuggestions"
                      :key="index"
                      class="bg-gray-50 p-3 rounded-lg border border-gray-200"
                    >
                      <p class="text-sm font-medium text-gray-900">
                        {{ suggestion }}
                      </p>
                      <div class="mt-2 flex items-center">
                        <span
                          class="inline-block h-2 w-2 rounded-full mr-2"
                          :class="{
                            'bg-green-500': index === 0,
                            'bg-yellow-500': index === 1,
                            'bg-red-500': index === 2,
                          }"
                        ></span>
                        <span class="text-xs text-gray-500">
                          {{
                            index === 0
                              ? "Высокая вероятность"
                              : index === 1
                              ? "Средняя вероятность"
                              : "Низкая вероятность"
                          }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-if="similarCases.length > 0">
                  <h3 class="text-lg font-medium text-gray-900 mb-3">
                    Похожие случаи
                  </h3>
                  <div
                    class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
                  >
                    <div
                      v-for="scase in similarCases"
                      :key="scase.id"
                      class="border border-gray-200 rounded-lg overflow-hidden"
                    >
                      <div class="h-36 bg-gray-100">
                        <img
                          :src="scase.imageUrl"
                          :alt="scase.condition"
                          class="w-full h-full object-cover"
                        />
                      </div>
                      <div class="p-3">
                        <p class="text-sm font-medium text-gray-900">
                          {{ scase.condition }}
                        </p>
                        <div class="mt-2 flex items-center justify-between">
                          <div class="flex items-center">
                            <Award size="16" class="text-[#0070C0] mr-1" />
                            <span class="text-xs text-gray-500"
                              >Совпадение: {{ scase.matchScore }}%</span
                            >
                          </div>
                          <span
                            class="text-xs font-medium"
                            :class="getConfidenceColor(scase.confidenceScore)"
                          >
                            {{ scase.confidenceScore }}% уверенность
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else>
                <div class="text-center py-10">
                  <div
                    class="mx-auto h-12 w-12 text-gray-400 flex items-center justify-center rounded-full bg-gray-100"
                  >
                    <AlertCircle size="24" />
                  </div>
                  <h3 class="mt-2 text-sm font-medium text-gray-900">
                    Нет диагностической информации
                  </h3>
                  <p class="mt-1 text-sm text-gray-500">
                    Для выбранного изображения нет диагностической информации.
                  </p>
                  <div class="mt-6">
                    <button
                      type="button"
                      class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-[#0070C0] hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#0070C0]"
                    >
                      Провести анализ изображения
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div
              v-if="diagnosis"
              class="px-6 py-4 border-t border-gray-200 flex justify-end space-x-4"
            >
              <button
                type="button"
                class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#0070C0]"
              >
                Редактировать
              </button>
              <button
                type="button"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-[#00A99D] hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#00A99D]"
              >
                Сохранить в карте пациента
              </button>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button
            type="submit"
            class="w-full mt-4"
            :disabled="isDiagnosticsUploadProccessingLoading"
            @click="newDiagnostic"
          >
            <span v-if="!isDiagnosticsUploadProccessingLoading">
              Прозвести новое обследование
            </span>

            <div
              v-else
              class="animate-spin rounded-full h-5 w-5 border-b-2 border-secondary"
            ></div>
          </Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import PatientsList from "@/components/PatientsList";
import {
  CheckCircle,
  AlertCircle,
  HelpCircle,
  Award,
  PlusCircle,
} from "lucide-vue-next";
import { toast } from "vue-sonner";

definePageMeta({
  layout: "admin",
});

const selectedPatient = ref(null);
const diagnosticResults = ref([]);
const selectedImage = ref(null);
const similarCases = ref([]);

const isLoading = ref(false);
const isDiagnosticsLoading = ref(false);
const isDiagnosticsUploadProccessingLoading = ref(false);

const fileInput = ref(null);

const isDragging = ref(false);
const uploadedFile = ref(null);

const imagePreviewUrl = ref(null);

const filters = ref(null);

const { $api } = useNuxtApp();

async function onPatientSelected(patient) {
  if (selectedPatient.value?.id === patient.id) return;
  selectedPatient.value = patient;
  await fetchDiagnostics();
}

// const diagnosis = computed(() => {
//   if (!selectedImage.value) return null;
//   return diagnosticResults.value.find(
//     (d) => d.imageId === selectedImage.value.id
//   );
// });

async function fetchDiagnostics() {
  isDiagnosticsLoading.value = true;
  const id = selectedPatient.value.id;
  try {
    const response = await $api(`/medical-images/${id}`, {
      method: "GET",
    });

    diagnosticResults.value = response;
  } catch (error) {
    console.error("Ошибка при получении пациентов:", error);
  } finally {
    isDiagnosticsLoading.value = false;
  }
}

function getStatusIcon(status) {
  switch (status) {
    case "confirmed":
      return CheckCircle;
    case "rejected":
      return AlertCircle;
    default:
      return HelpCircle;
  }
}

function getStatusText(status) {
  switch (status) {
    case "confirmed":
      return "Подтверждён";
    case "rejected":
      return "Отклонён";
    default:
      return "Ожидает подтверждения";
  }
}

function getConfidenceColor(score) {
  if (score >= 85) return "text-green-600";
  if (score >= 70) return "text-yellow-600";
  return "text-red-600";
}

function onDragOver() {
  isDragging.value = true;
}

function onDragLeave() {
  isDragging.value = false;
}

function onDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) {
    handleImageUpload({ target: { files: [file] } });
  }
}

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (file && file.type.startsWith("image/")) {
    uploadedFile.value = file;
    imagePreviewUrl.value = URL.createObjectURL(file);
    console.log("Загруженный файл:", file);
    // Здесь можно добавить логику отправки файла на сервер
  } else {
    alert("Пожалуйста, загрузите только изображения (JPG, PNG).");
  }
}

async function newDiagnostic() {
  if (!uploadedFile.value || !selectedPatient.value) {
    toast.error("Выберите файл и пациента");
    return;
  }

  const formData = new FormData();
  formData.append("image", uploadedFile.value);
  formData.append("image_type", "x-ray");

  isDiagnosticsUploadProccessingLoading.value = true;

  try {
    const response = await $api(
      `/patients/${selectedPatient.value.id}/diagnostics`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (response.status === 201 && response.data) {
      await fetchDiagnostics(); // Обновление списка диагностик
      toast.success("Диагностика отправлена на обработку");
    } else {
      toast.warning("Сохранено, но ожидается результат AI");
    }
  } catch (error) {
    console.error("Ошибка при отправке диагностики:", error);
    toast.error("Не удалось отправить диагностику");
  } finally {
    isDiagnosticsUploadProccessingLoading.value = false;
  }
}

async function getFilters() {
  try {
    const response = await $api(`/medical-images/filters`, {
      method: "GET",
    });

    filters = response;
  } catch (error) {}
}

// Форматирование размера файла
function formatFileSize(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

onMounted(() => {
  getFilters();
});
</script>
