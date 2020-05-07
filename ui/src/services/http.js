// @ts-nocheck
import axios from 'axios';
import store from '../store';

axios.defaults.baseURL = 'http://localhost:5000/api';
axios.defaults.withCredentials = true;

axios.interceptors.response.use(null, (error) => {
    const { response } = error;
    const { status: statusCode } = response;

    if (statusCode >= 400 && statusCode < 500) {
        const message = { type: 'danger' };
        if (response.data) {
            message.description = response.data.error || response.data.message;
        } else {
            message.description = response.statusText;
        }

        return store.dispatch('flashMessage', message, { root: true });
    }

    return Promise.reject(response);
});

export default {
    get: axios.get,
    post: axios.post,
    put: axios.put,
    patch: axios.patch,
    delete: axios.delete,
};
