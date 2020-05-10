// @ts-nocheck
import _ from 'lodash';
import http from '@/services/http';
import { appendQueryString } from '@/utils/functions';

const baseURL = 'categories';

export default {
    namespaced: true,
    state: {
        categories: [],
    },
    getters: {
        categories: (state) => state.categories,
    },
    actions: {
        async getCategories({ commit }, queryString = '') {
            const url = appendQueryString(baseURL, queryString);

            try {
                const { data } = await http.get(url);

                commit('SET_CATEGORIES', data.data);
                commit('SET_PAGINATION', data, { root: true });
                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async saveCategory({ dispatch }, payload) {
            const { id } = payload;
            const url = id ? `${baseURL}/${id}` : baseURL;
            const action = id ? 'edit' : 'add';
            const method = id ? 'PUT' : 'POST';
            const options = {
                headers: {
                    'Content-Type': 'application/json',
                },
            };

            try {
                const { data } = await http.wrapper({
                    url,
                    method,
                    data: _.pick(payload, ['name']),
                    ...options,
                });

                const message = {
                    type: 'success',
                    description: `Category ${action}ed successfully`,
                };

                dispatch('flashMessage', message, { root: true });

                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        // eslint-disable-next-line
        async getCategory({ commit }, id) {
            const url = `${baseURL}/${id}`;

            try {
                const { data } = await http.get(url);

                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async deleteCategory({ dispatch }, id) {
            try {
                await http.delete(`${baseURL}/${id}`);

                const message = {
                    type: 'success',
                    description: 'Category deleted successfully',
                };
                dispatch('flashMessage', message, { root: true });

                return Promise.resolve();
            } catch (error) {
                return Promise.reject(error);
            }
        },
    },
    mutations: {
        SET_CATEGORIES(state, categories) {
            state.categories = categories;
        },
    },
};
