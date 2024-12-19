<template>
  <q-btn @click="showCalender">Click here </q-btn>
  <q-date v-if="calenderBool" v-model="date"></q-date>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const date = ref(new Date())
const calenderBool = ref(false)
function showCalender() {
  calenderBool.value = !calenderBool.value
}
</script>
