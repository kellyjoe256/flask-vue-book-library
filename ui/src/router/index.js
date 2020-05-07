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

/* eslint-disable */
// prettier-ignore
router.beforeEach((to, from, next) => {
  const authenticated = store.getters['auth/authenticated'];

  let redirectTo = null;
  if (!authenticated && to.meta.authRequired) {
      redirectTo = { name: 'login' };
  } else if (authenticated && to.name !== '404' && !to.meta.authRequired) {
      redirectTo = { name: 'dashboard' };
  }

  if (redirectTo) {
      return next(redirectTo);
  }

  next();
});

export default router;
