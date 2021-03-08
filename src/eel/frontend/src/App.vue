<template>
  <div class="page-container">
    <md-app>
      <md-app-toolbar class="md-primary">
      <div class="md-toolbar-section-start">
        <span class="md-title">Mammografie 22-09-16</span>
      </div>
      <div class="md-toolbar-section-end">
        <md-menu md-align-trigger md-size="auto">
          <md-button md-menu-trigger>Mammo</md-button>
          <md-menu-content>
          </md-menu-content>
        </md-menu>
      </div>
      </md-app-toolbar>

      <md-app-drawer md-permanent="full">
        <md-toolbar class="md-transparent" md-elevation="0">
          Navigatie
        </md-toolbar>

        <md-list>
          <!-- NB: md-offset gives prop warning but this has to be fixed in the upstream, I have filed an issue on GitHub https://github.com/vuematerial/vue-material/issues/2315 -->
          <md-list-item>
            <md-menu md-align-trigger md-size="auto" md-offset-x="127" :md-offset-y="-36">
              <md-button md-menu-trigger><md-icon>save</md-icon> Bestand</md-button>
              <md-menu-content>
                <md-menu-item>Nieuw</md-menu-item>
                <md-menu-item>Openen...</md-menu-item>
                <md-menu-item>Opslaan</md-menu-item>
                <md-menu-item>Opslaan als...</md-menu-item>
                <md-menu-item>Exporteren</md-menu-item>
                <md-menu-item>Voorkeuren...</md-menu-item>
                <md-menu-item>Afsluiten</md-menu-item>
              </md-menu-content>
            </md-menu>
          </md-list-item>

          <md-list-item>
            <md-menu md-align-trigger md-size="auto" md-offset-x="127" :md-offset-y="-36">
              <md-button md-menu-trigger><md-icon>fit_screen</md-icon> Beeld</md-button>
            </md-menu>
          </md-list-item>

          <md-list-item>
            <md-menu md-align-trigger md-size="auto" md-offset-x="127" :md-offset-y="-36">
              <md-button md-menu-trigger><md-icon>help</md-icon> Help</md-button>
            </md-menu>
          </md-list-item>
        </md-list>
      </md-app-drawer>

      <md-app-content>
        <d3orgtree/>
      </md-app-content>
    </md-app>
  </div>
</template>

<style lang="scss">
  .md-app {
    height: 100vh;
    border: 1px solid rgba(#000, .12);
  }

  .md-drawer {
    width: 230px;
    max-width: calc(100vw - 125px);
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
