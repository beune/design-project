<template>
  <v-card
    elevation="0"
    outlined
  >
    <v-card-title>
      No environment selected
    </v-card-title>
    <v-card-subtitle>
      Pick an environment by using the selector in the top right corner
    </v-card-subtitle>
    <v-icon
      x-large
      style="position:absolute; right: 0; top: 5px"
      class="ma-5"
    >
      mdi-alert-octagon-outline
    </v-icon>
  </v-card>
</template>

<script>
export default {
name: "EmptyState"
}
</script>

<style scoped>

</style>
