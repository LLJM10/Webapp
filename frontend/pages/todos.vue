<template>
  <div class="p-6 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Todo Liste</h1>

    <!-- Neues Todo hinzufügen -->
    <div class="flex gap-2 mb-6">
      <input
        v-model="newTodo"
        type="text"
        placeholder="Neues Todo..."
        class="border px-3 py-2 flex-1 rounded"
      />
      <button
        @click="addTodo"
        class="bg-blue-600 text-white px-4 py-2 rounded"
      >
        ➕ Hinzufügen
      </button>
    </div>

    <!-- Todos anzeigen -->
    <ul>
      <li
        v-for="todo in todos"
        :key="todo.id"
        class="flex items-center justify-between p-2 border-b"
      >
        <span :class="{ 'line-through text-gray-500': todo.done }">
          {{ todo.title }}
        </span>
        <div class="flex gap-2">
          <button
            @click="toggleDone(todo)"
            class="text-sm bg-green-500 text-white px-2 py-1 rounded"
          >
            {{ todo.done ? "❌ Rückgängig" : "✅ Erledigt" }}
          </button>
          <button
            @click="deleteTodo(todo.id)"
            class="text-sm bg-red-500 text-white px-2 py-1 rounded"
          >
            🗑️ Löschen
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()
const apiBase = config.public.apiBase + "/todos/"

// Todos laden
const { data: todos, refresh } = await useFetch(apiBase)

// Neues Todo
const newTodo = ref("")

// Todo hinzufügen
async function addTodo() {
  if (!newTodo.value) return
  await $fetch(apiBase, {
    method: "POST",
    body: { title: newTodo.value, done: false },
  })
  newTodo.value = ""
  refresh()
}

// Todo löschen
async function deleteTodo(id) {
  await $fetch(apiBase + id + "/", { method: "DELETE" })
  refresh()
}

// Status toggeln
async function toggleDone(todo) {
  await $fetch(apiBase + todo.id + "/", {
    method: "PATCH",
    body: { done: !todo.done },
  })
  refresh()
}
</script>
