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
    name: 'UserEdit',
    metaInfo: {
        title: 'Edit User',
    },
    components: {
        UserForm,
    },
    props: ['id'],
    data() {
        return {
            form: {
                username: '',
                password: '',
                confirm_password: '',
                is_admin: 0,
            },
            errors: {},
        };
    },
    created() {
        this.$Progress.start();

        this.getUser(this.id)
            .then((data) => {
                this.$Progress.finish();

                this.form = {
                    ...data,
                };
            })
            /* eslint-disable */
            .catch((error) => {
                this.$Progress.fail();

                const { status } = error;
                if (status === 404) {
                    return this.$router.replace({
                        name: '404',
                    });
                }

                console.log(error);
            });
    },
    methods: {
        ...mapActions({
            getUser: 'users/getUser',
            saveUser: 'users/saveUser',
        }),
        save(data) {
            this.errors = {}; // clear previous errors if any

            if (data.password !== data.confirm_password) {
                this.errors = {
                    password: 'Passwords must match',
                };
            } else {
                this.$Progress.start();

                const fields = ['id', 'username', 'password', 'is_admin'];
                this.saveUser(_.pick(data, fields))
                    .then(() => {
                        this.$router.push({ name: 'users.index' });
                    })
                    .catch((error) => {
                        this.$Progress.fail();

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
