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
                        :to="{ name: 'categories.add' }"
                        class="btn btn-outline-secondary"
                    >Add Category</b-link>
                </b-col>
            </b-row>
            <template v-if="!categories.length">
                <h1>No categories available</h1>
            </template>
            <template v-else>
                <b-table
                    :fields="fields"
                    :items="categories"
                    striped
                >
                    <template v-slot:cell(name)="data">
                        {{ data.value }}
                    </template>
                    <template v-slot:cell(id)="data">
                        <b-link
                            :to="{
                                name: 'categories.edit',
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
                    :limit="limit"
                    :fetchMethod="getCategories"
                ></pagination>
            </template>
        </b-col>
    </b-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    name: 'CategoriesListing',
    metaInfo: {
        title: 'Categories',
    },
    created() {
        this.getCategories();
    },
    data() {
        return {
            limit: 0,
            currentPage: 1,
            fields: [
                {
                    key: 'name',
                    sortable: true,
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
            pages: 'pages',
            categories: 'categories/categories',
        }),
    },
    methods: {
        ...mapActions({
            getCategories: 'categories/getCategories',
            deleteCategory: 'categories/deleteCategory',
        }),
        erase(id) {
            // eslint-disable-next-line
            if (!confirm('Are you sure?')) {
                return;
            }

            this.deleteCategory(id)
                .then(() => {
                    this.getCategories();
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
};
</script>
