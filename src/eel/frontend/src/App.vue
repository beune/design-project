<template>
  <v-app>
      <v-app-bar id="top-menu-bar" :elevation="0" height="29px" dense color="primary">
        <v-menu
          bottom
          :offset-y="true"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="text-none"
              tile
              text
              elevation="0"
              color="white"
              v-bind="attrs"
              v-on="on"
            >
              Bestand
            </v-btn>
          </template>

          <v-list>
            <v-list-item link>
              <v-list-item-title>Nieuw</v-list-item-title>
            </v-list-item>
            <v-list-item link>
              <v-list-item-title>Openen...</v-list-item-title>
            </v-list-item>
          </v-list>

          <v-divider></v-divider>

          <v-list>
            <v-list-item link>
              <v-list-item-title>Opslaan</v-list-item-title>
            </v-list-item>
            <v-list-item link>
              <v-list-item-title>Opslaan als...</v-list-item-title>
            </v-list-item>
          </v-list>

          <v-divider></v-divider>

          <v-list>
            <v-list-item link>
              <v-list-item-title>Exporteren naar schijf...</v-list-item-title>
            </v-list-item>
            <v-list-item link>
              <v-list-item-title>Exporteren naar database...</v-list-item-title>
            </v-list-item>
          </v-list>

          <v-divider></v-divider>

          <v-list>
            <v-list-item link>
              <v-list-item-title>Voorkeuren...</v-list-item-title>
            </v-list-item>
          </v-list>

        </v-menu>
        <v-btn class="text-none" tile text elevation="0" color="white">
          Beeld
        </v-btn>
        <v-btn class="text-none" tile text elevation="0" color="white">
          Help
        </v-btn>
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
#menu-bar-wrapper {
  border-bottom: black 1px;
}

.body {
  font-family: "Segoe UI", serif;
}
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
