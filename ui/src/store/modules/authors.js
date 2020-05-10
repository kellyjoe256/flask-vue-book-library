// @ts-nocheck
import _ from 'lodash';
import http from '@/services/http';
import { appendQueryString } from '@/utils/functions';

const baseURL = 'authors';

export default {
    namespaced: true,
    state: {
        authors: [],
    },
    getters: {
        authors: (state) => state.authors,
    },
    actions: {
        async getAuthors({ commit }, queryString = '') {
            const url = appendQueryString(baseURL, queryString);

            try {
                const { data } = await http.get(url);

                commit('SET_AUTHORS', data.data);
                commit('SET_PAGINATION', data, { root: true });
                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async saveAuthor({ dispatch }, payload) {
            const { id } = payload;
            const url = id ? `${baseURL}/${id}` : baseURL;
            const action = id ? 'edit' : 'add';
            const method = id ? 'PUT' : 'POST';
            const options = {
                headers: {
                    'Content-Type': 'application/json',
                },
            };

            const fields = ['first_name', 'last_name', 'gender', 'about'];
            try {
                const { data } = await http.wrapper({
                    url,
                    method,
                    data: _.pick(payload, fields),
                    ...options,
                });

                const message = {
                    type: 'success',
                    description: `Author ${action}ed successfully`,
                };

                dispatch('flashMessage', message, { root: true });

                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        // eslint-disable-next-line
        async getAuthor({ commit }, id) {
            const url = `${baseURL}/${id}`;

            try {
                const { data } = await http.get(url);

                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async deleteAuthor({ dispatch }, id) {
            try {
                await http.delete(`${baseURL}/${id}`);

                const message = {
                    type: 'success',
                    description: 'Author deleted successfully',
                };
                dispatch('flashMessage', message, { root: true });

                return Promise.resolve();
            } catch (error) {
                return Promise.reject(error);
            }
        },
    },
    mutations: {
        SET_AUTHORS(state, authors) {
            state.authors = authors;
        },
    },
};
