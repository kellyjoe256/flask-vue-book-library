<template>
    <!-- prettier-ignore -->
    <book-form
        :form="form"
        :errors="errors"
        @save:book="save"
    ></book-form>
</template>

<script>
import { mapActions } from 'vuex';
import BookForm from './Form.vue';

export default {
    name: 'BookAdd',
    metaInfo: {
        title: 'Add Book',
    },
    components: {
        BookForm,
    },
    data() {
        return {
            form: {
                isbn: '',
                title: '',
                num_of_pages: '',
                publisher: '',
                publication_date: '',
                authors: [],
                categories: [],
                about: '',
            },
            errors: {},
        };
    },
    methods: {
        ...mapActions({
            saveBook: 'books/saveBook',
        }),
        save(data) {
            this.errors = {}; // clear previous errors if any

            this.$Progress.start();

            this.saveBook(data)
                .then(() => {
                    this.$router.push({ name: 'books.index' });
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
