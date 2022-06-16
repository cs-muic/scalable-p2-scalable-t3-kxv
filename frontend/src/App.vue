<template>
  <v-app>
    <v-app-bar
        fixed
        height="80"
        dense
        color="teal darken-3"
        dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <h1 class="white--text font-weight-bold">{{ this.$route.name}}</h1>

      <v-spacer></v-spacer>

      <v-btn
          plain
          fab
          icon
          x-large
          :to="{ name: 'Control Center' }"
      >
        <v-icon>mdi-home</v-icon>
      </v-btn>

    </v-app-bar>

    <br /><br /><br />

    <v-navigation-drawer v-model="drawer" fixed>
      <v-list>
        <v-list-item>
          <v-btn icon @click.stop="drawer = !drawer">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list nav dense>
        <v-list-item-group color="teal">
          <v-list-item v-for="item in items" :key="item.title" :to="item.link">
            <v-list-item-icon>
              <v-icon v-text="item.icon"></v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>

  </v-app>
</template>

<script>

/* eslint-disable */

export default {
  name: 'App',

  components: { },

  data: () => ({
    drawer: false,
    items: [
      { title: "Control Center", icon: "mdi-view-dashboard", link: "/" },
      { title: "Display Room", icon: "mdi-monitor", link: "/display-room" },

    ],
  }),

  created() {
    document.title = "Thumbnail Maker";
  },

};
</script>
