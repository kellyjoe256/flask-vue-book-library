// @ts-nocheck
import Vue from 'vue';
import Vuex from 'vuex';
import modules from './modules';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        message: null,
    },
    getters: {
        message: (state) => state.message,
    },
    actions: {
        flashMessage: ({ commit }, message) => {
            commit('SET_MESSAGE', message);

            setTimeout(() => {
                commit('CLEAR_MESSAGE');
            }, 5000);
        },
    },
    /* eslint-disable no-param-reassign */
    mutations: {
        SET_MESSAGE(state, message) {
            state.message = message;
        },

        CLEAR_MESSAGE(state) {
            state.message = null;
        },
    },
    modules,
});
