// @ts-nocheck
import Vue from 'vue';
import Vuex from 'vuex';
import modules from './modules';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        message: null,
        pagination: null,
    },
    getters: {
        message: (state) => state.message,
        pagination: (state) => state.pagination,
        pages: (state) => {
            const { pagination } = state;

            if (!pagination) {
                return false;
            }

            const { meta } = pagination;

            return meta.last_page;
        },
    },
    actions: {
        flashMessage: ({ commit }, message) => {
            commit('SET_MESSAGE', message);

            setTimeout(() => {
                commit('CLEAR_MESSAGE');
            }, 5100);
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

        SET_PAGINATION(state, { meta, links }) {
            state.pagination = {
                meta,
                links,
            };
        },
    },
    modules,
});
