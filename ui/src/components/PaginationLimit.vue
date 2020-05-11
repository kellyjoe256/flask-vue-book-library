<template>
    <!-- prettier-ignore -->
    <b-form-select
        v-model="selected"
        :class="`mb-3 ${sizeClass}`"
        :options="options"
        @change="changeLimit"
    ></b-form-select>
</template>

<script>
import eventBus from '@/eventBus';

export default {
    name: 'PaginationLimit',
    props: {
        sizeClass: {
            type: String,
            default: 'w-15',
        },
    },
    data() {
        return {
            selected: 10,
            options: [
                { value: 10, text: 10 },
                { value: 15, text: 15 },
                { value: 20, text: 20 },
                { value: 25, text: 25 },
                { value: 30, text: 30 },
            ],
        };
    },
    methods: {
        changeLimit() {
            eventBus.$emit('change:limit', this.selected);
        },
    },
};
</script>
