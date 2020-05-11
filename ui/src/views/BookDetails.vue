<template>
    <b-row>
        <b-col>
            <p><strong>Title</strong>: {{ book.title }}</p>
            <p><strong># of Pages</strong>: {{ book.num_of_pages }}</p>
            <p><strong>Publisher</strong>: {{ book.publisher }}</p>
            <p><strong>Publication date</strong>: {{ book.publication_date | date }}</p>
            <!-- prettier-ignore -->
            <p v-if="book.categories">
                <strong>Categories</strong>: {{ bookCategories }}
            </p>
            <p><strong>About</strong>:</p>
            <div class="about" v-html="markdownToHtml(book.about)"></div>
        </b-col>
        <b-col>
            <h3>Authors</h3>
            <!-- prettier-ignore -->
            <div
                class="author"
                v-for="(author, index) in book.authors"
                :key="author.id"
            >
                <p>
                    <strong>Name</strong>:
                    {{ `${author.first_name} ${author.last_name}` }}
                </p>
                <p>
                    <strong>Gender</strong>:
                    {{ author.gender === 'M' ? 'Male' : 'Female' }}
                </p>
                <p><strong>About</strong>:</p>
                <div class="about" v-html="markdownToHtml(author.about)"></div>
                <hr v-if="index !== (book.authors.length - 1)" />
            </div>
        </b-col>
    </b-row>
</template>

<script>
import { mapActions } from 'vuex';
import showdown from 'showdown';

export default {
    name: 'BookDetails',
    metaInfo: {
        title: 'Book Details',
    },
    props: ['id'],
    data() {
        return {
            book: {},
        };
    },
    computed: {
        bookCategories() {
            const { categories } = this.book;

            return categories.map((c) => c.name).join(', ');
        },
    },
    created() {
        this.$Progress.start();

        this.getBook(this.id)
            .then((data) => {
                this.$Progress.finish();

                this.book = data;
            })
            /* eslint-disable */
            .catch((error) => {
                this.$Progress.fail();

                const { status } = error;
                if (status === 404) {
                    return this.$router.replace({
                        name: 'index',
                    });
                }

                console.log(error);
            });
    },
    methods: {
        ...mapActions({
            getBook: 'books/getBook',
        }),
        markdownToHtml(value) {
            const converter = new showdown.Converter();

            return converter.makeHtml(value);
        },
    },
};
</script>

<style scoped>
hr {
    margin: 2rem 0;
}
</style>
