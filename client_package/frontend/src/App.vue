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
              style="margin-top: 10px;"
              class="text-none"
              tile
              text
              elevation="0"
              color="white"
              v-bind="attrs"
              v-on="on"
            >
              File
            </v-btn>
          </template>

          <v-list>
            <v-list-item
              link
              @click="copyTextRep"
            >
              <v-list-item-title>Copy to G2Speech</v-list-item-title>
            </v-list-item>
          </v-list>
          <v-divider />
          <v-list>
            <v-list-item
              link
              @click="addToDB"
            >
              <v-list-item-title>Export to database...</v-list-item-title>
            </v-list-item>
          </v-list>

          <v-divider />
        </v-menu>
        <v-btn
          style="margin-top: 10px;"
          class="text-none"
          tile
          text
          elevation="0"
          color="white"
        >
          View
        </v-btn>
        <v-btn
          style="margin-top: 10px;"
          class="text-none"
          tile
          text
          elevation="0"
          color="white"
        >
          Help
        </v-btn>
        <v-spacer />
        <v-progress-circular
          v-if="loading"
          style="margin-top: 10px"
          indeterminate
          color="white"
        />
        <v-btn
          style="margin-top: 10px;"
          icon
          color="white"
          @click="$vuetify.theme.dark = !$vuetify.theme.dark"
        >
          <v-icon>mdi-brightness-6</v-icon>
        </v-btn>

        <div style="width: 250px; padding-top: 10px;">
          <v-select
            v-model="environment"
            class="pt-5"
            dark
            :items="environments"
            height="25px"
            label="Environment"
            @change="environmentChanged"
          />
        </div>
        <template v-slot:extension>
          <v-tabs
            v-model="tab"
            grow
            dark
          >
            <v-tabs-slider color="orange" />
            <v-tab
              v-for="tab in tabs"
              :key="tab"
              class="white--text"
            >
              {{ tab }}
            </v-tab>
          </v-tabs>
        </template>
      </v-app-bar>

      <!-- Sizes your content based upon application components -->
      <v-main>
        <!-- Provides the application the proper gutter -->

        <v-tabs-items
          v-if="envchosen"
          v-model="tab"
        >
          <v-tab-item>
            <div style="padding-top: 90px;">
              <d3orgtree
                v-if="tree.length > 1"
                :tree-data="tree"
                @tree-changed="treeChanged()"
              />
            </div>
          </v-tab-item>
          <v-tab-item>
            <v-container fluid>
              <div style="padding-top: 90px;">
                <marker-test :node="text" />
              </div>
            </v-container>
          </v-tab-item>
        </v-tabs-items>
        <div
          v-else
          style="padding-top: 90px;"
        >
          <empty-state />
        </div>
      </v-main>
      <v-snackbar
        v-model="errorMessage"
        :timeout="3000"
        color="red"
        justify="center"
      >
        {{ errorText }}
      </v-snackbar>
    </v-app>
  </div>
</template>

<style lang="scss">

html { overflow-y: auto }

.v-tabs-slider-wrapper {
  border: 4px solid #EF7104;
}

#menu-bar-wrapper {
  border-bottom: black 1px;
}

.body {
  font-family: "Segoe UI", serif;
}
</style>

<script>
import d3orgtree from "./components/d3-org-tree.vue"
import MarkerTest from "./components/Marker.vue"
import EmptyState from "./components/EmptyState"

export default {
  components: {
    d3orgtree,
    MarkerTest,
    EmptyState
  },
  data: () => ({
    tab: null,
    tabs: ["Tree" ,"Text"],
    tree: [],
    environments: [],
    environment: "",
    envchosen: false,
    errorMessage: false,
    loading: false,
    errorText: "",
    text: {}
  }),
  mounted: function() {
    eel.expose(this.initializeFrontend, "initialize_frontend");
    eel.expose(this.updateFrontend, "update_frontend");
    eel.expose(this.showServerError, "show_server_error")
    eel.expose(this.showLoader, "show_loader");
  },
  methods: {
    //initialize frontend (called from backend)
    initializeFrontend(environments) {
      this.environments = environments;
    },
    //update frontend (called from backend)
    updateFrontend(tree, environment, text) {
      this.tree = tree;
      this.environment = environment;
      this.text = text;
    },
    //notifies backend of environment change
    environmentChanged(newEnvironment) {
      window.eel.update_environment(newEnvironment);
      this.envchosen = true;
    },
    copyTextRep() {
      window.eel.copy_tree();
    },
    showLoader(show) {
      this.loading = show;
    },
    showServerError(mess) {
      this.errorText = mess;
      this.errorMessage = true;
    },
    addToDB() {
      window.eel.add_to_db();
    },
  },
}
</script>
