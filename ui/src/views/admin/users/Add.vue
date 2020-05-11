<template>
    <!-- prettier-ignore -->
    <user-form
        :form="form"
        :errors="errors"
        @save:user="save"
    ></user-form>
</template>

<script>
import { mapActions } from 'vuex';
import _ from 'lodash';
import UserForm from './Form.vue';

export default {
    name: 'UserAdd',
    metaInfo: {
        title: 'Add User',
    },
    components: {
        UserForm,
    },
    data() {
        return {
            form: {
                username: '',
                password: '',
                confirm_password: '',
                is_admin: false,
            },
            errors: {},
        };
    },
    methods: {
        ...mapActions({
            saveUser: 'users/saveUser',
        }),
        save(data) {
            this.errors = {}; // clear previous errors if any

            if (data.password !== data.confirm_password) {
                this.errors = {
                    password: 'Passwords must match',
                };
            } else {
                const fields = ['username', 'password', 'is_admin'];
                this.saveUser(_.pick(data, fields))
                    .then(() => {
                        this.$router.push({ name: 'users.index' });
                    })
                    .catch((error) => {
                        const { data: errorData } = error;
                        if (errorData && typeof errorData.message === 'object') {
                            this.errors = errorData.message;
                        }
                        console.log(error);
                    });
            }
        },
    },
};
</script>
