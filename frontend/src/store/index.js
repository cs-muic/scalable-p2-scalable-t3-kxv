import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        queue: []
    },
    mutations: {
        setQueue(state, payload) {
            let data = {
                name: payload.name,
                id: payload.id
            }
            state.queue.push(data);
        },
    },
    actions: {
        setQueue({ commit }, payload) {
            commit("setQueue", payload);
        },
    },
    modules: {},
});