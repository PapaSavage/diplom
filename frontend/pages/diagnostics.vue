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
            <div class="my-4">
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Тип обследования</label
              >
              <Select v-model="selectedImageType">
                <SelectTrigger class="w-full">
                  <SelectValue placeholder="Выберите тип обследования" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem
                    v-for="type in filters?.image_types"
                    :key="type.id"
                    :value="type.name"
                    >{{ type.name }}</SelectItem
                  >
                </SelectContent>
              </Select>
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

          <div v-if="diagnosticResults.length == 0">
            <div class="bg-white rounded-lg shadow-sm p-6 text-center">
              <h3 class="text-lg font-medium text-gray-900 mb-2">
                Вы ещё не производили диагностику
              </h3>
              <p class="text-gray-500">
                Загрузите изображение и запустите диагностику
              </p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4 p-4 sm:grid-cols-3" v-else>
            <div
              v-for="diagnosticResult in diagnosticResults"
              @click="handleDiagnosticResultSelect(diagnosticResult)"
              :key="diagnosticResult.id"
              class="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow duration-200 cursor-pointer"
            >
              <div
                class="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow duration-200 cursor-pointer"
              >
                <div class="relative h-48 bg-gray-100">
                  <img
                    :src="publicUrl + diagnosticResult.image_url"
                    class="w-full h-full object-cover"
                  />
                  <div
                    class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-3"
                  >
                    <span class="text-white text-sm font-medium">{{
                      diagnosticResult.image_type
                    }}</span>
                  </div>
                  <div
                    class="absolute top-2 right-2 bg-[#0070C0] text-white text-xs rounded-full px-2 py-1"
                  >
                    {{ diagnosticResult.image_type }}
                  </div>
                </div>
                <div class="p-3">
                  <div class="flex items-center text-sm text-gray-500 mb-1">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="14"
                      height="14"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="lucide lucide-calendar mr-1"
                    >
                      <path d="M8 2v4"></path>
                      <path d="M16 2v4"></path>
                      <rect width="18" height="18" x="3" y="4" rx="2"></rect>
                      <path d="M3 10h18"></path></svg
                    ><span>{{ diagnosticResult.capture_date }}</span>
                  </div>

                  <div class="mt-2 flex justify-end">
                    <button
                      class="text-[#0070C0] hover:text-blue-700 inline-flex items-center text-sm"
                    >
                      Подробнее<svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="lucide lucide-chevron-right ml-1"
                      >
                        <path d="m9 18 6-6-6-6"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
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
    <!-- <div class="col-span-2"></div> -->
    <div class="col-span-4" v-if="selectedDiagnostic">
      <Card class="w-full">
        <CardHeader>
          <CardTitle>Диагностическая информация</CardTitle>
          <CardDescription
            >Изображение: ({{
              new Date(selectedDiagnostic.capture_date).toLocaleDateString(
                "ru-RU"
              )
            }})
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div>
            <div class="p-6">
              <div class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div class="relative bg-gray-100 rounded-lg overflow-hidden">
                    <img
                      :src="publicUrl + selectedDiagnostic.image_url"
                      class="w-full h-full object-contain"
                    />
                  </div>
                  <div class="space-y-4">
                    <div>
                      <h3 class="text-lg font-medium text-gray-900">Диагноз</h3>
                      <p class="mt-1 text-xl font-semibold text-[#0070C0]">
                        {{ selectedDiagnostic.diagnosis }}
                      </p>
                    </div>
                    <div>
                      <div class="flex items-center justify-between">
                        <h4 class="text-sm font-medium text-gray-500">
                          Достоверность диагноза
                        </h4>
                        <span
                          :class="getConfidenceColor(selectedDiagnostic.score)"
                          class="text-lg font-bold"
                        >
                          {{ selectedDiagnostic.score }}%
                        </span>
                      </div>
                      <div
                        class="mt-2 h-2 bg-gray-200 rounded-full overflow-hidden"
                      >
                        <div
                          :class="selectedDiagnostic.bg_score"
                          class="h-full"
                          :style="{ width: `${selectedDiagnostic.score}%` }"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
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
  Calendar,
} from "lucide-vue-next";
import { toast } from "vue-sonner";

definePageMeta({
  layout: "admin",
});
const config = useRuntimeConfig();
const publicUrl = config.public.apiBaseUrl + "/storage/";

const selectedPatient = ref(null);
const selectedDiagnostic = ref(null);
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

const selectedImageType = ref(null);

const filters = ref(null);

const { $api } = useNuxtApp();

async function onPatientSelected(patient) {
  if (selectedPatient.value?.id === patient.id) return;
  selectedDiagnostic.value = null;
  selectedPatient.value = patient;
  await fetchDiagnostics();
}

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
  formData.append("image_type", selectedImageType.value);

  isDiagnosticsUploadProccessingLoading.value = true;

  try {
    const response = await $api(
      `/patients/${selectedPatient.value.id}/diagnostics`,
      {
        method: "POST",
        body: formData,
      }
    );

    await fetchDiagnostics();

    selectedDiagnostic.value = response;

    toast.success("Диагностика отправлена на обработку");
  } catch (error) {
    console.error("Ошибка при отправке диагностики:", error);
    toast.error("Не удалось отправить диагностику");
  } finally {
    uploadedFile.value = null;
    imagePreviewUrl.value = null;
    isDiagnosticsUploadProccessingLoading.value = false;
  }
}

async function getFilters() {
  try {
    const response = await $api("/diagnostics/filters", {
      method: "GET",
    });

    filters.value = response;

    selectedImageType.value = filters.value.image_types[0].name;
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

function handleDiagnosticResultSelect(diagnosticResult) {
  selectedDiagnostic.value = diagnosticResult;
}

onMounted(() => {
  getFilters();
});
</script>
