<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold">Список пациентов</h1>

    <!-- Поиск -->
    <Input
      v-model="searchQuery"
      placeholder="Поиск по ФИО..."
      class="max-w-md"
    />

    <!-- Таблица -->
    <Card class="overflow-hidden py-0">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ФИО</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Телефон</TableHead>
            <TableHead>Дата рождения</TableHead>
            <TableHead>Действия</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="patient in filteredPatients" :key="patient.id">
            <TableCell>{{ patient.name }}</TableCell>
            <TableCell>{{ patient.email }}</TableCell>
            <TableCell>{{ patient.phone }}</TableCell>
            <TableCell>{{ formatDate(patient.birthDate) }}</TableCell>
            <TableCell>
              <Button variant="ghost" size="sm" @click="editPatient(patient)">
                Редактировать
              </Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Card>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

definePageMeta({
  layout: "admin",
});

// Имитация данных
const patients = ref([
  {
    id: 1,
    name: "Иванов Иван Иванович",
    email: "ivanov@example.com",
    phone: "+79001234567",
    birthDate: "1990-05-15",
  },
  {
    id: 2,
    name: "Петров Петр Петрович",
    email: "petrov@example.com",
    phone: "+79009876543",
    birthDate: "1985-12-25",
  },
]);

const searchQuery = ref("");

const filteredPatients = computed(() => {
  return patients.value.filter((patient) =>
    patient.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString("ru-RU");
};

const editPatient = (patient) => {
  alert(`Редактирование пациента: ${patient.name}`);
};
</script>

<style scoped>
/* Дополнительные стили можно добавить здесь */
</style>
