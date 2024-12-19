<template>
  <q-layout view="hHh lpR lfr">
    <q-header elevated class="q-pa-sm bg-brand text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-icon class = "q-ma-md">
            <img src="/icons/SPRII__Logomark_orange.png" style="width: 40px; height: 40px;" />
          </q-icon >
          Sprii Call Insights
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
