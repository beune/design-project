<template>
  <div>
    <v-app>
      <v-app-bar
        id="top-menu-bar"
        :elevation="0"
        height="29px"
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
        <v-spacer/>
        <v-select style="width: 250px; padding-top: 16px;"
                  :items="environments"
                  v-model="environment"
                  v-on:change="environmentChanged"
                  dense
                  height="23px"
        ></v-select>
      </v-app-bar>

      <!-- Sizes your content based upon application components -->
      <v-main>
        <!-- Provides the application the proper gutter -->
        <marker-test :node="text"/>
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
// import d3orgtree from "./components/d3-org-tree.vue"
import PreferencesDialog from "./components/PreferencesDialog.vue"
import MarkerTest from "./components/Marker.vue"

export default {
  components: {
    // d3orgtree,
    PreferencesDialog,
    MarkerTest,
  },
  data: () => ({
    tree: [],
    environments: [],
    environment: "",
    text: {
      children: [
        {
          text: "Een",
          color: null,
          type: "other",
        },
        {
          text: "stervormige laesie",
          color: "#E71212",
          type: "label",
          label: "mass/vorm"
        },
        {
          text: "laterale bovenkwadrant linkermamma,",
          color: "#FEFE7F",
          type: "label",
          label: "mass/location"
        },
      ],
      type: "node",
      label: "mass"
    },
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
