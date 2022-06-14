<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <template>
        <v-app>
          <router-view />
        </v-app>
      </template>

    </v-app-bar>
  </v-app>
</template>

<script>
import ControlCenter from "./components/ControlCenter.vue";

/* eslint-disable */

export default {
  name: 'App',

  components: {
    ControlCenter,
  },

  data: () => ({
    //
  }),
};
</script>
