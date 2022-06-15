<template>
  <v-container class="my-5 mx-auto" max-width="300">
    <v-row>
      <v-col
          v-for="vid in videos"
          :key="vid.name"
          class="d-flex child-flex"
          cols="4"
      >
        <v-card>
          <video
              :src="vid.file"
              width="100%"
              class="grey lighten-2"
              controls
          >
          </video>
          <v-card-actions>
            <v-card-title class="text-h6">
              {{ vid.name }}
            </v-card-title>
            <v-spacer></v-spacer>
            <v-btn
                class="ml-2"
                text
                @click="extractVideo(vid.name)"
            >
              Convert
              <v-icon left>mdi-plus-box</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>

      </v-col>
    </v-row>

    <v-row
        align="center"
        justify="center"
    >
      <v-progress-circular
          v-show="loading"
          :size="70"
          :width="7"
          color="teal"
          indeterminate
          class="my-16"
      ></v-progress-circular>
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
            @click="getStatus"
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
        <v-card-text v-for="s in this.$store.state.queue" :key="s.id">
          <span>{{ s.id }}</span><v-spacer></v-spacer><span>done</span>
        </v-card-text>
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
          <v-icon>mdi-plus-box-multiple</v-icon>
        </v-btn>
      </template>
      <v-card
          class="px-7 pt-7 pb-4 mx-auto text-center d-inline-block"
      >
        <v-card-title class="justify-center">
          Do you want to convert all videos to GIFs?
        </v-card-title>
        <v-card-actions class="justify-space-around">
          <v-btn text @click="dialog = false" color="red">
            NO
          </v-btn>
          <v-btn text @click="extractAll" color="teal">
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
    dialog: false,
    check: false,
    loading: true,
    videos: [],
  }),

  created() {
    this.getVideos();
  },

  methods: {
    async getVideos() {
      let data = {
        bucket: "videos"
      }
      let result = await Vue.axios.post("/api/get-vids", data);
      this.videos = result.data.vids;
      this.loading = false;
    },

    async extractAll() {
      this.dialog = false;
      let data = {
        bucket: "videos"
      }
      await Vue.axios.post("/api/extract-all", data)
    },

    async extractVideo(name) {
      let data = {
        filename: name
      }
      let result = await Vue.axios.post("/api/extract", data);
      let payload = {
        id: result.data.tracking_id,
        status: ""
      }
      await this.$store.dispatch("setQueue", payload.id, payload.status);
    },

    async getStatus() {
      let queue = this.$store.state.queue.slice();
      for (let i = 0; i < queue.length; i++) {
        let s = queue[i];
        let state = await Vue.axios.get("/api/get-status/" + s.id)
        console.warn(state.data);
        console.warn(state.data.id);
        console.warn(state.data.status);
        await this.$store.dispatch("setQueue", state.data.id, state.data.status);
      }
    }
  },
};
</script>

<style></style>