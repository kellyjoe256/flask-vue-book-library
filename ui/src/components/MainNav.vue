<template>
    <div>
        <b-navbar toggleable="lg" type="light" variant="light">
            <b-container>
                <!-- prettier-ignore -->
                <b-link
                    class="navbar-brand"
                    :to="{ name: baseRoute }"
                    exact
                >{{ navBarBrandLabel }}</b-link>

                <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

                <b-collapse id="nav-collapse" is-nav>
                    <!-- Right aligned nav items -->
                    <b-navbar-nav class="ml-auto">
                        <!-- prettier-ignore -->
                        <template v-if="user">
                            <b-link
                                class="nav-link"
                                :to="{ name: 'categories.index' }"
                            >Categories</b-link>
                            <b-nav-item-dropdown v-if="user" right>
                                <template v-slot:button-content>
                                    <strong>{{ username }}</strong>
                                </template>
                                <!-- prettier-ignore -->
                                <b-dropdown-item
                                    href="#"
                                    @click="logout"
                                >Logout</b-dropdown-item>
                            </b-nav-item-dropdown>
                        </template>
                        <!-- prettier-ignore -->
                        <template v-else>
                            <b-link
                                v-if="user === null"
                                class="nav-link"
                                :to="{ name: 'login' }"
                                exact
                            >Login</b-link>
                        </template>
                    </b-navbar-nav>
                </b-collapse>
            </b-container>
        </b-navbar>
    </div>
</template>

<script>
import _ from 'lodash';
import { mapGetters, mapActions } from 'vuex';

export default {
    name: 'MainNav',
    computed: {
        ...mapGetters({
            user: 'auth/user',
        }),
        username() {
            const { username } = this.user;
            return _.startCase(username);
        },
        baseRoute() {
            return this.user ? 'dashboard' : 'index';
        },
        navBarBrandLabel() {
            return this.user ? 'Dashboard' : 'Book Library';
        },
    },
    methods: {
        ...mapActions({
            logoutAction: 'auth/logout',
        }),
        logout() {
            this.logoutAction()
                .then(() => {
                    this.$router.replace({ name: 'login' });
                })
                // eslint-disable-next-line
                .catch((e) => {
                    this.$router.replace({ name: 'login' });
                });
        },
    },
};
</script>
