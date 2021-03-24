<template>
  <div>
    <v-app>
      <v-app-bar
        id="top-menu-bar"
        absolute
        :elevation="0"
        dense
        color="primary"
      >
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

          <v-divider />

          <v-list>
            <v-list-item link>
              <v-list-item-title>Opslaan</v-list-item-title>
            </v-list-item>
            <v-list-item link>
              <v-list-item-title>Opslaan als...</v-list-item-title>
            </v-list-item>
          </v-list>

          <v-divider />

          <v-list>
            <v-list-item link>
              <v-list-item-title>Exporteren naar schijf...</v-list-item-title>
            </v-list-item>
            <v-list-item link>
              <v-list-item-title>Exporteren naar database...</v-list-item-title>
            </v-list-item>
          </v-list>

          <v-divider />

          <v-list>
            <v-list-item
              to="/preferences"
              link
            >
              <v-list-item-title>Voorkeuren...</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-btn
          class="text-none"
          tile
          text
          elevation="0"
          color="white"
        >
          Beeld
        </v-btn>
        <v-btn
          class="text-none"
          tile
          text
          elevation="0"
          color="white"
        >
          Help
        </v-btn>
        <v-spacer />
        <div style="width: 250px;">
          <v-select
            v-model="environment"
            class="pt-5"
            :dark="true"
            :items="environments"
            height="25px"
            label="Environment"
            @change="environmentChanged"
          />
        </div>
      </v-app-bar>

      <!-- Sizes your content based upon application components -->
      <v-main>
        <!-- Provides the application the proper gutter -->
        <v-container fluid>
          <d3orgtree v-if="tree.length !== 0"
            :tree-data="tree"
          />
        </v-container>
      </v-main>
    </v-app>
    <PreferencesDialog
      :show-preferences-dialog="showPreferencesDialog"
      @closePreferencesDialog="closePreferencesDialog"
    />
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
  data: () => ({
    tree: [],
    environments: [],
    environment: "",
  }),
  computed: {
    showPreferencesDialog() {
      return this.$route.path.includes("preferences")
    }
  },
  mounted: function() {
    eel.expose(this.initializeFrontend, "initialize_frontend");
    eel.expose(this.updateFrontend, "update_frontend");
  },
  methods: {
    closePreferencesDialog() {
      this.$router.push({ path: '/' })
    },
    test_function() {
      window.eel.test("test");
    },
    //initialize frontend (called from backend)
    initializeFrontend(environments) {
      this.environments = environments
    },
    //update frontend (called from backend)
    updateFrontend(tree, environment) {
      this.tree = tree;
      this.environment = environment;
    },
    //notifies backend of environment change
    environmentChanged(newEnvironment) {
      window.eel.update_environment(newEnvironment)
    }
  },
}
</script>
