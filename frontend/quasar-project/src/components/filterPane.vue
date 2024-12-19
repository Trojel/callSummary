<template>
  <q-card class="q-pa-md q-mr-lg">
    <div class="q-pa-none">
      <div class="text-h5">Filters</div>

      <div class="q-mb-sm">
        <q-checkbox v-model="resolved" label="Show resolved" checked-icon="check" color="green" />
      </div>

      <div class="q-mb-sm">
        <q-checkbox v-model="unresolved" label="Show unresolved" checked-icon="check" color="green" />
      </div>

      <div class="q-mb-sm">
        <q-input v-model="search" label="Search" style="max-width: 300px" />
      </div>

      <div class="q-mb-md">
  <div class="q-pb-sm text-h6">Choose date range</div>
  <q-input
    filled
    v-model="dateRangeString"
    mask="##/##/#### - ##/##/####"
    class="q-ma-none"
    style="max-width: 100%; width: 300px;"
  >
    <template v-slot:append>
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
          <q-date v-model="dateRange" range mask="DD/MM/YYYY">
            <div class="row items-center justify-start">
              {{ dateRange }}
              <q-btn v-close-popup label="Close" color="primary" flat />
            </div>
          </q-date>
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</div>


      <div class="q-mt-md row justify-start">
        <q-btn color="primary" label="Apply" @click="applyFilters" />
      </div>
    </div>
  </q-card>
</template>

<script setup lang="ts">
import { ref, watch, inject } from 'vue'
import type { DateRange } from '../helpers/apiHelpers'
import { getRows } from '../helpers/apiHelpers'
import type { Row } from '../pages/IndexPage.vue'

const resolved = ref(true)
const unresolved = ref(true)
const search = ref('')


const rows = inject('rows', ref<Row[]>([]))

const dateRange = ref<DateRange>({ from: '', to: '' })
const dateRangeString = ref(`${dateRange.value.from} - ${dateRange.value.to}`)

// Watch for changes in dateRange and update dateRangeString
watch(dateRange, (newValue) => {
  if (newValue.from && newValue.to) {
    dateRangeString.value = `${newValue.from} - ${newValue.to}`
  } else if (newValue.from) {
    dateRangeString.value = `${newValue.from}`
  } else {
    dateRangeString.value = ''
  }
})

async function applyFilters (): Promise<void> {
  try {
    rows.value = await getRows(dateRange.value, resolved.value, unresolved.value)
    console.log("resolved value", resolved.value)
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}
</script>
