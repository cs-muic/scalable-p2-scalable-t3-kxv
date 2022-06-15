import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        queue: []
    },
    mutations: {
        setQueue(state, payload) {
            state.queue = payload;
        },
    },
    actions: {
        setQueue({ commit }, payload) {
            commit("setQueue", payload);
        },
    },
    modules: {},
});