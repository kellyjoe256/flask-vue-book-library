// @ts-nocheck
import axios from 'axios';
import _ from 'lodash';
import store from '../store';

axios.defaults.baseURL = 'http://localhost:5000/api';
axios.defaults.withCredentials = true;

axios.interceptors.response.use(null, (error) => {
    const { response } = error;
    const { status: statusCode } = response;

    if (statusCode >= 400 && statusCode < 500) {
        let description = response.data.error || response.data.message;
        if (!description || typeof description !== 'string') {
            description = response.statusText;
        }

        if (!_.lowerCase(description).includes('missing cookie')) {
            description = _.startCase(_.lowerCase(description));

            const message = {
                type: 'danger',
                description,
            };

            store.dispatch('flashMessage', message, { root: true });
        }
    }

    return Promise.reject(response);
});

export default {
    get: axios.get,
    post: axios.post,
    put: axios.put,
    patch: axios.patch,
    delete: axios.delete,
    wrapper: axios,
};
