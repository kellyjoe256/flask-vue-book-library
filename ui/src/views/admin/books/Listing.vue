<template>
    <b-row class="justify-content-md-center">
        <!-- prettier-ignore -->
        <b-col lg="11" md="auto">
            <b-row>
                <b-col>
                    <pagination-limit></pagination-limit>
                </b-col>
                <b-col class="text-right">
                    <b-link
                        :to="{ name: 'books.add' }"
                        class="btn btn-outline-secondary"
                    >Add Book</b-link>
                </b-col>
            </b-row>
            <template v-if="!books.length">
                <h1>No books available</h1>
            </template>
            <template v-else>
                <b-table
                    :fields="fields"
                    :items="books"
                    striped
                >
                    <template v-slot:cell(publication_date)="data">
                        {{ data.value | date }}
                    </template>
                    <template v-slot:cell(id)="data">
                        <b-link
                            :to="{
                                name: 'books.edit',
                                params: { id: data.value },
                            }"
                            class="text-info"
                        ><b-icon icon="pencil"></b-icon></b-link>
                        <a
                            class="text-danger"
                            href="#"
                            @click.prevent="erase(data.value)"
                        >
                            <b-icon icon="trash-fill"></b-icon>
                        </a>
                    </template>
                </b-table>
                <!-- prettier-ignore -->
                <pagination
                    :fetchMethod="getBooks"
                ></pagination>
            </template>
        </b-col>
    </b-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    name: 'BooksListing',
    metaInfo: {
        title: 'Books',
    },
    created() {
        this.getBooks();
    },
    data() {
        return {
            fields: [
                {
                    key: 'title',
                    label: 'Title',
                    sortable: true,
                },
                {
                    key: 'isbn',
                    label: 'ISBN',
                    sortable: true,
                },
                {
                    key: 'num_of_pages',
                    label: '# of Pages',
                    sortable: true,
                },
                {
                    key: 'publisher',
                    label: 'Publisher',
                    sortable: true,
                },
                {
                    key: 'publication_date',
                    label: 'Publication Date',
                },
                {
                    key: 'id',
                    label: '',
                },
            ],
        };
    },
    computed: {
        ...mapGetters({
            books: 'books/books',
        }),
    },
    methods: {
        ...mapActions({
            getBooks: 'books/getBooks',
            deleteBook: 'books/deleteBook',
        }),
        erase(id) {
            // eslint-disable-next-line
            if (!confirm('Are you sure?')) {
                return;
            }

            this.deleteBook(id)
                .then(() => {
                    this.getBooks();
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
};
</script>
