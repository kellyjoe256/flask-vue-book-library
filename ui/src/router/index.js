// @ts-nocheck
import Vue from 'vue';
import VueRouter from 'vue-router';
import routes from './routes';
import store from '../store';

Vue.use(VueRouter);

const router = new VueRouter({
    mode: 'hash',
    linkActiveClass: 'active',
    routes,
});

/* eslint-disable no-lonely-if */
router.beforeEach((to, from, next) => {
    const user = store.getters['auth/user'];
    const authenticated = store.getters['auth/authenticated'];

    const authRequired = to.matched.some((route) => route.meta.authRequired);
    const adminRequired = to.matched.some((route) => route.meta.adminRequired);

    if (authRequired) {
        if (!authenticated) {
            next({ name: 'login' });
        } else {
            if (adminRequired && !user.is_admin) {
                next({ name: 'dashboard' });
            } else {
                next();
            }
        }
    } else {
        if (authenticated) {
            next({ name: 'dashboard' });
        } else {
            next();
        }
    }
});

export default router;
