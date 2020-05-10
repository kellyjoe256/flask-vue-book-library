<template>
    <div id="app">
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
    computed: {
        ...mapGetters({
            message: 'message',
        }),
    },
};
</script>
