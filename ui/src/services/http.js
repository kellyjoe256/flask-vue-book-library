// @ts-nocheck
import axios from 'axios';
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

        // eslint-disable-next-line arrow-body-style
        const tokenExpired = ['token', 'expired'].every((w) => {
            return description.toLowerCase().includes(w);
        });
        // eslint-disable-next-line arrow-body-style
        const missingCookie = ['missing', 'cookie'].every((w) => {
            return description.toLowerCase().includes(w);
        });

        if (tokenExpired || missingCookie) {
            description = 'Session expired';
        }

        const message = {
            type: 'danger',
            description,
        };

        store.dispatch('flashMessage', message, { root: true });
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
