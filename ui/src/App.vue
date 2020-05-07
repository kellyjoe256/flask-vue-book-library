<template>
    <div id="app">
        <main-nav></main-nav>
        <b-container>
            <router-view />
        </b-container>
    </div>
</template>
<script>
import MainNav from '@/components/MainNav.vue';

export default {
    name: 'App',
    components: {
        MainNav,
    },
};
</script>
