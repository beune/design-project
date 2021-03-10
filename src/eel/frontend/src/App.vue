<template>
  <v-app>
    <v-app-bar :elevation="0" dense>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
          Bestand Beeld Help
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-app-bar>
    <!-- Sizes your content based upon application components -->
    <v-main>
    <v-app-bar :elevation="0" dense>
      <v-list-item>
        <v-list-item-content>
          Mammografie 22-09-16
        </v-list-item-content>
      </v-list-item>
    </v-app-bar>
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <d3orgtree/>
      </v-container>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>
  </v-app>
</template>

<style lang="scss">
/*TODO remove browser scrollbar*/
</style>

<script>
import d3orgtree from "./components/d3-org-tree.vue"
export default {
  components: {
    d3orgtree,
  },
  name: 'Normal',
  data: () => ({
  }),
  methods: {
    test_function () {
      window.eel.test("test");
    }
  },
}
</script>
