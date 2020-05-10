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
    name: 'CategoryAdd',
    metaInfo: {
        title: 'Add Category',
    },
    components: {
        CategoryForm,
    },
    data() {
        return {
            form: {
                name: '',
            },
            errors: {},
        };
    },
    methods: {
        ...mapActions({
            saveCategory: 'categories/saveCategory',
        }),
        save(data) {
            this.errors = {}; // clear previous errors if any

            this.saveCategory(data)
                .then(() => {
                    this.$router.push({ name: 'categories.index' });
                })
                .catch((error) => {
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
