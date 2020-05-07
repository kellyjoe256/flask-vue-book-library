// @ts-nocheck
import http from '@/services/http';

const baseURL = 'auth';

export default {
    namespaced: true,
    state: {
        user: null,
    },
    getters: {
        user: (state) => state.user,
        authenticated: (state) => Boolean(state.user),
    },
    actions: {
        async login({ commit }, credentials) {
            const url = `${baseURL}/login`;
            const options = {
                headers: {
                    'Content-Type': 'application/json',
                },
            };
            try {
                const { data } = await http.post(url, credentials, options);
                commit('SET_USER', data);
                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async authenticate({ state, commit }) {
            if (state.user) {
                return;
            }

            const url = `${baseURL}/me`;
            try {
                const { data } = await http.get(url);
                commit('SET_USER', data);
            } catch (error) {
                commit('SET_USER', null);
            }
        },

        async logout({ commit }) {
            const url = `${baseURL}/logout`;
            try {
                await http.post(url);
                commit('SET_USER', null);
                return Promise.resolve();
            } catch (error) {
                commit('SET_USER', null);
                return Promise.reject(error);
            }
        },
    },
    mutations: {
        SET_USER(state, user) {
            state.user = user;
        },
    },
};
