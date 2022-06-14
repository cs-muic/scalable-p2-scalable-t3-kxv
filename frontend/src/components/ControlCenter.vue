<template>
  <v-app>
    <v-app-bar app color="teal darken-3" dark>
      <v-spacer></v-spacer>

      <span class="mr-4">"Control Center"</span>
      <v-btn
        href=""
        target="_blank"
        text
        class="px-0 rounded-circle"
        min-width="36"
      >
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer class="teal darken-4" dark app>
      <v-list>
        <v-list-item class="pl-2">
          <v-list-item-icon class="ml-0 my-2 mr-3">
            <v-icon x-large>mdi-cloud-circle</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Control Center</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="display-room">
          <v-list-item-icon>
            <v-icon>mdi-information-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Display Room</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
// import Vue from "vue";
export default {
//   methods: {
//     async logout() {
//       let response = await Vue.axios.get("/api/logout");
//       if (response.data.success) {
//         await this.$router.push({ path: "/login" });
//       }
//     },
//   },
};
</script>

<style>
div.logo {
  font-size: 18px;
}
</style>