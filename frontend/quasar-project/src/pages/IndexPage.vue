<template>
  <q-page class="items-center">
    <div class="q-ma-lg row">
      <div class="col-2">
        <filterPane />
      </div>
      <div class="col-10">
        <q-table flat bordered title="Calls" :rows="rows" :columns="columns" row-key="id">
          <template v-slot:body-cell-Summary="props">
            <q-td :props="props">
              <read_summary :summary="props.row.summary"></read_summary>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>

    <q-card class="q-ma-md">
      <q-card-section>
        <q-btn
          color="primary"
          label="Generate Report"
          @click="generateReport"
        />
      </q-card-section>
      <q-card-section>
        <div v-show="showReport">
        <ul>
            <h6 class = "q-mb-xs">Common Issues:</h6>
            <li v-for="(issue, index) in report.common_issues" :key="index">{{ issue }}</li>
            <h6 class = "q-mb-xs">Key Themes:</h6>
            <li v-for="(theme, index) in report.key_themes" :key="index">{{ theme }}</li>
            <h6 class = "q-mb-xs">Areas for improvement:</h6>
            <li v-for="(area, index) in report.key_themes" :key="index">{{ area }}</li>
        </ul>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, provide } from 'vue'
import { getRows } from '../helpers/apiHelpers'
import read_summary from 'components/read_summary.vue'
import filterPane from 'components/filterPane.vue'
import type { DateRange }from '../helpers/apiHelpers'

export interface Row {
  id: number
  summary: string
  call_result: string
  call_duration: string
  contact_id: number
}

interface Report {
  key_themes: string[]
  common_issues: string[]
  Areas_for_improvement: string[]
}

const showReport = ref(false)

const dateRange = ref<DateRange>({ from: '', to: '' });
const report = ref<Report>({
  key_themes: [],
  common_issues: [],
  Areas_for_improvement: []
})
const rows = ref<Row[]>([])
provide('rows', rows)

onMounted(async () => {
  try {
    rows.value = await getRows(dateRange.value, true, true)
  } catch (error) {
    console.error('Error fetching data:', error)
  }
})

const columns = ref([
  {
    name: 'id',
    required: true,
    label: 'Id',
    align: 'left' as const,
    field: (row: Row) => row.id,
    format: (val: string) => `${val}`,
  },
  {
    name: 'Summary',
    label: 'Summary',
    align: 'center' as const,
    field: 'summary',
  },
  {
    name: 'Status',
    label: 'Status',
    align: 'center' as const,
    field: (row: { call_result: string }) => row.call_result,
    format: (val: Row) => `${val}`,
  },
  {
    name: 'Duration',
    label: 'Duration',
    align: 'center' as const,
    field: (row: Row) => row.call_duration,
    format: (val: string) => {
      const minutes = Math.floor(Number(val) / 60)
      const seconds = Number(val) % 60
      return `${minutes}:${seconds.toString().padStart(2, '0')}`
    },
  },
  {
    name: 'Contact',
    label: 'Contact',
    align: 'center' as const,
    field: (row: Row) => row.contact_id,
    format: (val: string) => `${val}`,
  },
])

async function generateReport (): Promise<void> {
  showReport.value = true
  try {
    const response = await fetch('https://coral-app-c58z6.ondigitalocean.app/report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        summarries: rows.value.map((row) => row.summary).join(', ')
      }),
    })
    const data = await response.json()
    report.value.key_themes = data.key_themes
    report.value.common_issues = data.common_issues
    report.value.Areas_for_improvement = data.Areas_for_improvement
    console.log(report.value)
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}
</script>
