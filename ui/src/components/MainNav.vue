<template>
    <div>
        <b-navbar toggleable="lg" type="light" variant="light">
            <b-container>
                <b-navbar-brand href="#">Book Library</b-navbar-brand>

                <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

                <b-collapse id="nav-collapse" is-nav>
                    <!-- Right aligned nav items -->
                    <b-navbar-nav class="ml-auto">
                        <b-nav-item href="#">Login</b-nav-item>
                    </b-navbar-nav>
                </b-collapse>
            </b-container>
        </b-navbar>
    </div>
</template>

<script>
export default {
    name: 'MainNav',
};
</script>
