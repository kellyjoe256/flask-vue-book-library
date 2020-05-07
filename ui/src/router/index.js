// @ts-nocheck
import Vue from 'vue';
import VueRouter from 'vue-router';

const Index = () => import('@/views/Index');

const routes = [
    {
        path: '/',
        name: 'index',
        component: Index,
    },
];

Vue.use(VueRouter);

const router = new VueRouter({
    mode: 'hash',
    linkActiveClass: 'active',
    routes,
});

export default router;
