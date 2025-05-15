<template>
  <div class="grid grid-cols-4 gap-4">
    <div class="col-span-4 md:col-span-2">
      <patients-list :global="false" @patient-selected="onPatientSelected" />
    </div>
    <div class="col-span-4 md:col-span-2" v-if="selectedPatient">
      <Card class="w-full">
        <CardHeader>
          <CardTitle>Медицинские изображения</CardTitle>
          <CardDescription
            >Изображения пациента: {{ selectedPatient.name }}</CardDescription
          >
        </CardHeader>
        <CardContent>
          <div v-if="!selectedImage">
            <div class="bg-white rounded-lg shadow-sm p-6 text-center">
              <h3 class="text-lg font-medium text-gray-900 mb-2">
                Нет выбранного изображения
              </h3>
              <p class="text-gray-500">
                Выберите изображение для просмотра диагностической информации.
              </p>
            </div>
          </div>
          <div v-else>
            <div
              class="px-6 py-4 border-b border-gray-200 flex justify-between items-center"
            >
              <div>
                <h2 class="text-lg font-medium text-gray-900">
                  Диагностическая информация
                </h2>
                <p class="mt-1 text-sm text-gray-500">
                  Изображение: {{ selectedImage.bodyPart }} ({{
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
          <Button type="submit" class="w-full mt-4" @click="uploadNewImage">
            Загрузить новое изображение
          </Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import PatientsList from "@/components/PatientsList";
import { CheckCircle, AlertCircle, HelpCircle, Award } from "lucide-vue-next";

definePageMeta({
  layout: "admin",
});

const selectedPatient = ref(null);
const selectedImage = ref(null);
const diagnosticResults = ref([]);
const similarCases = ref([]);

function onPatientSelected(patient) {
  selectedPatient.value = patient;
  // Здесь можно передать `patient` в другой компонент или выполнить другую логику
}

const diagnosis = computed(() => {
  if (!selectedImage.value) return null;
  return diagnosticResults.value.find(
    (d) => d.imageId === selectedImage.value.id
  );
});

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

function uploadNewImage() {
  // Логика загрузки нового изображения
}
</script>
