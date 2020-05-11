<template>
    <div id="app">
        <vue-progress-bar></vue-progress-bar>
        <main-nav></main-nav>
        <!-- prettier-ignore -->
        <b-toast
            v-if="message != null"
            id="my-toast"
            toaster="b-toaster-top-center"
            :variant="message.type"
            visible
            solid
        >{{ message.description }}</b-toast>
        <b-container id="wrapper">
            <router-view />
        </b-container>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';
import MainNav from '@/components/MainNav.vue';

export default {
    name: 'App',
    components: {
        MainNav,
    },
    mounted() {
        this.$Progress.start();

        this.$router.beforeResolve((to, from, next) => {
            //  start the progress bar
            this.$Progress.start();

            next();
        });

        // eslint-disable-next-line no-unused-vars
        this.$router.afterEach((to, from) => {
            //  finish the progress bar
            this.$Progress.finish();
        });
    },
    computed: {
        ...mapGetters({
            message: 'message',
        }),
    },
};
</script>
