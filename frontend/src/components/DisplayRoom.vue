<template>
  <v-container class="my-5 mx-auto" max-width="300">
    <v-row>
      <v-col
          v-for="img in images"
          :key="img"
          class="d-flex child-flex"
          cols="4"
      >
        <v-card>
          <v-img
              :src="img.file"
              :aspect-ratio="16/9"
              class="grey lighten-2"
          >
            <template v-slot:placeholder>
              <v-row
                  align="center"
                  justify="center"
              >
                <v-progress-circular
                    indeterminate
                    color="grey lighten-5"
                ></v-progress-circular>
              </v-row>
            </template>
          </v-img>
          <v-card-actions>
            <v-card-title class="text-h6">
              {{ img.name }}
            </v-card-title>
            <v-spacer></v-spacer>
            <v-btn
                class="ml-2"
                text
            >
              Delete
              <v-icon left>mdi-close-box</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>

      </v-col>
    </v-row>

    <v-dialog v-model="check" max-width="500">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            fab
            dark
            fixed
            bottom
            right
            color="teal darken-3"
            class="mb-16"
            v-bind="attrs"
            v-on="on"
        >
          <v-icon>mdi-format-list-checkbox</v-icon>
        </v-btn>
      </template>
      <v-card
          class="px-7 pt-7 pb-4 mx-auto text-center d-inline-block"
      >
        <v-card-title class="justify-center">
          Progress
        </v-card-title>
        <v-card-actions class="justify-space-around">
          <v-spacer></v-spacer>
          <v-btn text @click="check = false" color="teal">
            CLOSE
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


    <v-dialog v-model="dialog" max-width="500">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            fab
            dark
            fixed
            bottom
            right
            color="teal darken-3"
            v-bind="attrs"
            v-on="on"
        >
          <v-icon>mdi-close-box-multiple</v-icon>
        </v-btn>
      </template>
      <v-card
          class="px-7 pt-7 pb-4 mx-auto text-center d-inline-block"
      >
        <v-card-title class="justify-center">
          Do you want to delete all GIFs?
        </v-card-title>
        <v-card-actions class="justify-space-around">
          <v-btn text @click="dialog = false" color="red">
            NO
          </v-btn>
          <v-btn text @click="dialog = false" color="teal">
            YES
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import Vue from "vue";

export default {
  data: () => ({
    check: false,
    dialog: false,
    images: [],
  }),

  created() {
    this.getGIFs();
  },

  methods: {
    async getGIFs() {
      let data = {
        bucket: "gifs"
      }
      let result = await Vue.axios.post("/api/get-gifs", data);
      this.images = result.data.gifs;
    },
  },
};
</script>

<style></style>