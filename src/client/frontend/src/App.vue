<template>
  <div>
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
            <v-list-item to="/preferences" link>
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
          <d3orgtree :treeData="treeData"/>
        </v-container>
      </v-main>
    </v-app>
    <PreferencesDialog @closePreferencesDialog="closePreferencesDialog" :showPreferencesDialog="showPreferencesDialog"/>
  </div>
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
import PreferencesDialog from "./components/PreferencesDialog.vue"

export default {
  components: {
    d3orgtree,
    PreferencesDialog
  },
  name: 'App',
  data: () => ({
    treeData: null
  }),
  methods: {
    closePreferencesDialog() {
      this.$router.push({path: '/'})
    },
    test_function() {
      window.eel.test("test");
    },
    changeState(data) {
      this.tree = data.tree;
      this.environment = data.environment;
      // this.text = data.text;
    }
  },
  computed: {
    showPreferencesDialog() {
      return this.$route.path.includes("preferences")
    }
  },
  mounted: function() {
    eel.expose(this.changeState, "change_state");
  }

}
</script>
