<template>
    <b-row>
        <!-- prettier-ignore -->
        <b-col>
            <b-row>
                <b-col>
                    <div class="float-left">
                        <pagination-limit sizeClass="w-95"></pagination-limit>
                    </div>
                    <div class="float-left">
                        <b-input
                            id="search"
                            type="search"
                            placeholder="Search..."
                            v-model="searchValue"
                            @keyup="performSearch"
                            class="float-left"
                            trim
                        ></b-input>
                    </div>
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
                                name: 'book.details',
                                params: { id: data.value },
                            }"
                            class="text-dark"
                        ><b-icon icon="eye-fill"></b-icon></b-link>
                    </template>
                </b-table>
            </template>
            <!-- prettier-ignore -->
            <pagination
                :fetchMethod="getBooks"
            ></pagination>
        </b-col>
    </b-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import eventBus from '@/eventBus';

export default {
    name: 'Index',
    metaInfo: {
        title: 'Book Library',
    },
    data() {
        return {
            searchValue: '',
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
    created() {
        this.getBooks();
    },
    computed: {
        ...mapGetters({
            books: 'books/books',
        }),
    },
    methods: {
        ...mapActions({
            getBooks: 'books/getBooks',
        }),
        performSearch() {
            eventBus.$emit('search', this.searchValue);
        },
    },
};
</script>
