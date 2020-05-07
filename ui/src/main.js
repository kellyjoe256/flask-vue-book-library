// @ts-nocheck
import Vue from 'vue';
import VueMeta from 'vue-meta';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(VueMeta, {
    refreshOnceOnNavigation: true,
});

new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount('#app');
