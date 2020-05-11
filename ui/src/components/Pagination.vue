<template>
    <div class="overflow-auto">
        <!-- Use text in props -->
        <b-pagination
            v-if="pages > 1"
            v-model="currentPage"
            @change="changePage"
            :total-rows="pagination.meta.total"
            :per-page="pagination.meta.per_page"
            first-text="First"
            prev-text="Prev"
            next-text="Next"
            last-text="Last"
        ></b-pagination>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import eventBus from '@/eventBus';

export default {
    name: 'Pagination',
    props: {
        fetchMethod: {
            type: Function,
            required: true,
        },
    },
    data() {
        return {
            currentPage: 1,
            queryParams: {
                page: 1,
                limit: 10,
                search: null,
            },
        };
    },
    computed: {
        ...mapGetters({
            pages: 'pages',
            pagination: 'pagination',
        }),
    },
    created() {
        eventBus.$on('search', (value) => {
            const currentQueryParams = this.queryParams;
            const queryLinkParams = this.getLinkQueryParams();

            this.currentPage = 1;
            this.queryParams = {
                ...queryLinkParams,
                ...currentQueryParams,
                page: 1,
                search: value,
            };
        });

        eventBus.$on('change:limit', (limit) => {
            const currentQueryParams = this.queryParams;
            const queryLinkParams = this.getLinkQueryParams();

            this.currentPage = 1;
            this.queryParams = {
                ...queryLinkParams,
                ...currentQueryParams,
                page: 1,
                limit,
            };
        });
    },
    watch: {
        queryParams: {
            deep: true,
            // eslint-disable-next-line
            handler: function(newValue, oldValue) {
                const queryString = this.stringifyQueryParams(newValue);

                this.fetchMethod(queryString);
            },
        },
    },
    methods: {
        parseQueryStringParams(url) {
            const index = String(url)
                .trim()
                .indexOf('?');

            if (!(index > -1)) {
                return {};
            }

            const queryString = url.substr(index + 1);

            if (!queryString) {
                return {};
            }

            const queryStringParts = queryString.split('&');
            const output = {};
            for (let i = 0, len = queryStringParts.length; i < len; i += 1) {
                const [key, value] = queryStringParts[i].split('=');
                output[key] = value;
            }

            return output;
        },
        getLinkQueryParams() {
            const { links } = this.pagination;
            const linkQueryParams = this.parseQueryStringParams(links.first);

            return linkQueryParams;
        },
        stringifyQueryParams(params) {
            let output = '';

            Object.entries(params).forEach((entry) => {
                const [key, value] = entry;
                if (value) {
                    const queryString = `${key}=${value}`;
                    output += output ? `&${queryString}` : queryString;
                }
            });

            return output;
        },
        changePage(page) {
            const currentQueryParams = this.queryParams;
            const queryLinkParams = this.getLinkQueryParams();

            this.queryParams = {
                ...queryLinkParams,
                ...currentQueryParams,
                page,
            };
        },
    },
};
</script>
