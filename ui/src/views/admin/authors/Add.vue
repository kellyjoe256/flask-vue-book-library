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
    name: 'AuthorAdd',
    metaInfo: {
        title: 'Add Author',
    },
    components: {
        AuthorForm,
    },
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
    methods: {
        ...mapActions({
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
