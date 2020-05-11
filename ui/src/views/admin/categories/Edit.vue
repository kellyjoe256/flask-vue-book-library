<template>
    <!-- prettier-ignore -->
    <category-form
        :form="form"
        :errors="errors"
        @save:category="save"
    ></category-form>
</template>

<script>
import { mapActions } from 'vuex';
import CategoryForm from './Form.vue';

export default {
    name: 'CategoryEdit',
    metaInfo: {
        title: 'Edit Category',
    },
    components: {
        CategoryForm,
    },
    props: ['id'],
    data() {
        return {
            form: {
                name: '',
            },
            errors: {},
        };
    },
    created() {
        this.$Progress.start();

        this.getCategory(this.id)
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
            getCategory: 'categories/getCategory',
            saveCategory: 'categories/saveCategory',
        }),
        save(data) {
            this.errors = {}; // clear previous errors if any

            this.$Progress.start();

            this.saveCategory(data)
                .then(() => {
                    this.$router.push({ name: 'categories.index' });
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
