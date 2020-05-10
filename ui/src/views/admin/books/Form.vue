<template>
    <b-row class="justify-content-md-center">
        <b-col lg="8" md="auto">
            <div class="form">
                <!-- prettier-ignore -->
                <b-form @submit.prevent="onSubmit" autocomplete="off">
                    <b-form-group
                        label="Title"
                        label-for="title"
                    >
                        <b-form-input
                            id="title"
                            placeholder="Title"
                            v-model="form.title"
                            :class="{'is-invalid': hasError('title')}"
                            required trim lazy
                        ></b-form-input>
                        <b-form-invalid-feedback
                            v-if="hasError('title')"
                            v-text="getError('title')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        label="ISBN"
                        label-for="isbn"
                    >
                        <b-form-input
                            id="isbn"
                            placeholder="ISBN"
                            v-model="form.isbn"
                            :class="{'is-invalid': hasError('isbn')}"
                            required trim lazy
                        ></b-form-input>
                        <b-form-invalid-feedback
                            v-if="hasError('isbn')"
                            v-text="getError('isbn')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        label="Number of pages"
                        label-for="num_of_pages"
                    >
                        <b-form-input
                            id="num_of_pages"
                            placeholder="Number of pages"
                            type="number"
                            min="1"
                            v-model="form.num_of_pages"
                            :class="{'is-invalid': hasError('num_of_pages')}"
                            required lazy
                        ></b-form-input>
                        <b-form-invalid-feedback
                            v-if="hasError('num_of_pages')"
                            v-text="getError('num_of_pages')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        label="Publisher"
                        label-for="publisher"
                    >
                        <b-form-input
                            id="publisher"
                            placeholder="Publisher"
                            v-model="form.publisher"
                            :class="{'is-invalid': hasError('publisher')}"
                            required trim lazy
                        ></b-form-input>
                        <b-form-invalid-feedback
                            v-if="hasError('publisher')"
                            v-text="getError('publisher')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        label="Publication Date"
                        label-for="publication_date"
                    >
                        <b-form-datepicker
                            id="publication_date"
                            v-model="form.publication_date"
                            :class="{'is-invalid': hasError('publication_date')}"
                            required lazy
                        ></b-form-datepicker>
                        <b-form-invalid-feedback
                            v-if="hasError('publication_date')"
                            v-text="getError('publication_date')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        label="Categories"
                        label-for="categories"
                    >
                        <v-select
                            id="categories"
                            label="name"
                            placeholder="Select Categories..."
                            v-model.lazy="form.categories"
                            :options="categoryOptions"
                            :reduce="category => category.id"
                            multiple
                        ></v-select>
                        <b-form-invalid-feedback
                            v-if="hasError('categories')"
                            v-text="getError('categories')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        label="Authors"
                        label-for="authors"
                    >
                        <v-select
                            id="authors"
                            label="name"
                            placeholder="Select Authors..."
                            v-model.lazy="form.authors"
                            :options="authorOptions"
                            :reduce="author => author.id"
                            multiple
                        ></v-select>
                        <b-form-invalid-feedback
                            v-if="hasError('authors')"
                            v-text="getError('authors')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        label="About"
                        label-for="about"
                    >
                        <vue-simplemde
                            id="about"
                            v-model="form.about"
                            :configs="configs"
                        ></vue-simplemde>
                    </b-form-group>
                    <p
                        class="sm-8 invalid"
                        v-if="hasError('about')"
                        v-text="getError('about')"
                    ></p>
                    <b-button type="submit" variant="primary">Save</b-button>
                </b-form>
            </div>
        </b-col>
    </b-row>
</template>

<script>
import { mapActions } from 'vuex';
import vSelect from 'vue-select';
import VueSimplemde from 'vue-simplemde';
import formMixin from '@/mixins/form';

export default {
    name: 'BookForm',
    mixins: [formMixin],
    components: {
        VueSimplemde,
        vSelect,
    },
    props: {
        form: {
            type: Object,
            required: true,
        },
        errors: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            authors: [],
            categories: [],
            configs: {
                hideIcons: ['image', 'link'],
            },
        };
    },
    created() {
        const qs = 'all=true'; // query string
        const actions = [this.getAuthors, this.getCategories];

        // prettier-ignore
        Promise.all(
            actions.map((action) => (
                action(qs)
                    .then((result) => result)
                    .catch((error) => error)
            // eslint-disable-next-line comma-dangle
            ))
        )
            .then((data) => {
                const [authors, categories] = data;

                this.authors = authors;
                this.categories = categories;
            })
            .catch((error) => {
                console.log(error);
            });
    },
    computed: {
        authorOptions() {
            return this.authors.map((author) => ({
                id: author.id,
                name: `${author.first_name} ${author.last_name}`,
            }));
        },
        categoryOptions() {
            return this.categories.map((category) => ({
                id: category.id,
                name: category.name,
            }));
        },
    },
    methods: {
        ...mapActions({
            getAuthors: 'authors/getAuthors',
            getCategories: 'categories/getCategories',
        }),
        onSubmit() {
            this.$emit('save:book', this.form);
        },
    },
};
</script>

<style scoped>
@import '~simplemde/dist/simplemde.min.css';
@import '~vue-select/dist/vue-select.css';
</style>
