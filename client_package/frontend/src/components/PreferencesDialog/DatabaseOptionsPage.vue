<template>
  <v-form>
    <v-container fluid>
      <v-row>
        <v-text-field
          v-model="databaseURL"
          :rules="[rules.required]"
          :type="'text'"
          name="input-10-1"
          label="Database URL"
        />
        <v-text-field
          v-model="databaseUsername"
          :rules="[rules.required]"
          :type="'text'"
          name="input-10-1"
          label="Username"
        />
        <v-text-field
          v-model="databasePassword"
          :append-icon="showPassword ? 'visibility' : 'visibility_off'"
          :rules="[rules.required]"
          :type="showPassword ? 'text' : 'password'"
          name="input-10-1"
          label="Password"
          counter
          @click:append="showPassword = !showPassword"
        />
      </v-row>
    </v-container>
  </v-form>
</template>
<script>
  export default {
  data: () => ({
       showPassword: false,
        databaseURL: '',
        databaseUsername: '',
        databasePassword: '',
        rules: {
          required: value => !!value || 'Required.',
        },
  }),
}
</script>
