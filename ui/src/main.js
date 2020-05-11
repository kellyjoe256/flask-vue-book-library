// @ts-nocheck
import Vue from 'vue';
import VueMeta from 'vue-meta';
import VueProgressBar from 'vue-progressbar';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import App from './App.vue';
import Pagination from './components/Pagination.vue';
import PaginationLimit from './components/PaginationLimit.vue';
import router from './router';
import store from './store';
import filters from './filters';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import './assets/css/main.css';

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(VueMeta, {
    refreshOnceOnNavigation: true,
});
Vue.use(VueProgressBar, {
    color: '#343434',
    failedColor: '#dd4b39',
    thickness: '4px',
    transition: {
        speed: '1s',
        opacity: '0.9s',
        termination: 600,
    },
    autoRevert: true,
    location: 'top',
    inverse: false,
});

// mixins
Vue.mixin({
    filters,
});

// custom components
Vue.component('pagination', Pagination);
Vue.component('pagination-limit', PaginationLimit);

store.dispatch('auth/authenticate').then(() => {
    new Vue({
        router,
        store,
        render: (h) => h(App),
    }).$mount('#app');
});
