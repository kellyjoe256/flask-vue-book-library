// @ts-nocheck
import _ from 'lodash';
import http from '@/services/http';
import { appendQueryString } from '@/utils/functions';

const baseURL = 'books';

export default {
    namespaced: true,
    state: {
        books: [],
    },
    getters: {
        books: (state) => state.books,
    },
    actions: {
        async getBooks({ commit }, queryString = '') {
            const url = appendQueryString(baseURL, queryString);

            try {
                const { data } = await http.get(url);

                commit('SET_BOOKS', data.data);
                commit('SET_PAGINATION', data, { root: true });
                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async saveBook({ dispatch }, payload) {
            const { id } = payload;
            const url = id ? `${baseURL}/${id}` : baseURL;
            const action = id ? 'edit' : 'add';
            const method = id ? 'PUT' : 'POST';
            const options = {
                headers: {
                    'Content-Type': 'application/json',
                },
            };

            // prettier-ignore
            const fields = [
                'isbn', 'title', 'num_of_pages',
                'publisher', 'publication_date',
                'authors', 'categories', 'about',
            ];
            try {
                const { data } = await http.wrapper({
                    url,
                    method,
                    data: _.pick(payload, fields),
                    ...options,
                });

                const message = {
                    type: 'success',
                    description: `Book ${action}ed successfully`,
                };

                dispatch('flashMessage', message, { root: true });

                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        // eslint-disable-next-line
        async getBook({ commit }, id) {
            const url = `${baseURL}/${id}`;

            try {
                const { data } = await http.get(url);

                return Promise.resolve(data);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async deleteBook({ dispatch }, id) {
            try {
                await http.delete(`${baseURL}/${id}`);

                const message = {
                    type: 'success',
                    description: 'Book deleted successfully',
                };
                dispatch('flashMessage', message, { root: true });

                return Promise.resolve();
            } catch (error) {
                return Promise.reject(error);
            }
        },
    },
    mutations: {
        SET_BOOKS(state, books) {
            state.books = books;
        },
    },
};
