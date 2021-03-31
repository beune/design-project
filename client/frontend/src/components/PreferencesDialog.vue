<template>
  <v-dialog
    v-model="showPreferencesDialog"
    width="500"
    @click:outside="closePreferencesDialog"
  >
    <v-card>
      <v-card-title class="headline">
        Preferences
      </v-card-title>
      <v-row no-gutters>
        <v-col cols="4">
          <v-list
            dense
            nav
          >
            <v-list-item-group
              v-model="selectedItem"
              color="primary"
            >
              <v-list-item
                v-for="item in items"
                :key="item.title"
                link
                @click="navigate(item.routerPath)"
              >
                <v-list-item-icon>
                  <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                  <v-list-item-title>{{ item.text }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-col>
        <v-col>
          <v-container>
            <!--TODO fix met vue-router-->
            <router-view />
            <DatabaseOptionsPage
              v-if="this.$route.path.includes('database')"
            />
          </v-container>
        </v-col>
      </v-row>
      <v-card-text />
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="primary"
          text
          @click="closePreferencesDialog"
        >
          CANCEL
        </v-btn>
        <v-btn
          color="primary"
          text
          @click="saveNewPreferences"
        >
          OK
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import DatabaseOptionsPage from './PreferencesDialog/DatabaseOptionsPage.vue'
  export default {
  components: {
    DatabaseOptionsPage
  },
  props: {
    showPreferencesDialog: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    selectedItem: 0,
       items: [
        { text: 'Database', icon: 'storage', routerPath: 'database' },
        { text: 'G2Speech', icon: 'record_voice_over', routerPath: 'g2speech' },
        { text: 'Substitutions', icon: 'swap_horiz', routerPath: 'substitutions' },
      ],
  }),
  methods: {
    navigate(path) {
      this.$router.push({ path: '/preferences/' + path })
    },
    saveNewPreferences () {
      this.closePreferencesDialog()
    },
    closePreferencesDialog(){
      this.$emit('closePreferencesDialog')
    }
  }
}
</script>
