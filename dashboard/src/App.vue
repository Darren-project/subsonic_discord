<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
 <Suspense>
  <RouterView />
</Suspense>
</template>

<style scoped>
@import ./assets/main.css
</style>
