// @ts-nocheck
import _ from 'lodash';
import http from '@/services/http';
import { appendQueryString } from '@/utils/functions';

const baseURL = 'users';

export default {
    namespaced: true,
    state: {
        users: [],
    },
    getters: {
        users: (state) => state.users,
    },
    actions: {
        async getUsers({ commit }, queryString = '') {
            const url = appendQueryString(baseURL, queryString);

            try {
                const { data } = await http.get(url);

                commit('SET_USERS', data.data);
                commit('SET_PAGINATION', data, { root: true });

                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async saveUser({ dispatch }, payload) {
            const { id } = payload;
            const url = id ? `${baseURL}/${id}` : baseURL;
            const action = id ? 'edit' : 'add';
            const method = id ? 'PUT' : 'POST';
            const options = {
                headers: {
                    'Content-Type': 'application/json',
                },
            };

            const fields = ['username', 'password', 'is_admin'];
            try {
                const { data } = await http.wrapper({
                    url,
                    method,
                    data: _.pick(payload, fields),
                    ...options,
                });

                const message = {
                    type: 'success',
                    description: `User ${action}ed successfully`,
                };

                dispatch('flashMessage', message, { root: true });

                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        // eslint-disable-next-line
        async getUser({ commit }, id) {
            const url = `${baseURL}/${id}`;

            try {
                const { data } = await http.get(url);

                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async deleteUser({ dispatch }, id) {
            try {
                await http.delete(`${baseURL}/${id}`);

                const message = {
                    type: 'success',
                    description: 'User deleted successfully',
                };
                dispatch('flashMessage', message, { root: true });

                return Promise.resolve();
            } catch (error) {
                return Promise.reject(error);
            }
        },
    },
    mutations: {
        SET_USERS(state, users) {
            state.users = users;
        },
    },
};
