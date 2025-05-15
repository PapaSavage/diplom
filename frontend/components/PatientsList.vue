<template>
  <Card class="w-full">
    <CardHeader>
      <CardTitle>Список пациентов</CardTitle>
      <CardDescription>Всего пациентов: {{ patients.length }}</CardDescription>
    </CardHeader>

    <CardContent>
      <Input
        v-model="searchQuery"
        placeholder="Поиск по имени..."
        class="mb-4"
      />
      <div v-if="isLoading" class="flex justify-center items-center h-64">
        <div
          class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"
        ></div>
      </div>
      <ul
        v-else
        role="list"
        class="divide-y divide-gray-200 max-h-96 overflow-auto"
      >
        <li
          v-for="patient in filteredPatients"
          :key="patient.id"
          class="py-4 flex items-center justify-between hover:bg-gray-50 cursor-pointer transition-colors duration-150"
          @click="handlePatientSelect(patient)"
        >
          <div class="flex items-center space-x-3 px-3">
            <div class="bg-blue-500 rounded-full p-2 text-white">
              <UserIcon size="16" />
            </div>
            <div>
              <p class="font-medium">{{ patient.name }}</p>
              <div
                class="flex flex-col gap-2 md:gap-4 md:flex-row text-sm text-gray-500 mt-1"
              >
                <span class="flex items-center">
                  <CalendarIcon class="mr-1 h-4 w-4" />
                  <span>Возраст: {{ patient.age }}</span>
                </span>
                <span class="flex items-center">
                  <ClockIcon class="mr-1 h-4 w-4" />
                  <span
                    >Пол:
                    {{
                      patient.gender === "male"
                        ? "М"
                        : patient.gender === "female"
                        ? "Ж"
                        : "Другой"
                    }}</span
                  >
                </span>
                <span class="flex items-center">
                  <Weight class="mr-1 h-4 w-4" />
                  <span>Вес: {{ patient.weight }}</span>
                </span>
              </div>
              <p
                v-if="patient.medical_history"
                class="text-sm text-gray-500 truncate mt-1"
              >
                История: {{ patient.medical_history }}
              </p>
            </div>
          </div>
          <div class="flex space-x-2 mr-3">
            <!-- <Button @click="selectedPatient = patient" variant="outline"
              >Просмотр</Button
            > -->
            <!-- Форма редактирования -->
            <Dialog v-if="global">
              <DialogTrigger as-child>
                <Button @click="openEditDialog(patient)" variant="secondary"
                  >Редактировать</Button
                >
              </DialogTrigger>
              <DialogContent class="sm:max-w-md">
                <DialogHeader>
                  <DialogTitle>Редактирование пациента</DialogTitle>
                </DialogHeader>

                <form @submit.prevent="updatePatient" class="space-y-4">
                  <div>
                    <Label
                      for="edit-name"
                      class="block text-sm font-medium mb-1"
                      >Имя</Label
                    >
                    <Input
                      id="edit-name"
                      v-model="editingPatient.name"
                      required
                      class="w-full"
                    />
                  </div>

                  <div>
                    <Label for="edit-age" class="block text-sm font-medium mb-1"
                      >Возраст</Label
                    >
                    <Input
                      id="edit-age"
                      type="number"
                      v-model.number="editingPatient.age"
                      required
                      class="w-full"
                    />
                  </div>

                  <div>
                    <Label
                      for="edit-weight"
                      class="block text-sm font-medium mb-1"
                      >Вес (кг)</Label
                    >
                    <Input
                      id="edit-weight"
                      type="number"
                      v-model.number="editingPatient.weight"
                      class="w-full"
                    />
                  </div>

                  <div>
                    <Label
                      for="edit-gender"
                      class="block text-sm font-medium mb-1"
                      >Пол</Label
                    >
                    <Select v-model="editingPatient.gender">
                      <SelectTrigger class="w-full">
                        <SelectValue placeholder="Выберите пол" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="male">Мужской</SelectItem>
                        <SelectItem value="female">Женский</SelectItem>
                        <SelectItem value="other">Другой</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label
                      for="edit-medical-history"
                      class="block text-sm font-medium mb-1"
                      >Медицинская история</Label
                    >
                    <Textarea
                      class="w-full"
                      id="edit-medical-history"
                      v-model="editingPatient.medical_history"
                      rows="3"
                    />
                  </div>
                  <DialogClose as-child>
                    <Button type="submit" class="w-full mt-4">Обновить</Button>
                  </DialogClose>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        </li>
      </ul>
    </CardContent>

    <CardFooter v-if="global">
      <!-- Кнопка для открытия формы -->
      <Dialog>
        <DialogTrigger as-child>
          <Button>Добавить нового пациента</Button>
        </DialogTrigger>

        <DialogContent class="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Новый пациент</DialogTitle>
          </DialogHeader>

          <form
            @submit.prevent="addNewPatientForm"
            class="space-y-4"
            v-auto-animate
          >
            <FormField
              name="name"
              v-slot="{ componentField }"
              :validate-on-blur="true"
            >
              <FormItem>
                <FormLabel>Имя</FormLabel>
                <FormControl>
                  <Input id="name" v-bind="componentField" required />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <FormField
              name="age"
              v-slot="{ componentField }"
              :validate-on-blur="true"
            >
              <FormItem>
                <FormLabel>Возраст</FormLabel>
                <FormControl>
                  <Input
                    id="age"
                    type="number"
                    v-bind="componentField"
                    required
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <FormField
              name="weight"
              v-slot="{ componentField }"
              :validate-on-blur="true"
            >
              <FormItem>
                <FormLabel>Вес (кг)</FormLabel>
                <FormControl>
                  <Input
                    id="weight"
                    type="number"
                    v-bind="componentField"
                    required
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <FormField
              name="gender"
              v-slot="{ componentField }"
              :validate-on-blur="true"
            >
              <FormItem>
                <FormLabel>Пол</FormLabel>
                <FormControl>
                  <Select v-model="newPatient.gender">
                    <SelectTrigger>
                      <SelectValue placeholder="Выберите пол" required />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="male">Мужской</SelectItem>
                      <SelectItem value="female">Женский</SelectItem>
                      <SelectItem value="other">Другой</SelectItem>
                    </SelectContent>
                  </Select>
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <FormField
              name="medical_history"
              v-slot="{ componentField }"
              :validate-on-blur="true"
            >
              <FormItem>
                <FormLabel>Медицинская история</FormLabel>
                <FormControl>
                  <Textarea
                    id="medical_history"
                    rows="3"
                    v-bind="componentField"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <DialogClose as-child>
              <Button type="submit" class="w-full mt-4" :disabled="!meta.valid"
                >Создать</Button
              >
            </DialogClose>
          </form>
        </DialogContent>
      </Dialog>
    </CardFooter>
  </Card>
</template>

<script setup>
import { ref } from "vue";
import { toast } from "vue-sonner";

// Импорты UI-компонентов

import { Button } from "@/components/ui/button";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

import { UserIcon, CalendarIcon, ClockIcon, Weight } from "lucide-vue-next";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";
import { vAutoAnimate } from "@formkit/auto-animate/vue";

const props = defineProps({
  global: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits(["patient-selected"]);

// Схема валидации
const patientSchema = toTypedSchema(
  z.object({
    name: z.string().min(2, "Имя должно быть не менее 2 символов"),
    age: z.number().positive("Возраст должен быть положительным числом"),
    weight: z
      .number()
      .positive("Вес должен быть положительным числом")
      .optional(),
    gender: z.enum(["male", "female", "other"]),
    medical_history: z.string().optional(),
  })
);

const patients = ref([]);
const selectedPatient = ref(null);
const editingPatient = ref(null);
const newPatient = ref({
  name: "",
  age: null,
  gender: "male",
  medical_history: "",
  weight: null,
});
0;

const { handleSubmit, setFieldError, isFieldDirty, meta } = useForm({
  validationSchema: patientSchema,
  initialValues: newPatient.value,
});

const { $api } = useNuxtApp();

const isLoading = ref(false);

const searchQuery = ref("");

const filteredPatients = computed(() => {
  if (!searchQuery.value) return patients.value;
  const query = searchQuery.value.toLowerCase();
  return patients.value.filter((patient) =>
    patient.name.toLowerCase().includes(query)
  );
});

async function fetchPatients() {
  isLoading.value = true;
  try {
    const response = await $api("/patients", {
      method: "GET",
    });

    patients.value = response;
  } catch (error) {
    console.error("Ошибка при получении пациентов:", error);
  } finally {
    isLoading.value = false;
  }
}
const addNewPatientForm = handleSubmit(async (values) => {
  await addNewPatient(values);
});
async function addNewPatient(values) {
  isLoading.value = true;

  try {
    const response = await $api("/patients", {
      method: "POST",
      body: JSON.stringify(values),
      onResponse: async ({ response }) => {
        if ([200, 201].includes(response.status)) {
          await fetchPatients();

          toast("Пациент добавлен");

          newPatient.value = {
            name: "",
            age: null,
            gender: "male",
            medical_history: "",
            weight: null,
          };
        }
      },
    });
  } catch (error) {
  } finally {
    isLoading.value = false;
  }
}

async function updatePatient() {
  isLoading.value = true;
  try {
    const response = await $api(`/patients/${editingPatient.value.id}`, {
      method: "PATCH",
      body: JSON.stringify(editingPatient.value),
      onResponse: async ({ response }) => {
        if ([200, 201].includes(response.status)) {
          await fetchPatients();
          toast("Данные пациента обновлены");
        }
      },
    });
  } catch (error) {
    console.error("Ошибка обновления пациента:", error);
  } finally {
    isLoading.value = false;
  }
}

function openEditDialog(patient) {
  editingPatient.value = { ...patient };
}

function handlePatientSelect(patient) {
  emit("patient-selected", patient);
}

onMounted(() => {
  fetchPatients();
});
</script>
