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
    name: 'BookEdit',
    metaInfo: {
        title: 'Edit Book',
    },
    components: {
        BookForm,
    },
    props: ['id'],
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
    created() {
        this.$Progress.start();

        this.getBook(this.id)
            .then((data) => {
                this.$Progress.finish();

                const authors = data.authors.map((author) => author.id);
                const categories = data.categories.map((author) => author.id);

                this.form = {
                    ...data,
                    authors,
                    categories,
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
            getBook: 'books/getBook',
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
