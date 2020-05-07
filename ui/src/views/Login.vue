<template>
    <b-row class="justify-content-md-center">
        <b-col lg="8" md="auto">
            <div class="login-form">
                <!-- prettier-ignore -->
                <b-form @submit.prevent="onSubmit" autocomplete="off">
                    <b-form-group
                        id="input-group-1"
                        label="Username"
                        label-for="username"
                    >
                        <b-form-input
                            id="username"
                            placeholder="Username"
                            v-model="form.username"
                            required
                        ></b-form-input>
                    </b-form-group>
                    <b-form-group
                        id="input-group-2"
                        label="Password"
                        label-for="password"
                    >
                        <b-form-input
                            id="password"
                            type="password"
                            placeholder="Password"
                            v-model="form.password"
                            required
                        ></b-form-input>
                    </b-form-group>

                    <b-button type="submit" variant="primary">Submit</b-button>
                </b-form>
            </div>
        </b-col>
    </b-row>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    name: 'Login',
    metaInfo: {
        title: 'Login',
    },
    data() {
        return {
            form: {
                username: '',
                password: '',
            },
        };
    },
    methods: {
        ...mapActions({
            login: 'auth/login',
        }),
        onSubmit() {
            this.login(this.form)
                .then(() => {
                    this.$router.replace({
                        name: 'dashboard',
                    });
                })
                .catch((response) => {
                    console.log(response);
                });
        },
    },
};
</script>
