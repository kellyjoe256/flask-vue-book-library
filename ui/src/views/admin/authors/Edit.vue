<template>
    <!-- prettier-ignore -->
    <author-form
        :form="form"
        :errors="errors"
        @save:author="save"
    ></author-form>
</template>

<script>
import { mapActions } from 'vuex';
import AuthorForm from './Form.vue';

export default {
    name: 'AuthorEdit',
    metaInfo: {
        title: 'Edit Author',
    },
    components: {
        AuthorForm,
    },
    props: ['id'],
    data() {
        return {
            form: {
                first_name: '',
                last_name: '',
                gender: '',
                about: '',
            },
            errors: {},
        };
    },
    created() {
        this.$Progress.start();

        this.getAuthor(this.id)
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
            getAuthor: 'authors/getAuthor',
            saveAuthor: 'authors/saveAuthor',
        }),
        save(data) {
            this.errors = {}; // clear previous errors if any

            this.$Progress.start();

            this.saveAuthor(data)
                .then(() => {
                    this.$router.push({ name: 'authors.index' });
                })
                .catch((error) => {
                    this.$Progress.fail();

                    const { data: errorData } = error;
                    if (errorData && typeof errorData.message === 'object') {
                        this.errors = errorData.message;
                    }
                    console.log(error);
                });
        },
    },
};
</script>
