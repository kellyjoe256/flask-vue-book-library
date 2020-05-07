<template>
    <div id="app">
        <main-nav></main-nav>
        <!-- prettier-ignore -->
        <b-container>
            <b-alert
                v-if="message != null"
                :variant="message.type"
                show
                dismissible
            >{{ message.description }}</b-alert>
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

<style scoped>
.container {
    padding-top: 1.5em;
}
</style>
