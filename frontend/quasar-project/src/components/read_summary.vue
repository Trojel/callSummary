<template>
  <q-btn size="xs" outline rounded icon="open_in_full" @click="openState = true">Read</q-btn>
  <q-dialog v-model="openState">
    <q-card>
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Call Summary</div>
        <q-space />
        <q-btn icon="close" outline rounded v-close-popup />
      </q-card-section>

      <q-card-section>
        {{ summary }}
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
defineProps({
  summary: String,
})

const openState = ref(false)
</script>
