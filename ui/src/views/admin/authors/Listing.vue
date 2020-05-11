<template>
    <b-row class="justify-content-md-center">
        <!-- prettier-ignore -->
        <b-col lg="10" md="auto">
            <b-row>
                <b-col>
                    <pagination-limit></pagination-limit>
                </b-col>
                <b-col class="text-right">
                    <b-link
                        :to="{ name: 'authors.add' }"
                        class="btn btn-outline-secondary"
                    >Add Author</b-link>
                </b-col>
            </b-row>
            <template v-if="!authors.length">
                <h1>No authors available</h1>
            </template>
            <template v-else>
                <b-table
                    :fields="fields"
                    :items="authors"
                    striped
                >
                    <template v-slot:cell(first_name)="data">
                        {{ data.value }}
                    </template>
                    <template v-slot:cell(last_name)="data">
                        {{ data.value }}
                    </template>
                    <template v-slot:cell(gender)="data">
                        {{ data.value === 'M' ? 'Male' : 'Female' }}
                    </template>
                    <template v-slot:cell(id)="data">
                        <b-link
                            :to="{
                                name: 'authors.edit',
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
                    :fetchMethod="getAuthors"
                ></pagination>
            </template>
        </b-col>
    </b-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    name: 'AuthorsListing',
    metaInfo: {
        title: 'Authors',
    },
    created() {
        this.getAuthors();
    },
    data() {
        return {
            fields: [
                {
                    key: 'first_name',
                    label: 'First Name',
                    sortable: true,
                },
                {
                    key: 'last_name',
                    label: 'Last Name',
                    sortable: true,
                },
                {
                    key: 'gender',
                    label: 'Gender',
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
            authors: 'authors/authors',
        }),
    },
    methods: {
        ...mapActions({
            getAuthors: 'authors/getAuthors',
            deleteAuthor: 'authors/deleteAuthor',
        }),
        erase(id) {
            // eslint-disable-next-line
            if (!confirm('Are you sure?')) {
                return;
            }

            this.$Progress.start();

            this.deleteAuthor(id)
                .then(() => {
                    this.getAuthors();

                    this.$Progress.finish();
                })
                .catch((error) => {
                    this.$Progress.fail();

                    console.log(error);
                });
        },
    },
};
</script>
